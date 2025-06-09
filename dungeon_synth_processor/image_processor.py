import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps
import io
import base64
import tempfile
import os
import random
import atexit
import shutil

class DungeonSynthProcessor:
    """
    Clean dungeon synth processor focused on effective black & white processing
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.processed_cache = {}  # Cache processed previews for exact consistency
        atexit.register(self.cleanup)
    
    def create_preview_base64(self, image):
        """Create 400x400 preview with proper orientation handling"""
        try:
            # Fix orientation from EXIF data
            image = ImageOps.exif_transpose(image)
            
            # Ensure proper color mode for processing
            if image.mode not in ('RGB', 'L'):
                if image.mode == 'RGBA':
                    # Handle transparency by compositing on white background
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                else:
                    image = image.convert('RGB')
            
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
            img = Image.open(filepath)
            img.load()
            
            # Fix orientation from EXIF data
            img = ImageOps.exif_transpose(img)
            
            # Ensure proper color mode
            if img.mode not in ('RGB', 'L'):
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert('RGB')
            
            if not self._validate_image(img):
                img.close()
                raise Exception("Invalid or corrupted image file")
            
            # Create preview first - this gives us consistent 400x400 base
            preview = self._create_square_preview(img, 400)
            img.close()
            
            # Apply processing to the 400x400 preview
            processed = self._apply_processing_to_preview(preview, params)
            
            # Cache the processed result for later download consistency
            cache_key = f"{os.path.basename(filepath)}_{hash(str(params))}"
            self.processed_cache[cache_key] = processed.copy()
            
            # Convert to base64
            buffer = io.BytesIO()
            processed.save(buffer, format='PNG')
            buffer.seek(0)
            preview_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            return f"data:image/png;base64,{preview_base64}"
            
        except Exception as e:
            raise Exception(f"Error processing preview: {str(e)}")
    
    def process_full_resolution(self, filepath, params, preset_name='custom'):
        """Process image at full resolution using the same method as preview for consistency"""
        try:
            # Try to use cached preview result first for exact consistency
            cache_key = f"{os.path.basename(filepath)}_{hash(str(params))}"
            
            if cache_key in self.processed_cache:
                # Use the exact processed preview and upscale it intelligently
                processed_preview = self.processed_cache[cache_key]
                
                # Load original image to get target dimensions
                original_img = Image.open(filepath)
                original_img = ImageOps.exif_transpose(original_img)
                orig_width, orig_height = original_img.size
                
                # Determine if we should crop to square or maintain aspect ratio
                if abs(orig_width - orig_height) < min(orig_width, orig_height) * 0.1:
                    # Nearly square - upscale to fit the larger dimension
                    target_size = max(orig_width, orig_height)
                    final_processed = processed_preview.resize((target_size, target_size), Image.Resampling.LANCZOS)
                else:
                    # Rectangular - create final image matching original aspect ratio
                    # Apply processing to full resolution for better quality on rectangular images
                    original_img_processed = self._apply_processing_to_image(original_img, params)
                    final_processed = original_img_processed
                
                original_img.close()
            else:
                # Fallback: process the full image directly
                img = Image.open(filepath)
                img = ImageOps.exif_transpose(img)
                final_processed = self._apply_processing_to_image(img, params)
                img.close()
            
            # Save to temporary file
            output_path = os.path.join(self.temp_dir, f"processed_{preset_name}_{os.path.basename(filepath)}.png")
            final_processed.save(output_path, 'PNG', quality=100, optimize=True)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error processing full resolution image: {str(e)}")
    
    def _validate_image(self, image):
        """Validate image file"""
        try:
            if image.width <= 0 or image.height <= 0:
                return False
            if image.width > 50000 or image.height > 50000:
                return False
            return True
        except:
            return False
    
    def _create_square_preview(self, image, size):
        """Create square preview matching web app crop logic"""
        # Ensure proper color mode before processing
        if image.mode not in ('RGB', 'L'):
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            else:
                image = image.convert('RGB')
        
        width, height = image.size
        crop_size = min(width, height)
        sx = (width - crop_size) // 2
        sy = (height - crop_size) // 2
        
        cropped = image.crop((sx, sy, sx + crop_size, sy + crop_size))
        return cropped.resize((size, size), Image.Resampling.LANCZOS)
    
    def _apply_processing_to_preview(self, preview_image, params):
        """Apply processing specifically tuned for 400x400 preview"""
        return self._apply_dungeon_synth_processing(preview_image, params, is_preview=True)
    
    def _apply_processing_to_image(self, image, params):
        """Apply processing to any size image with scaling adjustments"""
        return self._apply_dungeon_synth_processing(image, params, is_preview=False)
    
    def _apply_dungeon_synth_processing(self, image, params, is_preview=True):
        """Core dungeon synth processing with consistent results"""
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            
            if img_array is None or img_array.size == 0:
                raise Exception("Invalid image array")
            
            # Apply blur first if needed
            blur_amount = params.get('blur', 0)
            if blur_amount > 0:
                pil_img = Image.fromarray(img_array)
                pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=blur_amount))
                img_array = np.array(pil_img)
            
            # Convert to grayscale using luminosity method
            gray = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
            
            # Apply brightness
            brightness = params.get('brightness', 0)
            gray = np.clip(gray + brightness, 0, 255)
            
            # Apply contrast
            contrast = params.get('contrast', 1.5)
            gray = np.clip((gray - 128) * contrast + 128, 0, 255)
            
            # Apply method-specific processing
            threshold = params.get('threshold', 128)
            method = params.get('method', 'custom')
            
            if method in ['threshold', 'silhouette']:
                gray = np.where(gray > threshold, 255, 0)
            elif method == 'manuscript':
                gray = np.where(gray > threshold, 220, 20)
            elif method == 'ghostly':
                gray = np.where(gray > threshold, np.minimum(255, gray + 30), np.maximum(0, gray - 20))
            elif method == 'atmospheric':
                gray = np.where(gray > threshold + 30, 255, 
                               np.where(gray < threshold - 30, 0, gray))
            elif method == 'cavern':
                gray = np.where(gray > threshold + 40, 255,
                               np.where(gray < threshold - 60, 0, gray * 0.3))
            elif method == 'frozen':
                gray = np.where(gray > threshold, np.minimum(255, gray * 1.2), 
                               np.maximum(0, gray * 0.4))
            elif method == 'ritual':
                gray = np.where(gray > threshold + 20, 255,
                               np.where(gray < threshold - 40, 0, gray * 0.8))
            
            # Add noise/grain with consistent pattern
            noise_amount = params.get('noise', 20)
            if noise_amount > 0:
                # Create deterministic noise pattern based on image content and parameters
                height, width = gray.shape
                seed_value = int(np.sum(gray) % 1000) + hash(str(params)) % 1000
                np.random.seed(seed_value)
                
                # Scale noise based on image size for visual consistency
                if is_preview:
                    noise_scale = 1.0
                else:
                    # Adjust noise for larger images to maintain visual appearance
                    pixel_count = height * width
                    if pixel_count > 160000:  # Larger than 400x400
                        noise_scale = min(2.0, np.sqrt(pixel_count / 160000))
                    else:
                        noise_scale = 1.0
                
                scaled_noise = noise_amount * noise_scale
                noise_array = np.random.uniform(-scaled_noise/2, scaled_noise/2, gray.shape)
                gray = np.clip(gray + noise_array, 0, 255)
            
            gray = gray.astype(np.uint8)
            result = np.stack([gray, gray, gray], axis=-1)
            return Image.fromarray(result)
            
        except Exception as e:
            raise Exception(f"Error in dungeon synth processing: {str(e)}")
    
    # Legacy method support for backward compatibility
    def _apply_processing(self, image, params):
        """Legacy method - redirects to new consistent processing"""
        return self._apply_dungeon_synth_processing(image, params, is_preview=True)
    
    def _apply_processing_vectorized(self, image, params):
        """Legacy method - redirects to new consistent processing"""
        return self._apply_dungeon_synth_processing(image, params, is_preview=False)

    def cleanup(self):
        """Clean up temporary files and cache"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            self.processed_cache.clear()
        except Exception:
            pass