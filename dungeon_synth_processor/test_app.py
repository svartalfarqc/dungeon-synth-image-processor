#!/usr/bin/env python3
"""
Comprehensive test script for the Dungeon Synth Image Processor
Tests all features to ensure no regressions
"""

import os
import sys
import json
import time
import threading
import requests
from PIL import Image
import io
import base64
import tempfile

# Configuration
BASE_URL = "http://localhost:5000"
TEST_IMAGE_SIZE = (800, 600)  # Non-square to test aspect ratio
TEST_RESULTS = []

def log_test(test_name, success, details=""):
    """Log test results"""
    result = {
        "test": test_name,
        "success": success,
        "details": details,
        "timestamp": time.time()
    }
    TEST_RESULTS.append(result)
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {test_name} - {details}")

def create_test_image():
    """Create a test image for processing"""
    img = Image.new('RGB', TEST_IMAGE_SIZE, color='white')
    # Add some content for testing
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Draw a gradient
    for i in range(TEST_IMAGE_SIZE[0]):
        gray = int(255 * (i / TEST_IMAGE_SIZE[0]))
        draw.line([(i, 0), (i, TEST_IMAGE_SIZE[1])], fill=(gray, gray, gray))
    # Add shapes
    draw.rectangle([100, 100, 300, 300], fill='black')
    draw.ellipse([400, 200, 600, 400], fill='gray')
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_server_health():
    """Test if server is running and healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            log_test("Server Health Check", True, f"Presets: {data['presets_available']}, Tints: {data['color_tints_available']}")
            return True
        else:
            log_test("Server Health Check", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Server Health Check", False, str(e))
        return False

def test_file_upload(image_path):
    """Test file upload functionality"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                log_test("File Upload", True, f"Filename: {data['filename']}, Size: {data['width']}x{data['height']}")
                return data['filename']
            else:
                log_test("File Upload", False, data.get('error', 'Unknown error'))
                return None
        else:
            log_test("File Upload", False, f"Status code: {response.status_code}")
            return None
    except Exception as e:
        log_test("File Upload", False, str(e))
        return None

