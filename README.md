# 🏰 Dungeon Synth Image Processor

Transform ordinary images into authentic dungeon synth album cover aesthetics. This local web application provides 12 carefully crafted presets, 9 atmospheric color tints, aspect ratio preservation options, and precise manual controls for creating evocative imagery.

## Features

- **12 Authentic Presets** - From ancient manuscript textures to crystalline winter processing
- **9 Atmospheric Color Tints** - Deep earth tones, archaic greys, and ritual bloods
- **Aspect Ratio Preservation** - Keep original image proportions or crop to square
- **Real-time Preview** - Witness transformations as parameters shift
- **Automatic Processing** - All variations generated instantly on upload
- **Multiple Export Resolutions** - 400x400 to 3000x3000 pixels
- **Smart Regeneration** - Updates all previews when settings change
- **Complete Privacy** - All processing occurs locally on your machine

## Installation

### Requirements
- Python 3.7 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/dungeon-synth-processor.git
cd dungeon-synth-processor

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Launch
```bash
python app.py
```

Navigate to: http://localhost:5000

## Interface Overview

![Main Interface](screenshots/main-interface.png)

The application is organized into five primary sections:

### Upload Section
- Supports JPG, PNG, TIFF, BMP, WebP formats
- Maximum file size: 32MB
- Drag and drop functionality included

### Preset Collection

![Preset Gallery](screenshots/preset-gallery.png)

| Preset | Description |
|--------|-------------|
| **Medieval Manuscript** | Aged parchment with authentic manuscript textures |
| **Clean Threshold** | Pure binary black and white conversion |
| **Atmospheric Depths** | Misty, ethereal processing for otherworldly atmospheres |
| **Silhouette** | Stark forms against pale backgrounds |
| **Ghostly Apparition** | Supernatural blur with lifted shadows |
| **Cavern Deep** | Deep underground tunnel aesthetics |
| **Frozen Wastes** | Crystalline winter processing with minimal grain |
| **Dark Ritual** | Heavy grain for occult atmospheres |
| **Lithographic Codex** | Historical printmaking simulation |
| **Sepia Nostalgia** | Vintage film degradation effects |
| **Comfy Hearth** | Warm, subdued domestic atmospheres |
| **Forest Mystic** | Organic textures with natural depth |

### Color Tinting Palette

![Color Tinting](screenshots/color-tinting.png)

Apply subtle atmospheric overlays to processed images:

- **None** - Pure monochromatic processing
- **Sepia Warmth** - Aged photograph tones
- **Sickly Green** - Eerie, supernatural atmosphere
- **Archaic Grey** - Ancient stone textures
- **Winter Frost** - Cold, crystalline blues
- **Comfy Earth** - Warm, natural browns
- **Blood Ritual** - Deep, ominous reds
- **Parchment Age** - Yellowed manuscript tones
- **Deep Purple** - Mystical, arcane atmosphere

### Aspect Ratio Options

![Aspect Ratio Toggle](screenshots/aspect-ratio-toggle.png)

