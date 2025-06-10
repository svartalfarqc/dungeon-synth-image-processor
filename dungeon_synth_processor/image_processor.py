import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps, ImageChops
import io
import base64
import tempfile
import os
import random
import atexit
import shutil
from presets import get_color_tint

class DungeonSynthProcessor:
    """
    Enhanced dungeon synth processor with authentic visual processing and color tinting
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.processed_cache = {}
        atexit.register(self.cleanup)
    
    def create_preview_base64(self, image):
        """Create 400x400 preview with proper orientation handling"""
        try:
            # Fix orientation from EXIF data
            image = ImageOps.exif_transpose(image)
            
            # Ensure proper color mode for processing
            if image.mode not in ('RGB', 'L'):
                if image.mode == 'RGBA':
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
            
            # Apply color tinting if specified
            color_tint = params.get('color_tint', 'none')
            if color_tint and color_tint != 'none':
                processed = self._apply_color_tint(processed, color_tint)
            
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
    
    def _apply_color_tint(self, image, tint_name):
        """Apply color tinting to processed image"""
        try:
            tint_info = get_color_tint(tint_name)
            if not tint_info or not tint_info.get('color'):
                return image
            
            # Convert hex color to RGB
            hex_color = tint_info['color'].lstrip('#')
            tint_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            opacity = tint_info.get('opacity', 0.3)
            blend_mode = tint_info.get('blend_mode', 'overlay')
            
            # Create tint layer
            tint_layer = Image.new('RGB', image.size, tint_rgb)
            
            # Apply blend mode
            if blend_mode == 'overlay':
                result = self._blend_overlay(image, tint_layer, opacity)
            elif blend_mode == 'multiply':
                result = self._blend_multiply(image, tint_layer, opacity)
            elif blend_mode == 'soft_light':
                result = self._blend_soft_light(image, tint_layer, opacity)
            else:
                # Default to normal blend
                result = Image.blend(image, tint_layer, opacity)
            
            return result
            
        except Exception as e:
            # If tinting fails, return original image
            return image
    
    def _blend_overlay(self, base, overlay, opacity):
        """Overlay blend mode implementation"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        # Overlay blend formula
        mask = base_array < 0.5
        result = np.where(mask, 
                         2 * base_array * overlay_array,
                         1 - 2 * (1 - base_array) * (1 - overlay_array))
        
        # Apply opacity
        result = base_array * (1 - opacity) + result * opacity
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    def _blend_multiply(self, base, overlay, opacity):
        """Multiply blend mode implementation"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        # Multiply blend
        result = base_array * overlay_array
        
        # Apply opacity
        result = base_array * (1 - opacity) + result * opacity
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    def _blend_soft_light(self, base, overlay, opacity):
        """Soft light blend mode implementation"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        # Soft light blend formula (simplified)
        mask = overlay_array < 0.5
        result = np.where(mask,
                         base_array - (1 - 2 * overlay_array) * base_array * (1 - base_array),
                         base_array + (2 * overlay_array - 1) * (np.sqrt(base_array) - base_array))
        
        # Apply opacity
        result = base_array * (1 - opacity) + result * opacity
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
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
        """Enhanced dungeon synth processing with research-based methods"""
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
            
            # Apply contrast with research-based curves
            contrast = params.get('contrast', 1.5)
            method = params.get('method', 'custom')
            
            # Apply method-specific contrast curves
            if method in ['comfy', 'sepia']:
                # Lower contrast for warm, inviting aesthetics
                gray = np.clip((gray - 128) * (contrast * 0.8) + 128, 0, 255)
            elif method in ['lithographic', 'forest']:
                # Medium contrast with S-curve
                gray = self._apply_s_curve(gray, contrast)
            else:
                # Standard contrast
                gray = np.clip((gray - 128) * contrast + 128, 0, 255)
            
            # Apply method-specific processing
            threshold = params.get('threshold', 128)
            
            if method == 'threshold':
                gray = np.where(gray > threshold, 255, 0)
            elif method == 'silhouette':
                gray = np.where(gray > threshold, 255, 0)
            elif method == 'manuscript':
                # Manuscript processing with aged parchment effect
                gray = self._apply_manuscript_effect(gray, threshold)
            elif method == 'ghostly':
                gray = np.where(gray > threshold, np.minimum(255, gray + 30), np.maximum(0, gray - 20))
            elif method == 'atmospheric':
                # Tonal compression for atmospheric effect
                gray = self._apply_tonal_compression(gray, threshold)
            elif method == 'cavern':
                gray = np.where(gray > threshold + 40, 255,
                               np.where(gray < threshold - 60, 0, gray * 0.3))
            elif method == 'frozen':
                # Crystalline processing
                gray = self._apply_crystalline_effect(gray, threshold)
            elif method == 'ritual':
                gray = np.where(gray > threshold + 20, 255,
                               np.where(gray < threshold - 40, 0, gray * 0.8))
            elif method == 'lithographic':
                # Lithographic/engraving simulation
                gray = self._apply_lithographic_effect(gray, threshold)
            elif method == 'sepia':
                # Vintage film effect
                gray = self._apply_vintage_film_effect(gray, threshold)
            elif method == 'comfy':
                # Warm hearth effect
                gray = self._apply_comfy_effect(gray, threshold)
            elif method == 'forest':
                # Organic texture enhancement
                gray = self._apply_forest_effect(gray, threshold)
            
            # Add noise/grain with method-specific characteristics
            noise_amount = params.get('noise', 20)
            if noise_amount > 0:
                gray = self._apply_method_specific_noise(gray, noise_amount, method, params)
            
            gray = gray.astype(np.uint8)
            result = np.stack([gray, gray, gray], axis=-1)
            return Image.fromarray(result)
            
        except Exception as e:
            raise Exception(f"Error in dungeon synth processing: {str(e)}")
    
    def _apply_s_curve(self, gray, contrast):
        """Apply S-curve for gentle contrast enhancement"""
        # Normalize to 0-1
        normalized = gray / 255.0
        # Apply S-curve
        s_curve = 1 / (1 + np.exp(-contrast * (normalized - 0.5)))
        return np.clip(s_curve * 255, 0, 255)
    
    def _apply_manuscript_effect(self, gray, threshold):
        """Medieval manuscript processing"""
        # Create aged parchment effect
        aged = np.where(gray > threshold, 
                       np.minimum(255, gray * 0.9 + 20),  # Slightly yellowed whites
                       np.maximum(15, gray * 0.8))        # Deep but not pure blacks
        return aged
    
    def _apply_tonal_compression(self, gray, threshold):
        """Atmospheric tonal compression"""
        # Compress dynamic range while preserving detail
        compressed = gray * 0.7 + 40  # Lift shadows, compress highlights
        return np.clip(compressed, 0, 255)
    
    def _apply_crystalline_effect(self, gray, threshold):
        """Winter synth crystalline processing"""
        # Sharp, clean transitions with enhanced highlights
        return np.where(gray > threshold, 
                       np.minimum(255, gray * 1.3), 
                       np.maximum(0, gray * 0.5))
    
    def _apply_lithographic_effect(self, gray, threshold):
        """Lithographic/engraving simulation"""
        # Simulate halftone patterns and cross-hatching
        return np.where(gray > threshold + 20, 255,
                       np.where(gray < threshold - 20, 0, gray))
    
    def _apply_vintage_film_effect(self, gray, threshold):
        """Vintage film degradation effect"""
        # Lifted blacks, compressed highlights
        lifted = gray * 0.8 + 30
        return np.clip(lifted, 0, 240)  # Prevent pure whites
    
    def _apply_comfy_effect(self, gray, threshold):
        """Warm comfy synth processing"""
        # Gentle, low contrast with lifted shadows
        comfy = gray * 0.7 + 50
        return np.clip(comfy, 0, 255)
    
    def _apply_forest_effect(self, gray, threshold):
        """Forest/organic texture enhancement"""
        # Enhanced midtones for organic detail
        return np.where(gray > threshold + 30, 255,
                       np.where(gray < threshold - 30, 0, gray * 1.1))
    
    def _apply_method_specific_noise(self, gray, noise_amount, method, params):
        """Apply noise based on method characteristics"""
        height, width = gray.shape
        seed_value = int(np.sum(gray) % 1000) + hash(str(params)) % 1000
        np.random.seed(seed_value)
        
        if method in ['manuscript', 'lithographic']:
            # Coarser grain for aged/printed effects
            noise_scale = noise_amount * 1.2
            grain_size = 2
        elif method in ['comfy', 'sepia']:
            # Fine, gentle grain
            noise_scale = noise_amount * 0.8
            grain_size = 1
        elif method in ['frozen', 'crystalline']:
            # Minimal, sharp grain
            noise_scale = noise_amount * 0.6
            grain_size = 1
        else:
            # Standard grain
            noise_scale = noise_amount
            grain_size = 1
        
        # Generate appropriate noise pattern
        if grain_size > 1:
            # Create coarser grain
            small_noise = np.random.uniform(-noise_scale/2, noise_scale/2, 
                                          (height//grain_size, width//grain_size))
            noise_array = np.repeat(np.repeat(small_noise, grain_size, axis=0), grain_size, axis=1)
            # Crop to exact size
            noise_array = noise_array[:height, :width]
        else:
            noise_array = np.random.uniform(-noise_scale/2, noise_scale/2, gray.shape)
        
        return np.clip(gray + noise_array, 0, 255)

    def cleanup(self):
        """Clean up temporary files and cache"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            self.processed_cache.clear()
        except Exception:
            pass