def test_processing(filename, params, test_name):
    """Test image processing with given parameters"""
    try:
        data = {
            'filename': filename,
            **params
        }
        response = requests.post(f"{BASE_URL}/process", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # Verify preview is base64 image
                preview = result.get('preview', '')
                if preview.startswith('data:image/png;base64,'):
                    log_test(test_name, True, "Preview generated successfully")
                    return True
                else:
                    log_test(test_name, False, "Invalid preview format")
                    return False
            else:
                log_test(test_name, False, result.get('error', 'Unknown error'))
                return False
        else:
            log_test(test_name, False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test(test_name, False, str(e))
        return False

def test_all_presets(filename):
    """Test all processing presets"""
    presets = [
        ('medieval', { 'contrast': 1.4, 'brightness': -5, 'threshold': 120, 'noise': 35, 'blur': 0.8, 'method': 'manuscript' }),
        ('threshold', { 'contrast': 1.6, 'brightness': 0, 'threshold': 90, 'noise': 15, 'blur': 0, 'method': 'threshold' }),
        ('atmospheric', { 'contrast': 1.3, 'brightness': -15, 'threshold': 150, 'noise': 25, 'blur': 2.0, 'method': 'atmospheric' }),
        ('silhouette', { 'contrast': 2.8, 'brightness': 25, 'threshold': 75, 'noise': 8, 'blur': 0, 'method': 'silhouette' }),
        ('ghostly', { 'contrast': 1.2, 'brightness': 35, 'threshold': 190, 'noise': 30, 'blur': 2.5, 'method': 'ghostly' }),
        ('cavernDeep', { 'contrast': 2.2, 'brightness': -40, 'threshold': 85, 'noise': 40, 'blur': 1.0, 'method': 'cavern' }),
        ('frozenWastes', { 'contrast': 2.8, 'brightness': 50, 'threshold': 120, 'noise': 12, 'blur': 0, 'method': 'frozen' }),
        ('darkRitual', { 'contrast': 2.4, 'brightness': -20, 'threshold': 80, 'noise': 50, 'blur': 1.5, 'method': 'ritual' }),
        ('lithographic', { 'contrast': 1.8, 'brightness': 5, 'threshold': 130, 'noise': 20, 'blur': 0.3, 'method': 'lithographic' }),
        ('sepiaNostalgia', { 'contrast': 1.1, 'brightness': 20, 'threshold': 140, 'noise': 18, 'blur': 0.7, 'method': 'sepia' }),
        ('comfyHearth', { 'contrast': 1.0, 'brightness': 15, 'threshold': 160, 'noise': 12, 'blur': 1.2, 'method': 'comfy' }),
        ('forestMystic', { 'contrast': 1.3, 'brightness': -10, 'threshold': 110, 'noise': 28, 'blur': 1.0, 'method': 'forest' })
    ]
    
    all_passed = True
    for preset_name, params in presets:
        params['color_tint'] = 'none'
        params['preserve_aspect_ratio'] = False
        if not test_processing(filename, params, f"Preset: {preset_name}"):
            all_passed = False
        time.sleep(0.1)  # Small delay between requests
    
    return all_passed

def test_color_tints(filename):
    """Test all color tints"""
    tints = ['none', 'sepia', 'sickly_green', 'archaic_grey', 'winter_frost', 
             'comfy_earth', 'blood_ritual', 'parchment_age', 'deep_purple']
    
    params = {
        'contrast': 1.5,
        'brightness': 0,
        'threshold': 128,
        'noise': 20,
        'blur': 0,
        'method': 'custom',
        'preserve_aspect_ratio': False
    }
    
    all_passed = True
    for tint in tints:
        params['color_tint'] = tint
        if not test_processing(filename, params, f"Color Tint: {tint}"):
            all_passed = False
        time.sleep(0.1)
    
    return all_passed

def test_aspect_ratio_preservation(filename):
    """Test aspect ratio preservation feature"""
    params = {
        'contrast': 1.5,
        'brightness': 0,
        'threshold': 128,
        'noise': 20,
        'blur': 0,
        'method': 'custom',
        'color_tint': 'none'
    }
    
    # Test with aspect ratio preserved
    params['preserve_aspect_ratio'] = True
    test1 = test_processing(filename, params, "Aspect Ratio: Preserved")
    
    # Test without aspect ratio preserved
    params['preserve_aspect_ratio'] = False
    test2 = test_processing(filename, params, "Aspect Ratio: Square Crop")
    
    return test1 and test2

def test_concurrent_requests(filename):
    """Test concurrent requests to ensure thread safety"""
    results = []
    threads = []
    
    def process_request(preset_name, aspect_ratio, tint):
        params = {
            'contrast': 1.5,
            'brightness': 0,
            'threshold': 128,
            'noise': 20,
            'blur': 0,
            'method': preset_name,
            'color_tint': tint,
            'preserve_aspect_ratio': aspect_ratio
        }
        success = test_processing(filename, params, f"Concurrent: {preset_name}, AR={aspect_ratio}, Tint={tint}")
        results.append(success)
    
    # Create multiple concurrent requests with different parameters
    test_cases = [
        ('custom', False, 'none'),
        ('manuscript', True, 'sepia'),
        ('threshold', False, 'sickly_green'),
        ('atmospheric', True, 'winter_frost'),
        ('custom', True, 'deep_purple')
    ]
    
    for preset, ar, tint in test_cases:
        thread = threading.Thread(target=process_request, args=(preset, ar, tint))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return all(results)

def test_download_sizes(filename):
    """Test different download sizes"""
    sizes = ['400', '1400', '2000', '3000']
    all_passed = True
    
    for size in sizes:
        try:
            url = f"{BASE_URL}/download/custom/{filename}?tint=none&size={size}&preserve_aspect_ratio=false"
            response = requests.get(url)
            
            if response.status_code == 200:
                # Verify it's a valid PNG
                img = Image.open(io.BytesIO(response.content))
                actual_size = img.size[0]  # Should be square
                if actual_size == int(size):
                    log_test(f"Download Size: {size}x{size}", True, "Size verified")
                else:
                    log_test(f"Download Size: {size}x{size}", False, f"Expected {size}, got {actual_size}")
                    all_passed = False
            else:
                log_test(f"Download Size: {size}x{size}", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            log_test(f"Download Size: {size}x{size}", False, str(e))
            all_passed = False
        
        time.sleep(0.1)
    
    return all_passed

def test_download_with_aspect_ratio(filename):
    """Test download with aspect ratio preserved"""
    try:
        # Process with aspect ratio preserved
        params = {
            'contrast': 1.5,
            'brightness': 0,
            'threshold': 128,
            'noise': 20,
            'blur': 0,
            'method': 'custom',
            'color_tint': 'none',
            'preserve_aspect_ratio': True
        }
        
        # First process the image
        response = requests.post(f"{BASE_URL}/process", json={'filename': filename, **params})
        if response.status_code != 200:
            log_test("Download with Aspect Ratio", False, "Failed to process image")
            return False
        
        # Download with aspect ratio preserved
        url = f"{BASE_URL}/download/custom/{filename}?tint=none&size=400&preserve_aspect_ratio=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Check filename from Content-Disposition header
            content_disp = response.headers.get('Content-Disposition', '')
            
            # Verify it's a valid PNG and check dimensions
            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
            
            # For our 800x600 test image scaled to fit in 400x400, it should be 400x300
            expected_width = 400
            expected_height = 300
            
            if width == expected_width and height == expected_height:
                log_test("Download with Aspect Ratio", True, f"Dimensions: {width}x{height}")
                return True
            else:
                log_test("Download with Aspect Ratio", False, 
                        f"Expected {expected_width}x{expected_height}, got {width}x{height}")
                return False
        else:
            log_test("Download with Aspect Ratio", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Download with Aspect Ratio", False, str(e))
        return False

def test_cleanup(filename):
    """Test file cleanup"""
    try:
        response = requests.post(f"{BASE_URL}/cleanup/{filename}")
        if response.status_code == 200:
            log_test("File Cleanup", True, "Cleanup successful")
            return True
        else:
            log_test("File Cleanup", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("File Cleanup", False, str(e))
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("DUNGEON SYNTH IMAGE PROCESSOR - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Check server health
    if not test_server_health():
        print("\nERROR: Server is not running or not healthy!")
        print("Please start the server with: python app.py")
        return False
    
    # Create test image
    test_image_path = create_test_image()
    print(f"\nCreated test image: {TEST_IMAGE_SIZE[0]}x{TEST_IMAGE_SIZE[1]}")
    
    try:
        # Upload test image
        filename = test_file_upload(test_image_path)
        if not filename:
            print("\nERROR: File upload failed!")
            return False
        
        print("\n--- Testing Processing Features ---")
        
        # Test all presets
        print("\nTesting all presets...")
        test_all_presets(filename)
        
        # Test color tints
        print("\nTesting color tints...")
        test_color_tints(filename)
        
        # Test aspect ratio preservation
        print("\nTesting aspect ratio preservation...")
        test_aspect_ratio_preservation(filename)
        
        # Test concurrent requests
        print("\nTesting concurrent requests (thread safety)...")
        test_concurrent_requests(filename)
        
        # Test download sizes
        print("\nTesting download sizes...")
        test_download_sizes(filename)
        
        # Test download with aspect ratio
        print("\nTesting download with aspect ratio preserved...")
        test_download_with_aspect_ratio(filename)
        
        # Cleanup
        print("\nTesting cleanup...")
        test_cleanup(filename)
        
    finally:
        # Clean up test image
        if os.path.exists(test_image_path):
            os.unlink(test_image_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(TEST_RESULTS)
    passed_tests = sum(1 for r in TEST_RESULTS if r['success'])
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if failed_tests > 0:
        print("\nFailed Tests:")
        for result in TEST_RESULTS:
            if not result['success']:
                print(f"  - {result['test']}: {result['details']}")
    
    return failed_tests == 0

if __name__ == "__main__":
    # Wait a moment for server to be ready if just started
    time.sleep(1)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)