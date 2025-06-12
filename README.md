# 🏰 Dungeon Synth Image Processor

A local Python web application for transforming images into dungeon synth album cover aesthetics. Features high-contrast black and white processing, multiple presets, and full-resolution downloads.
Made with Claude (Anthropic).

## Features

- **Multiple Processing Presets**: High Contrast, Atmospheric, Silhouette, Medieval Manuscript, Ghostly Apparition
- **Real-time Preview**: Live preview with adjustable parameters
- **Full Resolution Processing**: Downloads maintain original image quality
- **Multiple Input Formats**: Supports JPG, PNG, TIFF, BMP, WebP
- **Local Execution**: No internet connection required
- **Responsive Design**: Works on desktop and mobile

## Quick Start

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 2. Installation

```bash
# Clone or download the project files
# Navigate to the project directory
cd dungeon_synth_processor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open in Browser
Navigate to: `http://localhost:5000`

## Project Structure

```
dungeon_synth_processor/
├── app.py                 # Flask application
├── image_processor.py     # Core processing logic
├── presets.py            # Processing presets
├── requirements.txt      # Dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   ├── js/
│   │   └── main.js       # Frontend JavaScript
│   └── uploads/          # Temporary storage
├── templates/
│   └── index.html        # Main template
└── README.md            # This file
```

## Usage

1. **Upload Image**: Click "Upload Image" and select your photo
2. **Choose Preset**: Click any preset button for instant processing
3. **Custom Adjustments**: Use sliders for fine-tuning
4. **Download**: Click download buttons for full-resolution images

## Supported Image Formats

- **JPEG/JPG**: Standard photo format
- **PNG**: Lossless with transparency support
- **TIFF/TIF**: High-quality format
- **BMP**: Bitmap format
- **WebP**: Modern web format

## Processing Methods

### High Contrast Threshold
- Pure black & white conversion
- Dramatic contrast enhancement
- Perfect for stark silhouettes

### Atmospheric
- Subtle blur effect
- Enhanced contrast with detail preservation
- Mysterious, ethereal atmosphere

### Silhouette
- Extreme threshold processing
- Creates stark silhouettes
- Light backgrounds with dark subjects

### Medieval Manuscript
- Aged parchment aesthetic
- Heavy grain texture
- Historical, ancient feel

### Ghostly Apparition
- Ethereal blur processing
- Bright midtones
- Supernatural atmosphere

### Cavern Deep
- Deep shadows and mysterious tunnels
- Enhanced darkness for underground aesthetics

### Frozen Wastes
- Stark, minimalist winter landscapes
- High contrast for icy effects

### Dark Ritual
- Dramatic contrast for ritual atmospheres
- Heavy grain and atmospheric processing

### Custom Processing
- Adjustable contrast, brightness, threshold
- Variable noise/grain levels
- Customizable blur effects

## Technical Details

### Parameters
- **Contrast**: 0.5 - 3.0 (1.5 default)
- **Brightness**: -100 to +100 (0 default)
- **Threshold**: 0 - 255 (128 default)
- **Noise**: 0 - 50 (20 default)
- **Blur**: 0 - 5 pixels (0 default)

### Processing Pipeline
1. Image upload and validation
2. Square crop for preview (maintains aspect ratio)
3. Blur application (if enabled)
4. Grayscale conversion (luminosity method)
5. Brightness adjustment
6. Contrast enhancement
7. Method-specific processing
8. Noise/grain addition
9. Final output generation

## VSCode Setup

### Recommended Extensions
- Python (Microsoft)
- Flask Snippets
- HTML CSS Support
- Prettier - Code formatter

### Debug Configuration
Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "app.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

## Customization

### Adding New Presets
Edit `presets.py` to add new processing methods:

```python
'newPreset': {
    'contrast': 2.0,
    'brightness': 5,
    'threshold': 110,
    'noise': 15,
    'blur': 1.0,
    'method': 'custom',
    'name': 'New Preset',
    'description': 'Description of effect'
}
```

### Custom Processing Methods
Add new methods in `image_processor.py`:

```python
def _apply_method_processing(self, gray, threshold, method):
    if method == 'your_method':
        # Your custom processing logic
        return processed_gray
    # ... existing methods
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change port in app.py
app.run(debug=True, host='localhost', port=5001)
```

**Missing Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Permission Errors**
```bash
# Ensure upload directory is writable
chmod 755 static/uploads
```

**Large Image Processing**
- Images over 10MB may take longer to process
- For very large images, consider resizing before upload
- Processing time scales with image resolution

### Performance Optimization

For better performance with large images:
1. The app automatically uses vectorized processing for images > 1MP
2. Preview generation is optimized for 400x400 display
3. Full-resolution processing maintains original quality
4. Images are automatically converted to RGB during processing

## Dependencies

- **Flask**: Web framework
- **Pillow**: Image processing
- **NumPy**: Numerical operations
- **OpenCV**: Advanced image processing
- **Werkzeug**: WSGI utilities

## License

This project is open source. Feel free to modify and redistribute.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue with detailed description

## Changelog

### v1.0.0
- Clean image processing for dungeon synth aesthetics
- Support for JPG, PNG, TIFF, BMP, WebP formats
- Multiple processing presets
- Real-time preview and custom adjustments
- Full-resolution downloads
