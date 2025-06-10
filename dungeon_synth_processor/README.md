# 🏰 Enhanced Dungeon Synth Image Processor

A sophisticated Python web application for transforming images into authentic dungeon synth album cover aesthetics. Features research-based processing presets, optional color tinting, and full-resolution downloads.

## New Features in v2.0

### 🎨 **Research-Based Authentic Presets**
- **Medieval Manuscript**: Authentic illuminated manuscript aesthetic with aged parchment
- **Clean Threshold**: Binary threshold processing for stark dungeon aesthetics  
- **Atmospheric Depths**: Tonal compression with atmospheric blur for dungeon ambience
- **Lithographic Codex**: Historical printmaking simulation with engraving effects
- **Sepia Nostalgia**: Vintage film degradation with warm sepia tones
- **Comfy Hearth**: Warm domestic atmosphere with gentle earth tones
- **Forest Mystic**: Organic textures with deep green earth tone saturation

### 🌈 **Optional Color Tinting System**
- **9 Authentic Color Palettes**: Based on medieval pigment traditions
- **Professional Blend Modes**: Overlay, multiply, and soft light blending
- **Subgenre-Specific Tints**: Winter frost, comfy earth, blood ritual, and more
- **Real-time Preview**: See color effects instantly while adjusting

### 🔬 **Enhanced Processing Engine**
- **Method-Specific Algorithms**: Each preset uses unique processing optimized for its aesthetic
- **Advanced Contrast Curves**: S-curves and tonal compression for authentic vintage looks
- **Intelligent Grain Systems**: Coarse grain for aged effects, fine grain for modern looks
- **Research-Based Parameters**: All settings derived from dungeon synth visual analysis

## Features

- **12 Authentic Processing Presets**: From medieval manuscripts to crystalline winter landscapes
- **9 Color Tinting Options**: Research-based color palettes for authentic dungeon synth aesthetics
- **Real-time Preview**: Live preview with adjustable parameters and instant color tinting
- **Full Resolution Processing**: Downloads maintain original image quality with exact preview consistency
- **Multiple Input Formats**: Supports JPG, PNG, TIFF, BMP, WebP
- **Local Execution**: No internet connection required, complete privacy
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Quick Start

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 2. Installation

```bash
# Clone or download the project files
# Navigate to the project directory
cd enhanced_dungeon_synth_processor

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
enhanced_dungeon_synth_processor/
├── app.py                 # Flask application with color tinting support
├── image_processor.py     # Enhanced processing engine with research-based methods
├── presets.py            # Authentic presets and color tinting definitions
├── requirements.txt      # Dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Enhanced styling with color tinting UI
│   ├── js/
│   │   └── main.js       # Enhanced frontend with color tinting controls
│   └── uploads/          # Temporary storage
├── templates/
│   └── index.html        # Updated template with new presets and tinting
└── README.md            # This file
```

## Usage Guide

### Basic Workflow
1. **Upload Image**: Click "Upload Image" or drag & drop your photo
2. **Choose Processing**: Click any preset button for instant authentic processing
3. **Color Tinting**: Select from 9 research-based color palettes (optional)
4. **Custom Adjustments**: Use sliders for fine-tuning parameters
5. **Download**: Click download buttons for full-resolution processed images

### Authentic Dungeon Synth Presets

#### **Medieval Manuscript** 📜
- **Aesthetic**: Authentic illuminated manuscript with aged parchment
- **Processing**: Gentle contrast, warm tones, coarse grain texture
- **Best For**: Historical themes, ancient texts, classical dungeon synth

#### **Clean Threshold** 🔳  
- **Aesthetic**: Binary black and white for stark dungeon aesthetics
- **Processing**: Sharp threshold with minimal noise
- **Best For**: Minimalist covers, stark architectural subjects

#### **Atmospheric Depths** 🌫️
- **Aesthetic**: Tonal compression with deep atmospheric blur
- **Processing**: Reduced dynamic range, enhanced atmospheric perspective
- **Best For**: Dungeon ambience, mysterious depths, fog-shrouded landscapes

#### **Lithographic Codex** 🖨️
- **Aesthetic**: Historical printmaking with engraving-style effects
- **Processing**: Medium contrast with cross-hatching simulation
- **Best For**: Ancient texts, historical documents, scholarly aesthetics

#### **Sepia Nostalgia** 📸
- **Aesthetic**: Vintage film degradation with warm sepia tones  
- **Processing**: Lifted shadows, compressed highlights, film grain
- **Best For**: Nostalgic themes, aged photographs, vintage atmosphere

#### **Comfy Hearth** 🏠
- **Aesthetic**: Warm domestic atmosphere with gentle earth tones
- **Processing**: Low contrast, lifted shadows, warm color grading
- **Best For**: Comfy synth, tavern scenes, domestic medieval life

