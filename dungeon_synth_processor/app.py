from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import tempfile
import atexit
import logging
import signal
import sys
from werkzeug.utils import secure_filename
import PIL
from PIL import Image, ImageOps
import io
import base64

from image_processor import DungeonSynthProcessor
from presets import PROCESSING_PRESETS, COLOR_TINTS, get_color_tint_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize processor
processor = DungeonSynthProcessor()

# Store processed preview images for download
preview_cache = {}

# Cleanup on app shutdown
def cleanup_on_exit():
    try:
        processor.cleanup()
        preview_cache.clear()
        logger.info("Application shutdown - cleaned up temporary files")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def signal_handler(signum, frame):
    logger.info("Received shutdown signal, cleaning up...")
    cleanup_on_exit()
    sys.exit(0)

# Register cleanup handlers
atexit.register(cleanup_on_exit)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'webp', 'tif'}
MAX_DIMENSION = 20000  # Maximum width or height

def allowed_file(filename):
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

def validate_image_size(image):
    """Validate image dimensions"""
    if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
        return False
    if image.width <= 0 or image.height <= 0:
        return False
    return True

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 32MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error occurred.'}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and return base64 preview"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not '.' in file.filename:
            return jsonify({'error': 'Invalid file - no extension found'}), 400
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        if extension not in ALLOWED_EXTENSIONS:
            supported_formats = list(ALLOWED_EXTENSIONS)
            return jsonify({
                'error': f'Invalid file type. Supported formats: {", ".join(supported_formats).upper()}'
            }), 400
        
        try:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.' + extension
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Validate image
            with Image.open(filepath) as img:
                # Force load and apply EXIF orientation correction
                img.load()
                img = ImageOps.exif_transpose(img)
                
                # Convert problematic modes to RGB
                if img.mode not in ('RGB', 'L'):
                    if img.mode == 'RGBA':
                        # Handle transparency by creating white background
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    else:
                        img = img.convert('RGB')
                
                if not validate_image_size(img):
                    os.remove(filepath)  # Clean up invalid file
                    return jsonify({'error': f'Image too large. Maximum dimensions: {MAX_DIMENSION}x{MAX_DIMENSION}'}), 400
                
                width, height = img.size
                format_info = img.format or 'Unknown'
                
                # Create 400x400 preview matching web app
                preview_base64 = processor.create_preview_base64(img)
            
            # Initialize preview cache for this file
            preview_cache[filename] = {}
            
            logger.info(f"Image uploaded successfully: {filename} ({width}x{height}, {format_info})")
            
            return jsonify({
                'success': True,
                'filename': filename,
                'width': width,
                'height': height,
                'format': format_info,
                'preview': preview_base64
            })
            
        except Exception as e:
            # Clean up file if processing failed
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            
            error_msg = f'Invalid or corrupted image file: {str(e)}'
            logger.error(f"Image processing error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed. Please try again.'}), 500

@app.route('/process', methods=['POST'])
def process_image():
    """Process image with given parameters and return preview"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        filename = data.get('filename')
        
        # Extract and validate parameters
        try:
            contrast = float(data.get('contrast', 1.5))
            brightness = int(data.get('brightness', 0))
            threshold = int(data.get('threshold', 128))
            noise = int(data.get('noise', 20))
            blur = float(data.get('blur', 0))
            method = data.get('method', 'custom')
            color_tint = data.get('color_tint', 'none')
            
            # Validate parameter ranges
            contrast = max(0.1, min(5.0, contrast))
            brightness = max(-200, min(200, brightness))
            threshold = max(0, min(255, threshold))
            noise = max(0, min(100, noise))
            blur = max(0, min(10, blur))
            
            # Validate color tint
            if color_tint not in COLOR_TINTS:
                color_tint = 'none'
            
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid parameters provided'}), 400
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Process with validated parameters
        params = {
            'contrast': float(data.get('contrast', 1.5)),
            'brightness': int(data.get('brightness', 0)),
            'threshold': int(data.get('threshold', 128)),
            'noise': int(data.get('noise', 20)),
            'blur': float(data.get('blur', 0)),
            'method': data.get('method', 'custom'),
            'color_tint': color_tint
        }
        
        # Process and return base64 preview
        preview_base64 = processor.process_preview(filepath, params)
        
        # Cache the processed preview for download
        # Convert base64 back to PIL Image for caching
        image_data = base64.b64decode(preview_base64.split(',')[1])
        processed_image = Image.open(io.BytesIO(image_data))
        
        # Store in cache with method and color tint as key
        cache_key = f"{method}_{color_tint}"
        if filename not in preview_cache:
            preview_cache[filename] = {}
        preview_cache[filename][cache_key] = processed_image.copy()
        
        # Also store with just the method name for preset downloads
        if method != 'custom':
            preset_cache_key = f"{method}_{color_tint}"
            preview_cache[filename][preset_cache_key] = processed_image.copy()
        
        return jsonify({
            'success': True,
            'preview': preview_base64
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/download/<preset_name>/<filename>')
def download_processed(preset_name, filename):
    """Download processed image at specified size (default 400x400)"""
    try:
        # Validate preset name
        if preset_name not in PROCESSING_PRESETS and preset_name != 'custom':
            return jsonify({'error': 'Invalid preset name'}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Original file not found'}), 404
        
        # Get the current color tint and size from request
        data = request.args
        color_tint = data.get('tint', 'none')
        size = int(data.get('size', '400'))
        
        # Create cache key to find the exact processed version
        cache_key = f"{preset_name}_{color_tint}"
        
        # For sizes other than 400, we need to reprocess at target resolution
        if size != 400:
            logger.info(f"Processing for download: {preset_name} at {size}x{size} with tint {color_tint}")
            
            # Get parameters for this preset
            if preset_name == 'custom':
                # For custom, we need to get the current slider values from the request
                params = {
                    'contrast': float(data.get('contrast', 1.5)),
                    'brightness': int(data.get('brightness', 0)),
                    'threshold': int(data.get('threshold', 128)),
                    'noise': int(data.get('noise', 20)),
                    'blur': float(data.get('blur', 0)),
                    'method': 'custom',
                    'color_tint': color_tint
                }
            else:
                # For presets, use the preset parameters
                params = PROCESSING_PRESETS[preset_name].copy()
                params['color_tint'] = color_tint
            
            # Process at target size
            processed_path = processor.process_at_size(filepath, params, size)
            
            # Create filename with color tint if applied
            tint_suffix = f'_{color_tint}' if color_tint != 'none' else ''
            download_name = f'dungeon_synth_{preset_name}{tint_suffix}_{size}x{size}.png'
            
            logger.info(f"Download started: {preset_name} - {filename} with tint {color_tint} ({size}x{size})")
            
            return send_file(
                processed_path,
                as_attachment=True,
                download_name=download_name,
                mimetype='image/png'
            )
        
        # For 400x400, use existing cache logic
        if filename in preview_cache and cache_key in preview_cache[filename]:
            # Use the cached version - this is the exact preview shown
            processed_image = preview_cache[filename][cache_key]
        else:
            # If not cached, we need to reprocess with the exact same parameters
            logger.info(f"Reprocessing for download: {preset_name} with tint {color_tint}")
            
            # Get parameters for this preset
            if preset_name == 'custom':
                # For custom, we need to get the current slider values from the request
                params = {
                    'contrast': float(data.get('contrast', 1.5)),
                    'brightness': int(data.get('brightness', 0)),
                    'threshold': int(data.get('threshold', 128)),
                    'noise': int(data.get('noise', 20)),
                    'blur': float(data.get('blur', 0)),
                    'method': 'custom',
                    'color_tint': color_tint
                }
            else:
                # For presets, use the preset parameters
                params = PROCESSING_PRESETS[preset_name].copy()
                params['color_tint'] = color_tint
            
            # Process to get the exact same result
            preview_base64 = processor.process_preview(filepath, params)
            
            # Convert base64 to PIL Image
            image_data = base64.b64decode(preview_base64.split(',')[1])
            processed_image = Image.open(io.BytesIO(image_data))
            
            # Cache it for future use
            if filename not in preview_cache:
                preview_cache[filename] = {}
            preview_cache[filename][cache_key] = processed_image.copy()
        
        # Save to temporary file for download
        temp_path = os.path.join(processor.temp_dir, f"download_{preset_name}_{color_tint}_{filename}.png")
        processed_image.save(temp_path, 'PNG', quality=100, optimize=False)
        
        # Create filename with color tint if applied
        tint_suffix = f'_{color_tint}' if color_tint != 'none' else ''
        download_name = f'dungeon_synth_{preset_name}{tint_suffix}_400x400.png'
        
        logger.info(f"Download started: {preset_name} - {filename} with tint {color_tint} (400x400)")
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='image/png'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/get_presets')
def get_presets():
    """Return available processing presets exactly matching web app"""
    return jsonify(PROCESSING_PRESETS)

@app.route('/get_color_tints')
def get_color_tints():
    """Return available color tints for UI"""
    return jsonify(get_color_tint_info())

@app.route('/cleanup/<filename>', methods=['POST'])
def cleanup_file(filename):
    """Clean up uploaded file and cached previews"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up file: {filename}")
        
        # Clean up cached previews
        if filename in preview_cache:
            del preview_cache[filename]
            
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return jsonify({'error': 'Cleanup failed'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'presets_available': len(PROCESSING_PRESETS),
        'color_tints_available': len(COLOR_TINTS),
        'upload_folder': os.path.exists(app.config['UPLOAD_FOLDER'])
    })

def find_free_port():
    """Find a free port to use"""
    import socket
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if __name__ == '__main__':
    logger.info("Starting Enhanced Dungeon Synth Processor...")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
    logger.info(f"Supported formats: {', '.join(ALLOWED_EXTENSIONS).upper()}")
    logger.info(f"Available presets: {len(PROCESSING_PRESETS)}")
    logger.info(f"Available color tints: {len(COLOR_TINTS)}")
    
    try:
        port = 5000
        try:
            app.run(
                debug=True, 
                host='127.0.0.1',
                port=port,
                threaded=True,
                use_reloader=True
            )
        except OSError as e:
            if "Address already in use" in str(e):
                port = find_free_port()
                logger.info(f"Port 5000 in use, trying port {port}")
                app.run(
                    debug=True, 
                    host='127.0.0.1',
                    port=port,
                    threaded=True,
                    use_reloader=True
                )
            else:
                raise
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        cleanup_on_exit()
    except Exception as e:
        logger.error(f"Application error: {e}")
        cleanup_on_exit()