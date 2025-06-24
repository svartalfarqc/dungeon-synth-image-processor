# 🏰 Dungeon Synth Image Processor

Transform any image into authentic dungeon synth album cover aesthetics with this powerful local web application. Features 12 unique presets, 9 color tinting options, and full customization controls.

![Dungeon Synth Processor Banner](https://github.com/yourusername/dungeon-synth-processor/assets/banner.png)

## ✨ Key Features

- **12 Authentic Presets** - From Medieval Manuscript to Forest Mystic
- **9 Color Tinting Palettes** - Add atmospheric color overlays to any processed image
- **Live Preview** - See changes instantly as you adjust parameters
- **Multiple Export Sizes** - 400x400 to 3000x3000 resolution
- **Batch Processing** - Generate all variations with one click
- **No Internet Required** - Runs entirely on your local machine

## 🚀 Quick Start

### Installation (3 minutes)

1. **Install Python** (3.7 or higher) - [Download Python](https://www.python.org/downloads/)

2. **Download & Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/dungeon-synth-processor.git
cd dungeon-synth-processor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python app.py
```

4. **Open in Browser**
Navigate to: http://localhost:5000

## 🎨 User Interface Guide

### Main Interface
![Main Interface](https://github.com/yourusername/dungeon-synth-processor/assets/main-interface.png)

The interface is divided into four main sections:

### 1. Upload Section
- Drag & drop or click to upload images
- Supports: JPG, PNG, TIFF, BMP, WebP
- Maximum file size: 32MB

### 2. Preset Selection
![Preset Buttons](https://github.com/yourusername/dungeon-synth-processor/assets/presets.png)

Click any preset button to instantly apply that aesthetic:

| Preset | Icon | Description |
|--------|------|-------------|
| **Medieval Manuscript** | 📜 | Aged parchment with authentic manuscript textures |
| **Clean Threshold** | 🔳 | Pure black & white binary processing |
| **Atmospheric Depths** | 🌫️ | Misty, ethereal dungeon atmospheres |
| **Silhouette** | 👤 | Stark silhouettes on light backgrounds |
| **Ghostly Apparition** | 👻 | Supernatural blur with lifted shadows |
| **Cavern Deep** | 🕳️ | Deep underground tunnel aesthetics |
| **Frozen Wastes** | ❄️ | Crystalline winter synth processing |
| **Dark Ritual** | 🔮 | Heavy grain for occult atmospheres |
| **Lithographic Codex** | 🖨️ | Historical printmaking simulation |
| **Sepia Nostalgia** | 📸 | Vintage film degradation effects |
| **Comfy Hearth** | 🏠 | Warm, inviting domestic atmospheres |
| **Forest Mystic** | 🌲 | Organic textures with natural depth |

### 3. Color Tinting Palette
![Color Tinting](https://github.com/yourusername/dungeon-synth-processor/assets/color-tinting.png)

Apply atmospheric color overlays to any processed image:

- **None** - Pure black & white processing
- **Sepia Warmth** - Classic aged photograph tones
- **Sickly Green** - Eerie, supernatural atmosphere
- **Archaic Grey** - Ancient stone textures
- **Winter Frost** - Cold, crystalline blues
- **Comfy Earth** - Warm, natural browns
- **Blood Ritual** - Deep, ominous reds
- **Parchment Age** - Yellowed manuscript tones
- **Deep Purple** - Mystical, arcane atmosphere

### 4. Custom Processing Controls
![Custom Controls](https://github.com/yourusername/dungeon-synth-processor/assets/custom-controls.png)

Fine-tune your processing with live preview:

| Control | Range | Description |
|---------|-------|-------------|
| **Contrast** | 0.5 - 3.0 | Intensity of light/dark separation |
| **Brightness** | -100 to +100 | Overall image lightness |
| **Threshold** | 0 - 255 | Binary conversion point |
| **Grain/Noise** | 0 - 50 | Texture and grain amount |
| **Atmospheric Blur** | 0 - 5 | Ethereal fog effect |

### 5. Download Options
![Download Options](https://github.com/yourusername/dungeon-synth-processor/assets/download-options.png)

Select your output size:
- **400x400** - Default web size
- **1400x1400** - Bandcamp standard
- **2000x2000** - High quality
- **3000x3000** - Ultra HD

## 📖 Workflow Examples

### Basic Workflow
1. Upload your image
2. Click a preset (e.g., "Medieval Manuscript")
3. Select a color tint (e.g., "Parchment Age")
4. Download your processed image

### Advanced Workflow
1. Upload your image
2. Click "Generate All Variations" to see all presets
3. Select your favorite preset
4. Fine-tune with custom controls
5. Apply color tinting
6. Choose output size
7. Download final image

### Batch Processing
1. Upload your image
2. Click "Generate All Variations"
3. Download each variation individually
4. Perfect for comparing different aesthetics

## 🔧 Technical Details

### Processing Pipeline
```
Input Image → Square Crop → Blur (optional) → Grayscale Conversion
→ Brightness Adjustment → Contrast Enhancement → Method Processing
→ Noise Addition → Color Tinting → Output
```

### Processing Methods

Each preset uses a unique processing algorithm:

- **Threshold Methods**: Binary conversion at specified levels
- **Atmospheric Methods**: Tonal compression with blur
- **Manuscript Methods**: Aged texture simulation
- **Crystalline Methods**: Sharp contrast with minimal grain

### Color Tinting System

- **Blend Modes**: Overlay, Multiply, Soft Light
- **Opacity Control**: 20-35% depending on tint
- **Non-destructive**: Applied after main processing

### Performance Optimization

- Vectorized NumPy operations for images >1MP
- Cached preview generation
- Separate preview (400x400) and export pipelines
- Automatic EXIF orientation correction

## 💾 File Management

### Supported Formats
| Format | Extension | Notes |
|--------|-----------|-------|
| JPEG | .jpg, .jpeg | Most common format |
| PNG | .png | Lossless, supports transparency |
| TIFF | .tif, .tiff | Professional quality |
| BMP | .bmp | Uncompressed bitmap |
| WebP | .webp | Modern web format |

### File Size Limits
- Maximum upload: 32MB
- Maximum dimensions: 20,000 x 20,000 pixels
- Recommended: Under 10MB for best performance

## 🛠️ Customization

### Adding Custom Presets

Edit `presets.py` to add your own:

```python
'your_preset': {
    'contrast': 1.5,
    'brightness': 0,
    'threshold': 128,
    'noise': 20,
    'blur': 1.0,
    'method': 'custom',
    'name': 'Your Preset Name',
    'description': 'Description of the effect'
}
```

### Creating Custom Color Tints

Add to `COLOR_TINTS` in `presets.py`:

```python
'custom_tint': {
    'name': 'Custom Tint',
    'color': '#hexcode',
    'opacity': 0.3,
    'blend_mode': 'overlay'  # or 'multiply', 'soft_light'
}
```

## 🐛 Troubleshooting

### Common Issues

**"Port 5000 already in use"**
```bash
# The app will automatically find a free port
# Or manually specify: python app.py --port 5001
```

**"Module not found" errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Large images processing slowly**
- Images over 10MB may take longer
- Consider resizing before upload
- Processing is optimized for <5000x5000

**Browser compatibility**
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Limited to smaller images

## 🎯 Tips & Best Practices

### For Best Results

1. **Source Images**
   - High contrast subjects work best
   - Clear foreground/background separation
   - Avoid overly busy compositions

2. **Preset Selection**
   - Medieval/Lithographic: Best for text and symbols
   - Atmospheric/Ghostly: Great for landscapes
   - Silhouette/Threshold: Perfect for stark imagery
   - Forest/Comfy: Ideal for organic subjects

3. **Color Tinting**
   - Apply after finding your ideal black & white processing
   - Sepia/Parchment: Historical feel
   - Green/Purple: Supernatural atmosphere
   - Grey/Frost: Cold, distant moods

4. **Export Sizes**
   - 400x400: Web previews, social media
   - 1400x1400: Bandcamp, streaming platforms
   - 2000x2000+: Physical media, prints

## 📱 Mobile Usage

The interface is fully responsive:
- Upload via camera or gallery
- All controls accessible
- Touch-friendly sliders
- Optimized for portrait/landscape

## 🔒 Privacy & Security

- **100% Local Processing** - No images uploaded to servers
- **No Data Collection** - Complete privacy
- **Temporary Files** - Auto-cleaned on exit
- **Open Source** - Verify the code yourself

## 📄 License

Open source - free to use and modify.

## 🙏 Credits
Luc Mercier
Created with Claude (Anthropic) for the dungeon synth community.

---