#### **Forest Mystic** 🌲
- **Aesthetic**: Organic textures with deep green earth saturation
- **Processing**: Enhanced midtones, organic grain patterns
- **Best For**: Forest themes, natural environments, woodland mysticism

#### **Silhouette** 👤
- **Processing**: Extreme threshold for stark silhouettes
- **Best For**: Dramatic subjects, architectural forms

#### **Ghostly Apparition** 👻  
- **Processing**: Ethereal blur with lifted shadows
- **Best For**: Supernatural themes, ethereal atmospheres

#### **Cavern Deep** 🕳️
- **Processing**: Deep underground tunnel atmospheres
- **Best For**: Cave systems, underground exploration

#### **Frozen Wastes** ❄️
- **Processing**: Crystalline winter synth with stark minimalism
- **Best For**: Winter landscapes, ice formations

#### **Dark Ritual** 🔮
- **Processing**: Heavy grain with dramatic shadows
- **Best For**: Occult themes, ritual atmospheres

### Color Tinting System

#### **Research-Based Palettes**
All color tints are derived from academic research on medieval pigments and dungeon synth visual analysis:

- **None**: Original monochrome processing
- **Sepia Warmth**: Classic warm brown tones (#8B4513)
- **Sickly Green**: Authentic dungeon synth olive greens (#556B2F)  
- **Archaic Grey**: Medieval stone and parchment greys (#708090)
- **Winter Frost**: Cold crystalline blues (#4682B4)
- **Comfy Earth**: Warm hearth and earth tones (#DEB887)
- **Blood Ritual**: Deep burgundy for occult themes (#800020)
- **Parchment Age**: Aged manuscript yellows (#F0E68C)
- **Deep Purple**: Mystical indigo tones (#4B0082)

#### **Professional Blend Modes**
- **Overlay**: Enhanced contrast and saturation
- **Multiply**: Darker, richer tones  
- **Soft Light**: Gentle, natural color enhancement

## Technical Details

### Enhanced Processing Engine

#### **Method-Specific Algorithms**
Each preset employs unique processing optimized for its aesthetic:

- **S-Curve Contrast**: Gentle enhancement without harsh transitions
- **Tonal Compression**: Atmospheric depth simulation  
- **Crystalline Processing**: Sharp, clean winter aesthetics
- **Manuscript Effects**: Aged parchment simulation
- **Lithographic Simulation**: Historical printmaking techniques

#### **Advanced Grain Systems**
- **Coarse Grain**: Aged effects, manuscript textures (2x pixel grouping)
- **Fine Grain**: Modern, subtle textures (standard pixel noise)
- **Method-Specific Scaling**: Grain adapts to processing method and image size

#### **Professional Color Blending**
- **Overlay Mode**: `result = base < 0.5 ? 2*base*overlay : 1-2*(1-base)*(1-overlay)`
- **Multiply Mode**: `result = base * overlay`  
- **Soft Light Mode**: Complex formula for natural color enhancement

### Parameters

#### **Processing Controls**
- **Contrast**: 0.5 - 3.0 (method-specific optimization)
- **Brightness**: -100 to +100 (preserves detail in shadows/highlights)
- **Threshold**: 0 - 255 (adaptive per processing method)
- **Noise**: 0 - 50 (intelligent scaling based on method)
- **Blur**: 0 - 5 pixels (atmospheric processing)

#### **Color Tinting**
- **Opacity**: 20-35% (method-optimized transparency)
- **Blend Modes**: Overlay, Multiply, Soft Light
- **Color Accuracy**: Hex values derived from historical pigment analysis

### Processing Pipeline

1. **Image Upload & Validation**
2. **EXIF Orientation Correction**
3. **Color Space Normalization** (RGB conversion)
4. **Square Crop Preview Generation** (400x400 for consistency)
5. **Method-Specific Processing Application**
   - Blur filtering (if enabled)
   - Luminosity-based grayscale conversion
   - Brightness adjustment with shadow/highlight preservation
   - Method-specific contrast curves
   - Threshold processing (adaptive per method)
   - Intelligent grain application
6. **Optional Color Tinting** (professional blend modes)
7. **Preview Generation & Caching**
8. **Full-Resolution Processing** (maintains exact preview consistency)

## Advanced Usage

### Custom Processing Workflow
1. Start with any preset as a base
2. Adjust contrast for desired dynamic range
3. Fine-tune brightness for shadow/highlight balance
4. Set threshold based on subject matter
5. Add grain for texture (method-specific scaling)
6. Apply atmospheric blur if needed
7. Select color tinting for mood enhancement

### Color Tinting Best Practices
- **Sepia/Parchment**: Perfect for classical dungeon synth
- **Sickly Green**: Authentic dungeon synth tradition
- **Winter Frost**: Ideal for atmospheric/ambient themes
- **Comfy Earth**: Excellent for tavern/domestic scenes
- **Blood Ritual**: Dramatic enhancement for dark themes

### Performance Optimization
- Preview processing optimized for 400x400 display
- Full-resolution processing uses intelligent upscaling
- Caching system ensures download consistency
- Vectorized operations for images over 1MP

## API Endpoints

### Core Functionality
- `POST /upload` - Image upload with validation
- `POST /process` - Image processing with parameters
- `GET /download/<preset>/<filename>` - Full-resolution download
- `GET /get_presets` - Available processing presets
- `GET /get_color_tints` - Available color tinting options
- `GET /health` - System status and capabilities

### Enhanced Features
- Color tinting parameter support in processing
- Method-specific parameter validation
- Professional blend mode implementation
- Cache management for download consistency

## VSCode Development Setup

### Recommended Extensions
- Python (Microsoft)
- Flask Snippets  
- HTML CSS Support
- Prettier - Code formatter
- Color Highlight (for hex color values)

### Debug Configuration
Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Enhanced Flask App",
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

## Customization Guide

### Adding New Presets
Edit `presets.py` to add authentic processing methods:

```python
'newPreset': {
    'contrast': 1.8,
    'brightness': 5,
    'threshold': 130,
    'noise': 20,
    'blur': 0.5,
    'method': 'custom',  # or new method
    'name': 'New Preset Name',
    'description': 'Description of visual effect'
}
```

### Adding New Color Tints
Add to `COLOR_TINTS` in `presets.py`:

```python
'new_tint': {
    'name': 'New Tint Name',
    'color': '#HexColor',
    'opacity': 0.30,
    'blend_mode': 'overlay'  # or 'multiply', 'soft_light'
}
```

### Custom Processing Methods
Implement in `image_processor.py`:

```python
def _apply_custom_method_effect(self, gray, threshold):
    """Custom processing implementation"""
    # Your processing logic here
    return processed_gray
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Application automatically finds free port
# Or manually specify in app.py
app.run(debug=True, host='127.0.0.1', port=5001)
```

**Missing Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Color Tinting Not Working**
- Check browser JavaScript console for errors
- Verify color tint API endpoint: `/get_color_tints`
- Ensure PIL/Pillow supports blend operations

**Processing Performance Issues**
- Large images (>10MB) require additional processing time
- Preview generation is optimized for speed
- Full-resolution processing maintains quality over speed

### Performance Optimization

**For Large Image Workflows:**
1. Use preview for parameter adjustment
2. Apply full-resolution processing only for final output
3. Consider image resizing for very large files (>20MB)
4. Processing time scales with image resolution

**Memory Management:**
- Application includes automatic cleanup systems
- Cache management prevents memory overflow
- Temporary files are cleaned on application shutdown

## Dependencies

- **Flask**: Web framework
- **Pillow**: Enhanced image processing with blend mode support
- **NumPy**: Vectorized numerical operations for performance
- **OpenCV**: Advanced image processing algorithms
- **Werkzeug**: WSGI utilities and security

## Research Foundation

This enhanced version is based on comprehensive research of dungeon synth visual aesthetics, including:

- Analysis of historical medieval pigments and color traditions
- Study of dungeon synth album cover visual patterns
- Academic research on color psychology and music visualization
- Professional image processing techniques for vintage effects
- Medieval manuscript and lithographic printing methods

## License

This project is open source under MIT License. Feel free to modify, enhance, and redistribute.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow established code patterns for presets and processing methods
4. Add comprehensive tests for new functionality
5. Update documentation for new features
6. Submit pull request with detailed description

## Changelog

### v2.0.0 - Research-Based Enhancement
- **BREAKING**: Replaced redundant "High Contrast Threshold" with authentic "Medieval Manuscript"
- **NEW**: 4 research-based authentic presets (Lithographic, Sepia, Comfy, Forest)
- **NEW**: Complete color tinting system with 9 medieval-inspired palettes
- **NEW**: Method-specific processing algorithms based on dungeon synth research
- **NEW**: Professional blend modes (Overlay, Multiply, Soft Light)
- **ENHANCED**: Advanced grain systems with method-specific characteristics
- **ENHANCED**: Intelligent contrast curves (S-curves, tonal compression)
- **ENHANCED**: Responsive UI with improved preset organization
- **ENHANCED**: Complete API documentation and development tools

### v1.0.0 - Initial Release
- Basic image processing with 9 presets
- Clean interface with real-time preview
- Full-resolution download capability
- Support for standard image formats

## Support

For issues, feature requests, or questions:
1. Check the troubleshooting section above
2. Review the comprehensive documentation
3. Check existing GitHub issues
4. Create detailed issue report with:
   - Operating system and Python version
   - Exact error messages
   - Steps to reproduce
   - Sample images (if relevant)

**Happy dungeon synth album cover creation! 🏰**