**Keep Original Shape (Don't Crop to Square)**
- When enabled: Preserves the original image proportions during processing
- When disabled: Crops images to perfect squares (default behavior)
- Preview adapts in real-time to show the effect
- Download sizes respect the chosen aspect ratio setting

This feature is particularly useful for:
- Maintaining cinematic widescreen compositions
- Preserving portrait-oriented artwork
- Working with banner or header images
- Creating non-standard album cover formats

### Manual Controls

| Control | Range | Effect |
|---------|-------|--------|
| **Contrast** | 0.5 - 3.0 | Light and shadow separation intensity |
| **Brightness** | -100 to +100 | Overall luminosity adjustment |
| **Threshold** | 0 - 255 | Binary conversion boundary |
| **Grain/Noise** | 0 - 50 | Texture and organic grain |
| **Atmospheric Blur** | 0 - 5 | Ethereal fog effect |

### Export Options

![Download Options](screenshots/download-options.png)

- **400x400** - Standard web format
- **1400x1400** - Bandcamp standard
- **2000x2000** - High resolution
- **3000x3000** - Archival quality

When "Keep Original Shape" is enabled, the download maintains the aspect ratio within the selected size constraints.

## Usage Workflows

### Basic Processing
1. Upload source image (all variations generated automatically)
2. Select desired preset to view in detail
3. Apply color tinting if desired
4. Download processed result

### Advanced Processing
1. Upload source image (all variations generated automatically)
2. Toggle "Keep Original Shape" if desired
3. Select preferred aesthetic from generated previews
4. Fine-tune using manual controls
5. Apply atmospheric color tinting
6. Export at desired resolution

### Batch Generation
All preset variations are automatically generated when you:
- Upload a new image
- Change the aspect ratio preference
- Select a different color tint

## Technical Implementation

### Processing Pipeline
```
Input → Orientation Fix → Aspect Decision → Blur (optional) → Grayscale Conversion
→ Brightness → Contrast → Method Processing → Noise → Color Tint → Output
```

### Processing Methods
- **Threshold Methods**: Binary conversion at specified levels
- **Atmospheric Methods**: Tonal compression with blur
- **Manuscript Methods**: Aged texture simulation
- **Crystalline Methods**: Sharp contrast with minimal grain

### Color Tinting System
- **Blend Modes**: Overlay, Multiply, Soft Light
- **Opacity Range**: 20-35% depending on tint
- **Non-destructive**: Applied after primary processing

### Aspect Ratio Preservation
- **Square Crop Mode**: Centers and crops to largest square
- **Preserve Mode**: Maintains original proportions
- **Preview System**: Shows letterboxed preview for non-square ratios
- **Export System**: Produces files at actual processed dimensions

## File Specifications

### Supported Formats
| Format | Extensions | Notes |
|--------|------------|-------|
| JPEG | .jpg, .jpeg | Standard format |
| PNG | .png | Lossless with transparency support |
| TIFF | .tif, .tiff | Professional quality |
| BMP | .bmp | Uncompressed bitmap |
| WebP | .webp | Modern web format |

### Limitations
- Maximum upload: 32MB
- Maximum dimensions: 20,000 x 20,000 pixels
- Optimal performance: Under 10MB

## Customization

### Adding Custom Presets

To add a new preset, modify `presets.py`. Here's a complete working example that creates a "Gothic Cathedral" preset with stained glass window effects:

```python
# In presets.py, add to PROCESSING_PRESETS dictionary:

'gothicCathedral': {
    'contrast': 2.5,        # High contrast for dramatic shadows
    'brightness': -25,      # Darker overall tone
    'threshold': 95,        # Lower threshold for more blacks
    'noise': 15,           # Moderate grain for texture
    'blur': 0.5,           # Slight blur for mystical effect
    'method': 'gothic',     # Custom processing method
    'name': 'Gothic Cathedral',
    'description': 'Deep shadows with stained glass luminosity'
}
```

Then implement the processing method in `image_processor.py`:

```python
# In _apply_dungeon_synth_processing method, add:

elif method == 'gothic':
    # Gothic cathedral effect - deep shadows with bright highlights
    gray = np.where(gray > threshold + 50, 
                   np.minimum(255, gray * 1.4),  # Bright areas glow
                   np.where(gray < threshold - 30, 
                           0,                     # Deep blacks
                           gray * 0.6))           # Midtones compressed
```

Finally, update the UI in `main.js`:

```javascript
// Add to the presets object in applyPreset function:
'gothicCathedral': { 
    contrast: 2.5, 
    brightness: -25, 
    threshold: 95, 
    noise: 15, 
    blur: 0.5, 
    method: 'gothic' 
}

// Add to the imageMap object:
'gothicCathedral': 'gothicCathedralImage'
```

And add the HTML in `index.html`:

```html
<!-- Add to preset buttons grid -->
<button onclick="applyPreset('gothicCathedral')">⛪ Gothic Cathedral</button>

<!-- Add to image grid -->
<div class="image-container">
    <h3>Gothic Cathedral</h3>
    <div class="image-wrapper">
        <img id="gothicCathedralImage" class="preview-image" style="display: none;">
        <div class="processing-placeholder">
            <div class="placeholder-icon">⛪</div>
            <p>Processing preview will appear here</p>
        </div>
    </div>
    <button class="download-btn" onclick="downloadProcessed('gothicCathedral')" disabled>Download</button>
    <div class="effect-info">Deep shadows with stained glass luminosity</div>
</div>
```

### Creating Color Tints

Add to `COLOR_TINTS` in `presets.py`:

```python
'moonlight': {
    'name': 'Moonlight Silver',
    'color': '#C0C0C0',  # Silver
    'opacity': 0.20,
    'blend_mode': 'soft_light'
}
```

## Troubleshooting

### Common Issues

**Port Conflicts**
```bash
# Application automatically finds available port
# Manual specification: python app.py --port 5001
```

**Missing Dependencies**
```bash
# Ensure virtual environment is active
# Reinstall: pip install -r requirements.txt
```

**Performance with Large Images**
- Files over 10MB require longer processing time
- Consider resizing before upload for optimal performance
- Processing optimized for images under 5000x5000 pixels

**Aspect Ratio Preview Issues**
- Non-square images show letterboxed in preview
- Actual downloads maintain true dimensions
- Preview always fits within 400x400 container

### Browser Compatibility
- Chrome/Edge: Full functionality
- Firefox: Full functionality
- Safari: Full functionality
- Mobile browsers: Limited to smaller file sizes

## Recommendations

### Source Material
- High contrast subjects yield optimal results
- Clear foreground/background separation enhances processing
- Avoid overly complex compositions

### Preset Selection
- Medieval/Lithographic: Ideal for text and symbolic imagery
- Atmospheric/Ghostly: Suited for landscapes and ambient scenes
- Silhouette/Threshold: Perfect for stark, dramatic imagery
- Forest/Comfy: Best for organic and natural subjects

### Aspect Ratio Considerations
- **Square Crop**: Traditional album covers, social media posts
- **Preserve Ratio**: Banners, wallpapers, cinematic compositions
- **Widescreen Sources**: Enable preservation for panoramic effects
- **Portrait Sources**: Maintain height for dramatic vertical compositions

### Color Application
- Apply tinting after achieving desired monochromatic processing
- Sepia/Parchment: Historical and aged aesthetics
- Green/Purple: Supernatural and otherworldly moods
- Grey/Frost: Cold, distant atmospheres

### Export Guidelines
- 400x400: Web use and social media
- 1400x1400: Music streaming platforms
- 2000x2000+: Physical media and high-quality prints
- Aspect preserved exports: Digital displays and banners

## Testing

The project includes comprehensive test suites:

```bash
# Run all tests
python test_app.py

# Test aspect ratio functionality specifically
python test_aspect_ratio.py
```

## Privacy and Security

- **Local Processing Only** - No external server communication
- **No Data Collection** - Complete user privacy
- **Automatic Cleanup** - Temporary files removed on exit
- **Open Source** - All code available for inspection

## License

Open source software - free for use and modification.

## Credits
Luc Mercier  
Developed with Claude (Anthropic)

---