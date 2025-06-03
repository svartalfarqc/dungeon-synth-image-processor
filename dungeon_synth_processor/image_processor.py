import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import io
import base64
import tempfile
import os
import random
import atexit
import shutil

class DungeonSynthProcessor:
    """
    Core image processing class that replicates the exact functionality
    of the web application's canvas-based processing with performance optimizations
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        # Register cleanup function
        atexit.register(self.cleanup)
    
    def create_preview_base64(self, image):
        """Create 400x400 preview and return as base64 - matches web app exactly"""
        try:
            # Calculate crop dimensions to maintain aspect ratio and center the image
            width, height = image.size
            size = min(width, height)
            sx = (width - size) // 2
            sy = (height - size) // 2
            
            # Crop to square and resize to 400x400
            cropped = image.crop((sx, sy, sx + size, sy + size))
            preview = cropped.resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = io.BytesIO()
            preview.save(buffer, format='PNG')
            preview_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return f"data:image/png;base64,{preview_base64}"
            
        except Exception as e:
            raise Exception(f"Error creating preview: {str(e)}")
    
    def process_preview(self, filepath, params):
        """Process image with parameters and return 400x400 preview as base64"""
        try:
            # Open and load the image completely into memory
            img = Image.open(filepath)
            img.load()  # Ensure image is fully loaded
            
            # Validate image
            if not self._validate_image(img):
                img.close()
                raise Exception("Invalid or corrupted image file")
            
            # Create preview first
            preview = self._create_square_preview(img, 400)
            
            # Close original image
            img.close()
            
            # Apply processing - exactly matching web app logic
            processed = self._apply_processing(preview, params)
            
            # Convert to base64
            buffer = io.BytesIO()
            processed.save(buffer, format='PNG')
            buffer.seek(0)  # Reset buffer position
            preview_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            return f"data:image/png;base64,{preview_base64}"
            
        except Exception as e:
            raise Exception(f"Error processing preview: {str(e)}")
    
    def process_full_resolution(self, filepath, params, preset_name='custom'):
        """Process image at full resolution and save to temp file"""
        try:
            with Image.open(filepath) as img:
                # Validate image
                if not self._validate_image(img):
                    raise Exception("Invalid or corrupted image file")
                
                # Check if we should use vectorized processing for performance
                pixel_count = img.width * img.height
                if pixel_count > 2000000:  # > 2MP, use vectorized
                    processed = self._apply_processing_vectorized(img, params)
                else:
                    processed = self._apply_processing(img, params)
                
                # Save to temporary file
                output_path = os.path.join(self.temp_dir, f"processed_{preset_name}_{os.path.basename(filepath)}.png")
                processed.save(output_path, 'PNG', quality=100, optimize=True)
                
                return output_path
                
        except Exception as e:
            raise Exception(f"Error processing full resolution image: {str(e)}")
    
    def _validate_image(self, image):
        """Validate image file"""
        try:
            # Check basic properties
            if image.width <= 0 or image.height <= 0:
                return False
            if image.width > 50000 or image.height > 50000:  # Reasonable limit
                return False
            return True
        except:
            return False
    
    def _create_square_preview(self, image, size):
        """Create square preview matching web app crop logic"""
        width, height = image.size
        crop_size = min(width, height)
        sx = (width - crop_size) // 2
        sy = (height - crop_size) // 2
        
        cropped = image.crop((sx, sy, sx + crop_size, sy + crop_size))
        return cropped.resize((size, size), Image.Resampling.LANCZOS)
    
    def _apply_processing(self, image, params):
        """Apply dungeon synth processing - exactly matching web app pixel processing"""
        try:
            # Ensure we're working with RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array for pixel-level manipulation
            img_array = np.array(image)
            
            # Validate array
            if img_array is None or img_array.size == 0:
                raise Exception("Invalid image array")
            
            # Apply blur first if needed (matches web app order)
            if params.get('blur', 0) > 0:
                blur_radius = params['blur']
                # Convert to PIL for gaussian blur, then back to numpy
                pil_img = Image.fromarray(img_array)
                pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                img_array = np.array(pil_img)
            
            # Choose processing method based on image size
            pixel_count = img_array.shape[0] * img_array.shape[1]
            if pixel_count > 160000:  # > 400x400, use vectorized for speed
                processed_array = self._vectorized_process_pixels(
                    img_array,
                    contrast=params.get('contrast', 1.5),
                    brightness=params.get('brightness', 0),
                    threshold=params.get('threshold', 128),
                    noise=params.get('noise', 20),
                    method=params.get('method', 'custom')
                )
            else:
                # Use pixel-by-pixel for exact web app replication on previews
                processed_array = self._process_pixels(
                    img_array,
                    contrast=params.get('contrast', 1.5),
                    brightness=params.get('brightness', 0),
                    threshold=params.get('threshold', 128),
                    noise=params.get('noise', 20),
                    method=params.get('method', 'custom')
                )
            
            # Validate processed array
            if processed_array is None:
                raise Exception("Processing failed - no output generated")
            
            return Image.fromarray(processed_array)
            
        except Exception as e:
            raise Exception(f"Error in image processing: {str(e)}")
    
    def _apply_processing_vectorized(self, image, params):
        """Vectorized processing for better performance on large images"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        img_array = np.array(image)
        
        # Apply blur first if needed
        if params.get('blur', 0) > 0:
            blur_radius = params['blur']
            pil_img = Image.fromarray(img_array)
            pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            img_array = np.array(pil_img)
        
        # Use vectorized processing
        processed_array = self._vectorized_process_pixels(
            img_array,
            contrast=params.get('contrast', 1.5),
            brightness=params.get('brightness', 0),
            threshold=params.get('threshold', 128),
            noise=params.get('noise', 20),
            method=params.get('method', 'custom')
        )
        
        return Image.fromarray(processed_array)
    
    def _process_pixels(self, img_array, contrast, brightness, threshold, noise, method):
        """Pixel-by-pixel processing matching web app exactly"""
        height, width, channels = img_array.shape
        processed = np.zeros_like(img_array)
        
        for y in range(height):
            for x in range(width):
                r, g, b = img_array[y, x]
                
                # Convert to grayscale (luminosity method - matches web app)
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Apply brightness
                gray = max(0, min(255, gray + brightness))
                
                # Apply contrast
                gray = max(0, min(255, int((gray - 128) * contrast + 128)))
                
                # Apply method-specific processing (matches web app switch statement)
                gray = self._apply_method_processing(gray, threshold, method)
                
                # Add noise/grain
                if noise > 0:
                    noise_amount = (random.random() - 0.5) * noise
                    gray = max(0, min(255, int(gray + noise_amount)))
                
                # Set RGB channels to same gray value
                processed[y, x] = [gray, gray, gray]
        
        return processed
    
    def _apply_method_processing(self, gray, threshold, method):
        """Apply method-specific processing exactly matching web app"""
        if method in ['threshold', 'silhouette']:
            return 255 if gray > threshold else 0
        
        elif method == 'manuscript':
            # Add sepia toning before final processing
            return 220 if gray > threshold else 20
        
        elif method == 'ghostly':
            # Softer threshold
            if gray > threshold:
                return min(255, gray + 30)
            else:
                return max(0, gray - 20)
        
        elif method == 'atmospheric':
            # Preserve more midtones
            if gray > threshold + 30:
                return 255
            elif gray < threshold - 30:
                return 0
            else:
                return gray
        
        else:  # custom or default
            return gray
    
    def _vectorized_process_pixels(self, img_array, contrast, brightness, threshold, noise, method):
        """Faster vectorized version for large images"""
        # Convert to grayscale using luminosity method
        gray = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
        
        # Apply brightness
        gray = np.clip(gray + brightness, 0, 255)
        
        # Apply contrast
        gray = np.clip((gray - 128) * contrast + 128, 0, 255)
        
        # Apply method-specific processing
        if method in ['threshold', 'silhouette']:
            gray = np.where(gray > threshold, 255, 0)
        elif method == 'manuscript':
            gray = np.where(gray > threshold, 220, 20)
        elif method == 'ghostly':
            gray = np.where(gray > threshold, np.minimum(255, gray + 30), np.maximum(0, gray - 20))
        elif method == 'atmospheric':
            gray = np.where(gray > threshold + 30, 255, 
                           np.where(gray < threshold - 30, 0, gray))
        
        # Add noise
        if noise > 0:
            noise_array = np.random.uniform(-noise/2, noise/2, gray.shape)
            gray = np.clip(gray + noise_array, 0, 255)
        
        gray = gray.astype(np.uint8)
        
        # Convert back to RGB
        result = np.stack([gray, gray, gray], axis=-1)
        return result

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass  # Ignore cleanup errors