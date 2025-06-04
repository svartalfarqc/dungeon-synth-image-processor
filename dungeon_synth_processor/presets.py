# presets.py
"""
Clean dungeon synth presets focused on effective black & white processing
"""

PROCESSING_PRESETS = {
    # Original 6 presets (preserved exactly)
    'highContrast': {
        'contrast': 2.5,
        'brightness': 10,
        'threshold': 100,
        'noise': 25,
        'blur': 0,
        'method': 'threshold',
        'name': 'High Contrast Threshold',
        'description': 'Pure black & white with dramatic contrast'
    },
    
    'threshold': {
        'contrast': 1.8,
        'brightness': 0,
        'threshold': 80,
        'noise': 15,
        'blur': 0,
        'method': 'threshold',
        'name': 'Threshold',
        'description': 'Clean threshold processing'
    },
    
    'atmospheric': {
        'contrast': 1.6,
        'brightness': -10,
        'threshold': 140,
        'noise': 20,
        'blur': 1.5,
        'method': 'atmospheric',
        'name': 'Atmospheric',
        'description': 'Subtle blur with enhanced contrast'
    },
    
    'silhouette': {
        'contrast': 3,
        'brightness': 20,
        'threshold': 70,
        'noise': 10,
        'blur': 0,
        'method': 'silhouette',
        'name': 'Silhouette',
        'description': 'Stark silhouettes against light background'
    },
    
    'manuscript': {
        'contrast': 2,
        'brightness': 15,
        'threshold': 120,
        'noise': 40,
        'blur': 0.5,
        'method': 'manuscript',
        'name': 'Medieval Manuscript',
        'description': 'Aged parchment effect with heavy grain'
    },
    
    'ghostly': {
        'contrast': 1.3,
        'brightness': 30,
        'threshold': 180,
        'noise': 30,
        'blur': 2,
        'method': 'ghostly',
        'name': 'Ghostly Apparition',
        'description': 'Ethereal blur with bright midtones'
    },
    
    # 3 NEW DUNGEON SYNTH PRESETS (inspired by your examples)
    'cavernDeep': {
        'contrast': 2.8,
        'brightness': -30,
        'threshold': 90,
        'noise': 35,
        'blur': 0.8,
        'method': 'cavern',
        'name': 'Cavern Deep',
        'description': 'Deep shadows with mysterious tunnels'
    },
    
    'frozenWastes': {
        'contrast': 3.2,
        'brightness': 40,
        'threshold': 110,
        'noise': 15,
        'blur': 0,
        'method': 'frozen',
        'name': 'Frozen Wastes',
        'description': 'Stark, minimalist winter landscapes'
    },
    
    'darkRitual': {
        'contrast': 2.6,
        'brightness': -15,
        'threshold': 85,
        'noise': 45,
        'blur': 1.2,
        'method': 'ritual',
        'name': 'Dark Ritual',
        'description': 'Dramatic contrast for ritual atmospheres'
    }
}

# Default parameters for custom processing
DEFAULT_PARAMS = {
    'contrast': 1.5,
    'brightness': 0,
    'threshold': 128,
    'noise': 20,
    'blur': 0,
    'method': 'custom'
}

def get_preset(name):
    """Get preset by name with fallback to default"""
    return PROCESSING_PRESETS.get(name, DEFAULT_PARAMS.copy())

def list_presets():
    """Return list of available preset names"""
    return list(PROCESSING_PRESETS.keys())

def get_preset_info():
    """Return preset information for UI"""
    return {
        name: {
            'name': preset['name'],
            'description': preset['description']
        }
        for name, preset in PROCESSING_PRESETS.items()
    }