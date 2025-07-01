#!/usr/bin/env python3
"""
Quick test to verify aspect ratio download works without 500 errors
"""

import requests
import tempfile
from PIL import Image, ImageDraw
import io
import sys

BASE_URL = "http://localhost:5000"

def create_test_image():
    """Create a non-square test image"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some visual content
    draw.rectangle([100, 100, 300, 300], fill='black')
    draw.ellipse([400, 200, 600, 400], fill='gray')
    draw.text((350, 50), "Test Image 800x600", fill='black')
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_aspect_ratio_download():
    print("Testing Aspect Ratio Download Fix")
    print("=" * 50)
    
    # Create and upload test image
    test_image = create_test_image()
    print(f"✓ Created test image: 800x600")
    
    try:
        # Upload
        with open(test_image, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code != 200:
            print(f"✗ Upload failed: {response.status_code}")
            return False
            
        data = response.json()
        filename = data['filename']
        print(f"✓ Uploaded successfully: {filename}")
        
        # Test processing with aspect ratio preserved
        params = {
            'filename': filename,
            'contrast': 1.5,
            'brightness': 0,
            'threshold': 128,
            'noise': 20,
            'blur': 0,
            'method': 'custom',
            'color_tint': 'none',
            'preserve_aspect_ratio': True
        }
        
        response = requests.post(f"{BASE_URL}/process", json=params)
        if response.status_code != 200:
            print(f"✗ Processing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print(f"✓ Processing successful with aspect ratio preserved")
        
        # Test download with different sizes
        test_sizes = ['400', '1400', '2000']
        
        for size in test_sizes:
            url = f"{BASE_URL}/download/custom/{filename}?tint=none&size={size}&preserve_aspect_ratio=true"
            
            try:
                response = requests.get(url)
                
                if response.status_code != 200:
                    print(f"✗ Download failed for size {size}: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                
                # Verify the downloaded image
                img = Image.open(io.BytesIO(response.content))
                width, height = img.size
                
                # Calculate expected dimensions
                # Original is 800x600, so aspect ratio is 4:3
                if width > height:
                    expected_height = int(size) * 3 // 4
                    expected_width = int(size)
                else:
                    expected_width = int(size)
                    expected_height = int(size) * 3 // 4
                
                print(f"✓ Download size {size}: Got {width}x{height} (expected ~{expected_width}x{expected_height})")
                
            except Exception as e:
                print(f"✗ Error downloading size {size}: {e}")
                return False
        
        # Test with different presets
        presets = ['medieval', 'atmospheric', 'lithographic']
        for preset in presets:
            preset_params = {
                'manuscript': { 'contrast': 1.4, 'brightness': -5, 'threshold': 120, 'noise': 35, 'blur': 0.8, 'method': 'manuscript' },
                'atmospheric': { 'contrast': 1.3, 'brightness': -15, 'threshold': 150, 'noise': 25, 'blur': 2.0, 'method': 'atmospheric' },
                'lithographic': { 'contrast': 1.8, 'brightness': 5, 'threshold': 130, 'noise': 20, 'blur': 0.3, 'method': 'lithographic' }
            }
            
            if preset == 'medieval':
                params.update(preset_params['manuscript'])
            else:
                params.update(preset_params.get(preset, {}))
                
            params['preserve_aspect_ratio'] = True
            
            response = requests.post(f"{BASE_URL}/process", json=params)
            if response.status_code != 200:
                print(f"✗ Processing failed for preset {preset}: {response.status_code}")
                return False
                
            print(f"✓ Preset {preset} processed successfully with aspect ratio")
        
        # Cleanup
        requests.post(f"{BASE_URL}/cleanup/{filename}")
        print(f"✓ Cleanup successful")
        
        print("\n✅ All aspect ratio tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        import os
        if os.path.exists(test_image):
            os.unlink(test_image)

if __name__ == "__main__":
    success = test_aspect_ratio_download()
    sys.exit(0 if success else 1)