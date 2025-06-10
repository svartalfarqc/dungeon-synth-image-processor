# presets.py
"""
Authentic dungeon synth presets based on visual aesthetic research
"""

PROCESSING_PRESETS = {
    # REDESIGNED: Fixed redundancy between high contrast and threshold
    'medieval': {
        'contrast': 1.4,
        'brightness': -5,
        'threshold': 120,
        'noise': 35,
        'blur': 0.8,
        'method': 'manuscript',
        'name': 'Medieval Manuscript',
        'description': 'Authentic medieval illuminated manuscript aesthetic with aged parchment'
    },
    
    'threshold': {
        'contrast': 1.6,
        'brightness': 0,
        'threshold': 90,
        'noise': 15,
        'blur': 0,
        'method': 'threshold',
        'name': 'Clean Threshold',
        'description': 'Clean binary threshold processing for stark dungeon aesthetics'
    },
    
    # UPDATED: More atmospheric processing
    'atmospheric': {
        'contrast': 1.3,
        'brightness': -15,
        'threshold': 150,
        'noise': 25,
        'blur': 2.0,
        'method': 'atmospheric',
        'name': 'Atmospheric Depths',
        'description': 'Tonal compression with atmospheric blur for dungeon ambience'
    },
    
    'silhouette': {
        'contrast': 2.8,
        'brightness': 25,
        'threshold': 75,
        'noise': 8,
        'blur': 0,
        'method': 'silhouette',
        'name': 'Silhouette',
        'description': 'Stark silhouettes against light backgrounds'
    },
    
    'ghostly': {
        'contrast': 1.2,
        'brightness': 35,
        'threshold': 190,
        'noise': 30,
        'blur': 2.5,
        'method': 'ghostly',
        'name': 'Ghostly Apparition',
        'description': 'Ethereal blur with lifted shadows for supernatural atmosphere'
    },
    
    # EXISTING BUT REFINED
    'cavernDeep': {
        'contrast': 2.2,
        'brightness': -40,
        'threshold': 85,
        'noise': 40,
        'blur': 1.0,
        'method': 'cavern',
        'name': 'Cavern Deep',
        'description': 'Deep underground shadows with mysterious tunnel atmospheres'
    },
    
    'frozenWastes': {
        'contrast': 2.8,
        'brightness': 50,
        'threshold': 120,
        'noise': 12,
        'blur': 0,
        'method': 'frozen',
        'name': 'Frozen Wastes',
        'description': 'Crystalline winter synth processing with stark minimalism'
    },
    
    'darkRitual': {
        'contrast': 2.4,
        'brightness': -20,
        'threshold': 80,
        'noise': 50,
        'blur': 1.5,
        'method': 'ritual',
        'name': 'Dark Ritual',
        'description': 'Heavy grain with dramatic shadows for occult atmospheres'
    },
    
    # NEW RESEARCH-BASED PRESETS
    'lithographic': {
        'contrast': 1.8,
        'brightness': 5,
        'threshold': 130,
        'noise': 20,
        'blur': 0.3,
        'method': 'lithographic',
        'name': 'Lithographic Codex',
        'description': 'Historical printmaking simulation with engraving-style effects'
    },
    
    'sepiaNostalgia': {
        'contrast': 1.1,
        'brightness': 20,
        'threshold': 140,
        'noise': 18,
        'blur': 0.7,
        'method': 'sepia',
        'name': 'Sepia Nostalgia',
        'description': 'Vintage film degradation with warm sepia tones'
    },
    
    'comfyHearth': {
        'contrast': 1.0,
        'brightness': 15,
        'threshold': 160,
        'noise': 12,
        'blur': 1.2,
        'method': 'comfy',
        'name': 'Comfy Hearth',
        'description': 'Warm domestic atmosphere with gentle earth tones'
    },
    
    'forestMystic': {
        'contrast': 1.3,
        'brightness': -10,
        'threshold': 110,
        'noise': 28,
        'blur': 1.0,
        'method': 'forest',
        'name': 'Forest Mystic',
        'description': 'Organic textures with deep green earth tone saturation'
    }
}

# Color tinting palettes based on research
COLOR_TINTS = {
    'none': {
        'name': 'No Tinting',
        'color': None,
        'opacity': 0.0,
        'blend_mode': 'normal'
    },
    'sepia': {
        'name': 'Sepia Warmth',
        'color': '#8B4513',  # Saddle brown
        'opacity': 0.35,
        'blend_mode': 'overlay'
    },
    'sickly_green': {
        'name': 'Sickly Green',
        'color': '#556B2F',  # Dark olive green
        'opacity': 0.30,
        'blend_mode': 'multiply'
    },
    'archaic_grey': {
        'name': 'Archaic Grey',
        'color': '#708090',  # Slate grey
        'opacity': 0.25,
        'blend_mode': 'overlay'
    },
    'winter_frost': {
        'name': 'Winter Frost',
        'color': '#4682B4',  # Steel blue
        'opacity': 0.25,
        'blend_mode': 'soft_light'
    },
    'comfy_earth': {
        'name': 'Comfy Earth',
        'color': '#DEB887',  # Burlywood
        'opacity': 0.30,
        'blend_mode': 'soft_light'
    },
    'blood_ritual': {
        'name': 'Blood Ritual',
        'color': '#800020',  # Burgundy
        'opacity': 0.20,
        'blend_mode': 'multiply'
    },
    'parchment_age': {
        'name': 'Parchment Age',
        'color': '#F0E68C',  # Khaki
        'opacity': 0.25,
        'blend_mode': 'overlay'
    },
    'deep_purple': {
        'name': 'Deep Purple',
        'color': '#4B0082',  # Indigo
        'opacity': 0.25,
        'blend_mode': 'multiply'
    }
}

# Default parameters for custom processing
DEFAULT_PARAMS = {
    'contrast': 1.5,
    'brightness': 0,
    'threshold': 128,
    'noise': 20,
    'blur': 0,
    'method': 'custom',
    'color_tint': 'none'
}

def get_preset(name):
    """Get preset by name with fallback to default"""
    preset = PROCESSING_PRESETS.get(name, DEFAULT_PARAMS.copy())
    # Ensure color_tint is set
    if 'color_tint' not in preset:
        preset['color_tint'] = 'none'
    return preset

def get_color_tint(name):
    """Get color tint by name"""
    return COLOR_TINTS.get(name, COLOR_TINTS['none'])

def list_presets():
    """Return list of available preset names"""
    return list(PROCESSING_PRESETS.keys())

def list_color_tints():
    """Return list of available color tint names"""
    return list(COLOR_TINTS.keys())

def get_preset_info():
    """Return preset information for UI"""
    return {
        name: {
            'name': preset['name'],
            'description': preset['description']
        }
        for name, preset in PROCESSING_PRESETS.items()
    }

def get_color_tint_info():
    """Return color tint information for UI"""
    return {
        name: {
            'name': tint['name'],
            'color': tint['color']
        }
        for name, tint in COLOR_TINTS.items()
    }