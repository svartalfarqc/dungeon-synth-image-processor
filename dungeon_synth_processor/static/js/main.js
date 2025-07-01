// static/js/main.js
class DungeonSynthApp {
    constructor() {
        this.currentFilename = null;
        this.isProcessing = false;
        this.selectedColorTint = 'none';
        this.colorTints = {};
        this.preserveAspectRatio = false;
        this.processedImages = {}; // Store processed images for each preset
        this.initializeEventListeners();
        this.updateSliderDisplays();
        this.loadColorTints();
    }

    async loadColorTints() {
        try {
            const response = await fetch('/get_color_tints');
            this.colorTints = await response.json();
        } catch (error) {
            console.error('Failed to load color tints:', error);
        }
    }

    initializeEventListeners() {
        // File upload
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                this.handleFileUpload(e);
            });
        }

        // Slider events with debounced processing
        const sliders = ['contrast', 'brightness', 'threshold', 'noise', 'blur'];
        sliders.forEach(slider => {
            const element = document.getElementById(slider);
            if (element) {
                element.addEventListener('input', () => {
                    this.updateSliderDisplay(slider);
                    this.debounceCustomProcess();
                });
            }
        });

        const aspectToggle = document.getElementById('preserveAspectRatio');
        if (aspectToggle) {
            aspectToggle.addEventListener('change', (e) => {
                this.preserveAspectRatio = e.target.checked;
                // Reprocess if we have an image loaded
                if (this.currentFilename && !this.isProcessing) {
                    this.debounceCustomProcess();
                    // Also reprocess all presets if they've been generated
                    if (Object.keys(this.processedImages).length > 1) {
                        this.processAllPresets();
                    }
                }
            });
        }

        // Color swatch selection
        document.querySelectorAll('.color-swatch').forEach(swatch => {
            swatch.addEventListener('click', (e) => {
                this.selectColorTint(swatch.dataset.tint);
            });
        });

        // Add drag and drop functionality
        this.setupDragAndDrop();
    }

    selectColorTint(tintName) {
        // Update selected state
        document.querySelectorAll('.color-swatch').forEach(swatch => {
            swatch.classList.remove('selected');
        });
        
        const selectedSwatch = document.querySelector(`.color-swatch[data-tint="${tintName}"]`);
        if (selectedSwatch) {
            selectedSwatch.classList.add('selected');
        }
        
        this.selectedColorTint = tintName;
        
        // Reprocess all visible images with new tint
        if (this.currentFilename && !this.isProcessing) {
            this.reprocessAllWithNewTint();
        }
    }

    async reprocessAllWithNewTint() {
        this.showProcessingStatus(true, 'Applying color tint to all images...', 10);
        
        try {
            // Reprocess each preset that's already been processed
            const presets = Object.keys(this.processedImages);
            for (let i = 0; i < presets.length; i++) {
                const preset = presets[i];
                const progress = 10 + (i / presets.length) * 80;
                this.showProcessingStatus(true, `Applying tint to ${preset}...`, progress);
                
                if (preset === 'custom') {
                    await this.processCustom();
                } else {
                    await this.reprocessPreset(preset);
                }
            }
            
            this.showProcessingStatus(true, 'Color tint applied!', 100);
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 1000);
            
        } catch (error) {
            console.error('Error applying color tint:', error);
            this.showStatus('Error applying color tint', 'error');
            this.showProcessingStatus(false);
        }
    }

    async reprocessPreset(presetName) {
        const presets = {
            'medieval': { contrast: 1.4, brightness: -5, threshold: 120, noise: 35, blur: 0.8, method: 'manuscript' },
            'threshold': { contrast: 1.6, brightness: 0, threshold: 90, noise: 15, blur: 0, method: 'threshold' },
            'atmospheric': { contrast: 1.3, brightness: -15, threshold: 150, noise: 25, blur: 2.0, method: 'atmospheric' },
            'silhouette': { contrast: 2.8, brightness: 25, threshold: 75, noise: 8, blur: 0, method: 'silhouette' },
            'ghostly': { contrast: 1.2, brightness: 35, threshold: 190, noise: 30, blur: 2.5, method: 'ghostly' },
            'cavernDeep': { contrast: 2.2, brightness: -40, threshold: 85, noise: 40, blur: 1.0, method: 'cavern' },
            'frozenWastes': { contrast: 2.8, brightness: 50, threshold: 120, noise: 12, blur: 0, method: 'frozen' },
            'darkRitual': { contrast: 2.4, brightness: -20, threshold: 80, noise: 50, blur: 1.5, method: 'ritual' },
            'lithographic': { contrast: 1.8, brightness: 5, threshold: 130, noise: 20, blur: 0.3, method: 'lithographic' },
            'sepiaNostalgia': { contrast: 1.1, brightness: 20, threshold: 140, noise: 18, blur: 0.7, method: 'sepia' },
            'comfyHearth': { contrast: 1.0, brightness: 15, threshold: 160, noise: 12, blur: 1.2, method: 'comfy' },
            'forestMystic': { contrast: 1.3, brightness: -10, threshold: 110, noise: 28, blur: 1.0, method: 'forest' }
        };

        const params = presets[presetName];
        if (!params) return;

        params.color_tint = this.selectedColorTint;
        params.preserve_aspect_ratio = this.preserveAspectRatio;  // Add this line
        const preview = await this.processWithParams(params);
        
        const imageMap = {
            'medieval': 'medievalImage',
            'threshold': 'thresholdImage',
            'atmospheric': 'atmosphericImage',
            'silhouette': 'silhouetteImage',
            'ghostly': 'ghostlyImage',
            'cavernDeep': 'cavernDeepImage',
            'frozenWastes': 'frozenWastesImage',
            'darkRitual': 'darkRitualImage',
            'lithographic': 'lithographicImage',
            'sepiaNostalgia': 'sepiaNostalgiaImage',
            'comfyHearth': 'comfyHearthImage',
            'forestMystic': 'forestMysticImage'
        };
        
        this.displayProcessedImage(imageMap[presetName], preview);
    }

    setupDragAndDrop() {
        const fileInput = document.getElementById('fileInput');
        const uploadPrompt = document.getElementById('uploadPrompt');
        
        if (!uploadPrompt) return;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadPrompt.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadPrompt.addEventListener(eventName, () => {
                uploadPrompt.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadPrompt.addEventListener(eventName, () => {
                uploadPrompt.classList.remove('drag-over');
            }, false);
        });

        uploadPrompt.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0 && fileInput) {
                fileInput.files = files;
                this.handleFileUpload({ target: { files: files } });
            }
        }, false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    updateSliderDisplays() {
        const sliders = ['contrast', 'brightness', 'threshold', 'noise', 'blur'];
        sliders.forEach(slider => this.updateSliderDisplay(slider));
    }

    updateSliderDisplay(slider) {
        const element = document.getElementById(slider);
        const display = document.getElementById(slider + 'Value');
        if (element && display) {
            display.textContent = element.value;
        }
    }

    showStatus(message, type = 'info') {
        const statusElement = document.getElementById('uploadStatus');
        if (!statusElement) return;
        
        statusElement.textContent = message;
        statusElement.className = `status-message ${type}`;
        statusElement.style.display = 'block';
        
        if (type === 'success' || type === 'error') {
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }

    showProcessingStatus(show = true, message = 'Processing image...', progress = 0) {
        const statusElement = document.getElementById('processingStatus');
        if (!statusElement) return;
        
        const messageElement = statusElement.querySelector('p');
        const progressFill = statusElement.querySelector('.progress-fill');
        
        if (messageElement) {
            messageElement.textContent = message;
        }
        
        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }
        
        statusElement.style.display = show ? 'block' : 'none';
        this.isProcessing = show;
    }

    debounceCustomProcess() {
        if (this.customProcessTimeout) {
            clearTimeout(this.customProcessTimeout);
        }
        this.customProcessTimeout = setTimeout(() => {
            if (this.currentFilename && !this.isProcessing) {
                this.processCustom();
            }
        }, 500);
    }

    validateFile(file) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff', 'image/bmp', 'image/webp'];
        const maxSize = 32 * 1024 * 1024; // 32MB

        if (!allowedTypes.includes(file.type)) {
            throw new Error('Invalid file type. Please upload JPG, PNG, TIFF, BMP, or WebP images.');
        }

        if (file.size > maxSize) {
            throw new Error('File too large. Maximum size is 32MB.');
        }

        return true;
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            this.validateFile(file);
            
            this.showStatus('Uploading and processing image...', 'info');
            this.showProcessingStatus(true, 'Uploading image...', 10);

            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.currentFilename = result.filename;
                this.processedImages = {}; // Reset processed images
                this.displayOriginalImage(result);
                this.enableControls();
                this.showStatus(`Image uploaded successfully (${result.width}x${result.height})`, 'success');
                
                // Auto-process all presets
                this.showProcessingStatus(true, 'Generating all variations...', 20);
                setTimeout(() => {
                    this.processAllPresets();
                }, 500);
            } else {
                this.showStatus(result.error || 'Upload failed', 'error');
                this.showProcessingStatus(false);
            }
        } catch (error) {
            this.showStatus(error.message, 'error');
            this.showProcessingStatus(false);
        }
    }

    displayOriginalImage(imageData) {
        const img = document.getElementById('originalImage');
        const prompt = document.getElementById('uploadPrompt');
        const info = document.getElementById('imageInfo');

        if (img && prompt && info) {
            img.src = imageData.preview;
            img.style.display = 'block';
            prompt.style.display = 'none';
            
            info.innerHTML = `
                <strong>Dimensions:</strong> ${imageData.width} x ${imageData.height}<br>
                <strong>Format:</strong> ${imageData.format}<br>
                <strong>Size:</strong> ${this.formatFileSize(imageData.width * imageData.height * 3)}<br>
                <strong>Filename:</strong> ${imageData.filename}
            `;
            info.style.display = 'block';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    enableControls() {
        const processAllBtn = document.getElementById('processAllBtn');
        const resetBtn = document.getElementById('resetBtn');
        
        if (processAllBtn) processAllBtn.disabled = false;
        if (resetBtn) resetBtn.disabled = false;
        
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.disabled = false;
        });
    }

    async processCustom() {
        if (!this.currentFilename || this.isProcessing) return;

        const params = this.getCurrentParams();
        params.method = 'custom';
        params.color_tint = this.selectedColorTint;
        params.preserve_aspect_ratio = this.preserveAspectRatio;  // Ensure this is included

        try {
            const preview = await this.processWithParams(params);
            this.displayProcessedImage('customImage', preview);
            this.processedImages['custom'] = true;
            
            // Enable custom download button
            const customDownloadBtn = document.querySelector('.custom-container .download-btn');
            if (customDownloadBtn) {
                customDownloadBtn.disabled = false;
                customDownloadBtn.classList.add('ready');
                customDownloadBtn.classList.remove('processing');
            }
            
        } catch (error) {
            console.error('Custom processing error:', error);
            this.showStatus(`Processing error: ${error.message}`, 'error');
        }
    }

    getCurrentParams() {
        return {
            contrast: parseFloat(document.getElementById('contrast')?.value || 1.5),
            brightness: parseInt(document.getElementById('brightness')?.value || 0),
            threshold: parseInt(document.getElementById('threshold')?.value || 128),
            noise: parseInt(document.getElementById('noise')?.value || 20),
            blur: parseFloat(document.getElementById('blur')?.value || 0),
            preserve_aspect_ratio: this.preserveAspectRatio
        };
    }

    async applyPreset(presetName) {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        if (this.isProcessing) {
            this.showStatus('Processing in progress, please wait...', 'error');
            return;
        }

        const presets = {
            'medieval': { contrast: 1.4, brightness: -5, threshold: 120, noise: 35, blur: 0.8, method: 'manuscript' },
            'threshold': { contrast: 1.6, brightness: 0, threshold: 90, noise: 15, blur: 0, method: 'threshold' },
            'atmospheric': { contrast: 1.3, brightness: -15, threshold: 150, noise: 25, blur: 2.0, method: 'atmospheric' },
            'silhouette': { contrast: 2.8, brightness: 25, threshold: 75, noise: 8, blur: 0, method: 'silhouette' },
            'ghostly': { contrast: 1.2, brightness: 35, threshold: 190, noise: 30, blur: 2.5, method: 'ghostly' },
            'cavernDeep': { contrast: 2.2, brightness: -40, threshold: 85, noise: 40, blur: 1.0, method: 'cavern' },
            'frozenWastes': { contrast: 2.8, brightness: 50, threshold: 120, noise: 12, blur: 0, method: 'frozen' },
            'darkRitual': { contrast: 2.4, brightness: -20, threshold: 80, noise: 50, blur: 1.5, method: 'ritual' },
            'lithographic': { contrast: 1.8, brightness: 5, threshold: 130, noise: 20, blur: 0.3, method: 'lithographic' },
            'sepiaNostalgia': { contrast: 1.1, brightness: 20, threshold: 140, noise: 18, blur: 0.7, method: 'sepia' },
            'comfyHearth': { contrast: 1.0, brightness: 15, threshold: 160, noise: 12, blur: 1.2, method: 'comfy' },
            'forestMystic': { contrast: 1.3, brightness: -10, threshold: 110, noise: 28, blur: 1.0, method: 'forest' }
        };

        const params = presets[presetName];
        if (!params) return;

        // Update UI sliders
        const contrastSlider = document.getElementById('contrast');
        const brightnessSlider = document.getElementById('brightness');
        const thresholdSlider = document.getElementById('threshold');
        const noiseSlider = document.getElementById('noise');
        const blurSlider = document.getElementById('blur');
        
        if (contrastSlider) contrastSlider.value = params.contrast;
        if (brightnessSlider) brightnessSlider.value = params.brightness;
        if (thresholdSlider) thresholdSlider.value = params.threshold;
        if (noiseSlider) noiseSlider.value = params.noise;
        if (blurSlider) blurSlider.value = params.blur;
        
        this.updateSliderDisplays();

        try {
            this.showProcessingStatus(true, `Applying ${presetName} preset...`, 30);
            
            params.color_tint = this.selectedColorTint;
            params.preserve_aspect_ratio = this.preserveAspectRatio;  // Add this line
            const preview = await this.processWithParams(params);
            
            const imageMap = {
                'medieval': 'medievalImage',
                'threshold': 'thresholdImage',
                'atmospheric': 'atmosphericImage',
                'silhouette': 'silhouetteImage',
                'ghostly': 'ghostlyImage',
                'cavernDeep': 'cavernDeepImage',
                'frozenWastes': 'frozenWastesImage',
                'darkRitual': 'darkRitualImage',
                'lithographic': 'lithographicImage',
                'sepiaNostalgia': 'sepiaNostalgiaImage',
                'comfyHearth': 'comfyHearthImage',
                'forestMystic': 'forestMysticImage'
            };
            
            this.displayProcessedImage(imageMap[presetName] || 'customImage', preview);
            this.displayProcessedImage('customImage', preview);
            this.processedImages[presetName] = true;
            this.processedImages['custom'] = true;
            
            // Enable custom download button
            const customDownloadBtn = document.querySelector('.custom-container .download-btn');
            if (customDownloadBtn) {
                customDownloadBtn.disabled = false;
                customDownloadBtn.classList.add('ready');
            }
            
            this.showProcessingStatus(true, `${presetName} preset applied!`, 100);
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 1000);
            
        } catch (error) {
            this.showStatus(`Processing error: ${error.message}`, 'error');
            this.showProcessingStatus(false);
        }
    }

    async processAllPresets() {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        this.showProcessingStatus(true, 'Processing all variations...', 25);
        
        const presets = [
            { name: 'medieval', imageId: 'medievalImage', params: { contrast: 1.4, brightness: -5, threshold: 120, noise: 35, blur: 0.8, method: 'manuscript' }},
            { name: 'threshold', imageId: 'thresholdImage', params: { contrast: 1.6, brightness: 0, threshold: 90, noise: 15, blur: 0, method: 'threshold' }},
            { name: 'atmospheric', imageId: 'atmosphericImage', params: { contrast: 1.3, brightness: -15, threshold: 150, noise: 25, blur: 2.0, method: 'atmospheric' }},
            { name: 'silhouette', imageId: 'silhouetteImage', params: { contrast: 2.8, brightness: 25, threshold: 75, noise: 8, blur: 0, method: 'silhouette' }},
            { name: 'ghostly', imageId: 'ghostlyImage', params: { contrast: 1.2, brightness: 35, threshold: 190, noise: 30, blur: 2.5, method: 'ghostly' }},
            { name: 'cavernDeep', imageId: 'cavernDeepImage', params: { contrast: 2.2, brightness: -40, threshold: 85, noise: 40, blur: 1.0, method: 'cavern' }},
            { name: 'frozenWastes', imageId: 'frozenWastesImage', params: { contrast: 2.8, brightness: 50, threshold: 120, noise: 12, blur: 0, method: 'frozen' }},
            { name: 'darkRitual', imageId: 'darkRitualImage', params: { contrast: 2.4, brightness: -20, threshold: 80, noise: 50, blur: 1.5, method: 'ritual' }},
            { name: 'lithographic', imageId: 'lithographicImage', params: { contrast: 1.8, brightness: 5, threshold: 130, noise: 20, blur: 0.3, method: 'lithographic' }},
            { name: 'sepiaNostalgia', imageId: 'sepiaNostalgiaImage', params: { contrast: 1.1, brightness: 20, threshold: 140, noise: 18, blur: 0.7, method: 'sepia' }},
            { name: 'comfyHearth', imageId: 'comfyHearthImage', params: { contrast: 1.0, brightness: 15, threshold: 160, noise: 12, blur: 1.2, method: 'comfy' }},
            { name: 'forestMystic', imageId: 'forestMysticImage', params: { contrast: 1.3, brightness: -10, threshold: 110, noise: 28, blur: 1.0, method: 'forest' }}
        ];

        try {
            for (let i = 0; i < presets.length; i++) {
                const preset = presets[i];
                const progress = 25 + (i / presets.length) * 60;
                this.showProcessingStatus(true, `Processing ${preset.name} (${i + 1}/${presets.length})...`, progress);
                
                preset.params.color_tint = this.selectedColorTint;
                preset.params.preserve_aspect_ratio = this.preserveAspectRatio; 
                const preview = await this.processWithParams(preset.params);
                this.displayProcessedImage(preset.imageId, preview);
                this.processedImages[preset.name] = true;
                
                await new Promise(resolve => setTimeout(resolve, 200));
            }
            
            this.showProcessingStatus(true, 'Finalizing custom preview...', 90);
            await this.processCustom();
            
            this.showStatus('All variations processed successfully!', 'success');
            this.showProcessingStatus(true, 'All processing complete!', 100);
            
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 2000);
            
        } catch (error) {
            this.showStatus(`Processing error: ${error.message}`, 'error');
            this.showProcessingStatus(false);
        }
    }

    async processWithParams(params) {
        const requestData = {
            filename: this.currentFilename,
            ...params
        };

        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Processing failed');
        }

        return result.preview;
    }

    displayProcessedImage(imageId, previewData) {
        const img = document.getElementById(imageId);
        const placeholder = img?.parentElement?.querySelector('.processing-placeholder');
        
        if (img) {
            img.src = previewData;
            img.style.display = 'block';
            if (placeholder) {
                placeholder.style.display = 'none';
            }
        }
    }

    async downloadProcessed(presetName) {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        try {
            this.showStatus('Preparing download...', 'info');
            this.showProcessingStatus(true, 'Generating download...', 25);
            
            // Get selected output size
            const outputSize = document.getElementById('outputSize')?.value || '400';
            
            // Build URL with current parameters
            let url = `/download/${presetName}/${this.currentFilename}?tint=${this.selectedColorTint}&size=${outputSize}&preserve_aspect_ratio=${this.preserveAspectRatio}`;
            
            // For custom preset, add all current slider values
            if (presetName === 'custom') {
                const params = this.getCurrentParams();
                url += `&contrast=${params.contrast}`;
                url += `&brightness=${params.brightness}`;
                url += `&threshold=${params.threshold}`;
                url += `&noise=${params.noise}`;
                url += `&blur=${params.blur}`;
            }
            
            this.showProcessingStatus(true, 'Downloading image...', 75);
            
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`Download failed: ${response.statusText}`);
            }
            
            this.showProcessingStatus(true, 'Preparing download...', 90);
            
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = downloadUrl;
            
            // Extract filename from Content-Disposition header if available, or use default
            const contentDisposition = response.headers.get('content-disposition');
            let downloadName = `dungeon_synth_${presetName}.png`;
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    downloadName = filenameMatch[1].replace(/['"]/g, '');
                }
            } else {
                // Use the filename pattern from the server
                const tintSuffix = this.selectedColorTint !== 'none' ? `_${this.selectedColorTint}` : '';
                downloadName = `dungeon_synth_${presetName}${tintSuffix}.png`;
            }
            
            a.download = downloadName;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            setTimeout(() => {
                URL.revokeObjectURL(downloadUrl);
            }, 1000);
            
            this.showProcessingStatus(true, 'Download complete!', 100);
            this.showStatus('Download completed successfully!', 'success');
            
        } catch (error) {
            this.showStatus(`Download error: ${error.message}`, 'error');
        } finally {
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 1500);
        }
    }

    resetToOriginal() {
        if (!this.currentFilename) return;

        const contrastSlider = document.getElementById('contrast');
        const brightnessSlider = document.getElementById('brightness');
        const thresholdSlider = document.getElementById('threshold');
        const noiseSlider = document.getElementById('noise');
        const blurSlider = document.getElementById('blur');
        
        if (contrastSlider) contrastSlider.value = 1.5;
        if (brightnessSlider) brightnessSlider.value = 0;
        if (thresholdSlider) thresholdSlider.value = 128;
        if (noiseSlider) noiseSlider.value = 20;
        if (blurSlider) blurSlider.value = 0;
        
        this.updateSliderDisplays();
        
        // Reset color tint
        this.selectColorTint('none');
        
        if (!this.isProcessing) {
            this.debounceCustomProcess();
        }
    }

    async cleanup() {
        if (this.currentFilename) {
            try {
                await fetch(`/cleanup/${this.currentFilename}`, { method: 'POST' });
            } catch (error) {
                console.error('Cleanup error:', error);
            }
        }
    }
}

// Global functions for button onclick handlers
let app;

function applyPreset(presetName) {
    if (app) app.applyPreset(presetName);
}

function processAllPresets() {
    if (app) app.processAllPresets();
}

function resetToOriginal() {
    if (app) app.resetToOriginal();
}

function processCustom() {
    if (app) app.processCustom();
}

function downloadProcessed(presetName) {
    if (app) app.downloadProcessed(presetName);
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', function() {
    app = new DungeonSynthApp();
    
    // Set initial color tint selection
    const noneSwatch = document.querySelector('.color-swatch[data-tint="none"]');
    if (noneSwatch) {
        noneSwatch.classList.add('selected');
    }
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        if (app) app.cleanup();
    });
});