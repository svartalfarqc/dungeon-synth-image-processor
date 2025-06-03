from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import tempfile
import atexit
import logging
import signal
import sys
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64
from image_processor import DungeonSynthProcessor
from presets import PROCESSING_PRESETS

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

# Store current settings for custom downloads
current_custom_params = {
    'contrast': 1.5,
    'brightness': 0,
    'threshold': 128,
    'noise': 20,
    'blur': 0,
    'method': 'custom'
}

# Cleanup on app shutdown
def cleanup_on_exit():
    try:
        processor.cleanup()
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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'webp', 'tif'}
MAX_DIMENSION = 20000  # Maximum width or height

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type. Supported formats: {", ".join(ALLOWED_EXTENSIONS).upper()}'}), 400
        
        try:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Validate image
            with Image.open(filepath) as img:
                if not validate_image_size(img):
                    os.remove(filepath)  # Clean up invalid file
                    return jsonify({'error': f'Image too large. Maximum dimensions: {MAX_DIMENSION}x{MAX_DIMENSION}'}), 400
                
                width, height = img.size
                format_info = img.format or 'Unknown'
                
                # Create 400x400 preview matching web app
                preview_base64 = processor.create_preview_base64(img)
            
            logger.info(f"Image uploaded successfully: {filename} ({width}x{height})")
            
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
            logger.error(f"Image processing error: {str(e)}")
            return jsonify({'error': f'Invalid or corrupted image file: {str(e)}'}), 400
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed. Please try again.'}), 500

@app.route('/process', methods=['POST'])
def process_image():
    """Process image with given parameters and return preview"""
    global current_custom_params
    
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
            
            # Validate parameter ranges
            contrast = max(0.1, min(5.0, contrast))
            brightness = max(-200, min(200, brightness))
            threshold = max(0, min(255, threshold))
            noise = max(0, min(100, noise))
            blur = max(0, min(10, blur))
            
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid parameters provided'}), 400
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Process with validated parameters
        params = {
            'contrast': contrast,
            'brightness': brightness,
            'threshold': threshold,
            'noise': noise,
            'blur': blur,
            'method': method
        }
        
        # Store custom parameters for downloads
        if method == 'custom':
            current_custom_params = params.copy()
        
        # Process and return base64 preview
        preview_base64 = processor.process_preview(filepath, params)
        
        return jsonify({
            'success': True,
            'preview': preview_base64
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/download/<preset_name>/<filename>')
def download_processed(preset_name, filename):
    """Download processed image at full resolution"""
    try:
        # Validate preset name
        if preset_name not in PROCESSING_PRESETS and preset_name != 'custom':
            return jsonify({'error': 'Invalid preset name'}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Original file not found'}), 404
        
        # Get preset parameters matching web app exactly
        if preset_name in PROCESSING_PRESETS:
            params = PROCESSING_PRESETS[preset_name].copy()
        else:
            # Use stored custom parameters
            params = current_custom_params.copy()
        
        # Process at full resolution
        output_path = processor.process_full_resolution(filepath, params, preset_name)
        
        if not os.path.exists(output_path):
            return jsonify({'error': 'Failed to generate processed image'}), 500
        
        logger.info(f"Download started: {preset_name} - {filename}")
        
        # Use send_file with proper cleanup
        def remove_file(response):
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception:
                pass
            return response
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f'dungeon_synth_{preset_name}.png',
            mimetype='image/png'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/get_presets')
def get_presets():
    """Return available processing presets exactly matching web app"""
    return jsonify(PROCESSING_PRESETS)

@app.route('/cleanup/<filename>', methods=['POST'])
def cleanup_file(filename):
    """Clean up uploaded file"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up file: {filename}")
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

# In the main section, replace the app.run() with:
if __name__ == '__main__':
    logger.info("Starting Dungeon Synth Processor...")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
    
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
