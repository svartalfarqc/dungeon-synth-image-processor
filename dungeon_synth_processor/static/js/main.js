// static/js/main.js
class DungeonSynthApp {
    constructor() {
        this.currentFilename = null;
        this.isProcessing = false;
        this.initializeEventListeners();
        this.updateSliderDisplays();
    }

    initializeEventListeners() {
        // File upload
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.handleFileUpload(e);
        });

        // Slider events - immediate processing like web app
        const sliders = ['contrast', 'brightness', 'threshold', 'noise', 'blur'];
        sliders.forEach(slider => {
            const element = document.getElementById(slider);
            element.addEventListener('input', () => {
                this.updateSliderDisplay(slider);
                // Immediate processing like original web app
                if (this.currentFilename && !this.isProcessing) {
                    this.processCustom();
                }
            });
        });

        // Add drag and drop functionality
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const fileInput = document.getElementById('fileInput');
        const uploadPrompt = document.getElementById('uploadPrompt');
        
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
            if (files.length > 0) {
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
        display.textContent = element.value;
    }

    showStatus(message, type = 'info') {
        const statusElement = document.getElementById('uploadStatus');
        statusElement.textContent = message;
        statusElement.className = `status-message ${type}`;
        statusElement.style.display = 'block';
        
        if (type === 'success' || type === 'error') {
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }

    showProcessingStatus(show = true, message = 'Processing image...') {
        const statusElement = document.getElementById('processingStatus');
        const messageElement = statusElement.querySelector('p');
        if (messageElement) {
            messageElement.textContent = message;
        }
        statusElement.style.display = show ? 'block' : 'none';
        this.isProcessing = show;
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
            this.showProcessingStatus(true, 'Uploading image...');

            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.currentFilename = result.filename;
                this.displayOriginalImage(result);
                this.enableControls();
                this.showStatus(`Image uploaded successfully (${result.width}x${result.height})`, 'success');
                
                // Auto-process all presets
                this.showProcessingStatus(true, 'Generating all variations...');
                setTimeout(() => {
                    this.processAllPresets();
                }, 500);
            } else {
                this.showStatus(result.error || 'Upload failed', 'error');
            }
        } catch (error) {
            this.showStatus(error.message, 'error');
        } finally {
            if (!this.currentFilename) {
                this.showProcessingStatus(false);
            }
        }
    }

    displayOriginalImage(imageData) {
        const img = document.getElementById('originalImage');
        const prompt = document.getElementById('uploadPrompt');
        const info = document.getElementById('imageInfo');

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

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    enableControls() {
        document.getElementById('processAllBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;
        document.getElementById('processCustomBtn').disabled = false;
        
        // Enable all download buttons
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.disabled = false;
        });
    }

    async processCustom() {
        if (!this.currentFilename || this.isProcessing) return;

        const params = this.getCurrentParams();
        params.method = 'custom';

        try {
            const preview = await this.processWithParams(params);
            this.displayProcessedImage('customImage', preview);
        } catch (error) {
            console.error('Custom processing error:', error);
            this.showStatus(`Processing error: ${error.message}`, 'error');
        }
    }

    getCurrentParams() {
        return {
            contrast: parseFloat(document.getElementById('contrast').value),
            brightness: parseInt(document.getElementById('brightness').value),
            threshold: parseInt(document.getElementById('threshold').value),
            noise: parseInt(document.getElementById('noise').value),
            blur: parseFloat(document.getElementById('blur').value)
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

        // Get preset parameters
        const presets = {
            'highContrast': { contrast: 2.5, brightness: 10, threshold: 100, noise: 25, blur: 0, method: 'threshold' },
            'threshold': { contrast: 1.8, brightness: 0, threshold: 80, noise: 15, blur: 0, method: 'threshold' },
            'atmospheric': { contrast: 1.6, brightness: -10, threshold: 140, noise: 20, blur: 1.5, method: 'atmospheric' },
            'silhouette': { contrast: 3, brightness: 20, threshold: 70, noise: 10, blur: 0, method: 'silhouette' },
            'manuscript': { contrast: 2, brightness: 15, threshold: 120, noise: 40, blur: 0.5, method: 'manuscript' },
            'ghostly': { contrast: 1.3, brightness: 30, threshold: 180, noise: 30, blur: 2, method: 'ghostly' }
        };

        const params = presets[presetName];
        if (!params) return;

        // Update UI sliders
        document.getElementById('contrast').value = params.contrast;
        document.getElementById('brightness').value = params.brightness;
        document.getElementById('threshold').value = params.threshold;
        document.getElementById('noise').value = params.noise;
        document.getElementById('blur').value = params.blur;
        
        this.updateSliderDisplays();

        // Process and display
        try {
            this.showProcessingStatus(true, `Applying ${presetName} preset...`);
            
            const preview = await this.processWithParams(params);
            const imageMap = {
                'highContrast': 'highContrastImage',
                'threshold': 'thresholdImage',
                'atmospheric': 'atmosphericImage',
                'silhouette': 'silhouetteImage',
                'manuscript': 'manuscriptImage',
                'ghostly': 'ghostlyImage'
            };
            
            this.displayProcessedImage(imageMap[presetName] || 'customImage', preview);
            this.displayProcessedImage('customImage', preview); // Also update custom
            
        } catch (error) {
            this.showStatus(`Processing error: ${error.message}`, 'error');
        } finally {
            this.showProcessingStatus(false);
        }
    }

    async processAllPresets() {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        this.showProcessingStatus(true, 'Processing all variations...');
        
        const presets = [
            { name: 'highContrast', imageId: 'highContrastImage', params: { contrast: 2.5, brightness: 10, threshold: 100, noise: 25, blur: 0, method: 'threshold' }},
            { name: 'threshold', imageId: 'thresholdImage', params: { contrast: 1.8, brightness: 0, threshold: 80, noise: 15, blur: 0, method: 'threshold' }},
            { name: 'atmospheric', imageId: 'atmosphericImage', params: { contrast: 1.6, brightness: -10, threshold: 140, noise: 20, blur: 1.5, method: 'atmospheric' }},
            { name: 'silhouette', imageId: 'silhouetteImage', params: { contrast: 3, brightness: 20, threshold: 70, noise: 10, blur: 0, method: 'silhouette' }},
            { name: 'manuscript', imageId: 'manuscriptImage', params: { contrast: 2, brightness: 15, threshold: 120, noise: 40, blur: 0.5, method: 'manuscript' }},
            { name: 'ghostly', imageId: 'ghostlyImage', params: { contrast: 1.3, brightness: 30, threshold: 180, noise: 30, blur: 2, method: 'ghostly' }}
        ];

        try {
            for (let i = 0; i < presets.length; i++) {
                const preset = presets[i];
                this.showProcessingStatus(true, `Processing ${preset.name} (${i + 1}/${presets.length})...`);
                
                const preview = await this.processWithParams(preset.params);
                this.displayProcessedImage(preset.imageId, preview);
                
                // Small delay to prevent overwhelming the server
                await new Promise(resolve => setTimeout(resolve, 200));
            }
            
            // Process custom with current settings
            this.showProcessingStatus(true, 'Finalizing custom preview...');
            await this.processCustom();
            
            this.showStatus('All variations processed successfully!', 'success');
            
        } catch (error) {
            this.showStatus(`Processing error: ${error.message}`, 'error');
        } finally {
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
        const placeholder = img.parentElement.querySelector('.processing-placeholder');
        
        img.src = previewData;
        img.style.display = 'block';
        if (placeholder) {
            placeholder.style.display = 'none';
        }
    }

    async downloadProcessed(presetName) {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        try {
            this.showStatus('Preparing high-resolution download...', 'info');
            this.showProcessingStatus(true, 'Generating full-resolution image...');
            
            const url = `/download/${presetName}/${this.currentFilename}`;
            
            // Create temporary link and trigger download
            const a = document.createElement('a');
            a.href = url;
            a.download = `dungeon_synth_${presetName}.png`;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            this.showStatus('Download started successfully!', 'success');
            
        } catch (error) {
            this.showStatus(`Download error: ${error.message}`, 'error');
        } finally {
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 1000);
        }
    }

    resetToOriginal() {
        if (!this.currentFilename) return;

        // Reset all sliders to defaults
        document.getElementById('contrast').value = 1.5;
        document.getElementById('brightness').value = 0;
        document.getElementById('threshold').value = 128;
        document.getElementById('noise').value = 20;
        document.getElementById('blur').value = 0;
        
        this.updateSliderDisplays();
        
        if (!this.isProcessing) {
            this.processCustom();
        }
    }

    async downloadProcessed(presetName) {
        if (!this.currentFilename) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        try {
            this.showStatus('Preparing high-resolution download...', 'info');
            this.showProcessingStatus(true, 'Generating full-resolution image...');
            
            // If downloading custom, send current parameters first
            if (presetName === 'custom') {
                const params = this.getCurrentParams();
                params.method = 'custom';
                
                // Send current custom parameters to server
                await fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        filename: this.currentFilename,
                        ...params
                    })
                });
                
                // Small delay to ensure server processes the parameters
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            
            const url = `/download/${presetName}/${this.currentFilename}`;
            
            // Use fetch for better error handling
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`Download failed: ${response.statusText}`);
            }
            
            // Get the blob and create download
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);
            
            // Create temporary link and trigger download
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `dungeon_synth_${presetName}.png`;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // Clean up the blob URL
            setTimeout(() => {
                URL.revokeObjectURL(downloadUrl);
            }, 1000);
            
            this.showStatus('Download completed successfully!', 'success');
            
        } catch (error) {
            this.showStatus(`Download error: ${error.message}`, 'error');
        } finally {
            setTimeout(() => {
                this.showProcessingStatus(false);
            }, 1000);
        }
    }

    // Cleanup function
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
    app.applyPreset(presetName);
}

function processAllPresets() {
    app.processAllPresets();
}

function resetToOriginal() {
    app.resetToOriginal();
}

function processCustom() {
    app.processCustom();
}

function downloadProcessed(presetName) {
    app.downloadProcessed(presetName);
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', function() {
    app = new DungeonSynthApp();
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        app.cleanup();
    });
});