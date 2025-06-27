/**
 * Page Loading Animation Controller
 * Handles navigation loading states with subtle geometric animations
 */

class PageLoadingController {
    constructor() {
        this.isLoading = false;
        this.loadingOverlay = null;
        this.loadingTimeout = null;
        this.minLoadingTime = 300; // Minimum loading time in ms
        this.maxLoadingTime = 5000; // Maximum loading time before auto-hide
        
        this.init();
    }

    init() {
        this.createLoadingOverlay();
        this.attachNavigationListeners();
        this.handleBrowserNavigation();
    }

    createLoadingOverlay() {
        // Create loading overlay HTML
        const overlayHTML = `
            <div id="page-loading-overlay" class="page-loading-overlay">
                <div class="loading-container">
                    <!-- Geometric shapes animation -->
                    <div class="loading-shapes">
                        <div class="loading-square"></div>
                        <div class="loading-circle"></div>
                        <div class="loading-circle"></div>
                        <div class="loading-circle"></div>
                        <div class="loading-circle"></div>
                    </div>
                    
                    <!-- Loading text -->
                    <div class="loading-text">Loading...</div>
                    
                    <!-- Progress bar (optional) -->
                    <div class="loading-progress">
                        <div class="loading-progress-bar" id="loading-progress-bar"></div>
                    </div>
                </div>
            </div>
        `;

        // Insert overlay into DOM
        document.body.insertAdjacentHTML('beforeend', overlayHTML);
        this.loadingOverlay = document.getElementById('page-loading-overlay');
    }

    showLoading() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        
        // Add loading class to content
        const mainContent = document.querySelector('main');
        if (mainContent) {
            mainContent.classList.add('content-loading');
        }
        
        // Show overlay
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.add('active');
        }
        
        // Reset progress bar
        const progressBar = document.getElementById('loading-progress-bar');
        if (progressBar) {
            progressBar.style.width = '0%';
            this.animateProgressBar(progressBar);
        }
        
        // Auto-hide after max time
        this.loadingTimeout = setTimeout(() => {
            this.hideLoading();
        }, this.maxLoadingTime);
    }

    hideLoading() {
        if (!this.isLoading) return;
        
        // Clear timeout
        if (this.loadingTimeout) {
            clearTimeout(this.loadingTimeout);
            this.loadingTimeout = null;
        }
        
        // Ensure minimum loading time
        setTimeout(() => {
            this.isLoading = false;
            
            // Hide overlay
            if (this.loadingOverlay) {
                this.loadingOverlay.classList.remove('active');
            }
            
            // Remove loading class from content
            const mainContent = document.querySelector('main');
            if (mainContent) {
                mainContent.classList.remove('content-loading');
                mainContent.classList.add('content-loaded');
                
                // Remove the loaded class after transition
                setTimeout(() => {
                    mainContent.classList.remove('content-loaded');
                }, 300);
            }
        }, this.minLoadingTime);
    }

    animateProgressBar(progressBar) {
        if (!this.isLoading) return;
        
        // Simulate progress
        let progress = 0;
        const increment = Math.random() * 15 + 5; // Random increment between 5-20%
        
        const updateProgress = () => {
            if (!this.isLoading) return;
            
            progress += increment;
            progress = Math.min(progress, 90); // Don't reach 100% until actually loaded
            
            progressBar.style.width = `${progress}%`;
            
            if (progress < 90) {
                setTimeout(updateProgress, 200 + Math.random() * 300);
            }
        };
        
        updateProgress();
    }

    completeProgress() {
        const progressBar = document.getElementById('loading-progress-bar');
        if (progressBar) {
            progressBar.style.width = '100%';
        }
    }

    attachNavigationListeners() {
        // Intercept navigation links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            
            // Skip if not a navigation link or if it's an external link
            if (!link || 
                link.hostname !== window.location.hostname ||
                link.href === window.location.href ||
                link.target === '_blank' ||
                link.download ||
                link.href.startsWith('mailto:') ||
                link.href.startsWith('tel:')) {
                return;
            }
            
            // Skip if it's a same-page anchor link
            if (link.href.includes('#') && 
                link.href.split('#')[0] === window.location.href.split('#')[0]) {
                return;
            }
            
            // Show loading animation
            this.showLoading();
        });

        // Handle form submissions that might cause page navigation
        document.addEventListener('submit', (e) => {
            const form = e.target;
            
            // Skip AJAX forms or forms with target="_blank"
            if (form.target === '_blank' || 
                form.hasAttribute('data-ajax') ||
                form.method.toLowerCase() === 'get') {
                return;
            }
            
            this.showLoading();
        });
    }

    handleBrowserNavigation() {
        // Handle browser back/forward buttons
        window.addEventListener('beforeunload', () => {
            this.showLoading();
        });

        // Handle page load completion
        window.addEventListener('load', () => {
            this.hideLoading();
        });

        // Handle DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {
            this.completeProgress();
            this.hideLoading();
        });

        // Handle navigation via History API (for SPAs)
        window.addEventListener('popstate', () => {
            this.showLoading();
        });
    }

    // Manual methods for programmatic control
    show() {
        this.showLoading();
    }

    hide() {
        this.hideLoading();
    }

    // Method to customize loading text
    setLoadingText(text) {
        const loadingText = document.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }

    // Method to use alternative dot animation
    useDotsAnimation() {
        const shapesContainer = document.querySelector('.loading-shapes');
        if (shapesContainer) {
            shapesContainer.innerHTML = `
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            `;
        }
    }
}

// Global loading controller instance
let pageLoadingController;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    pageLoadingController = new PageLoadingController();
    
    // Make it globally accessible for manual control
    window.PageLoading = {
        show: () => pageLoadingController.show(),
        hide: () => pageLoadingController.hide(),
        setText: (text) => pageLoadingController.setLoadingText(text),
        useDots: () => pageLoadingController.useDotsAnimation()
    };
});

// Django-specific enhancements
if (typeof django !== 'undefined') {
    // Handle Django AJAX requests
    document.addEventListener('DOMContentLoaded', function() {
        // Override jQuery AJAX if available
        if (typeof $ !== 'undefined' && $.ajaxSetup) {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    // Only show loading for page-changing requests
                    if (settings.url && !settings.url.includes('api/') && 
                        (settings.type === 'POST' || settings.url !== window.location.href)) {
                        pageLoadingController?.show();
                    }
                },
                complete: function() {
                    pageLoadingController?.hide();
                }
            });
        }
        
        // Handle fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            const url = args[0];
            const options = args[1] || {};
            
            // Show loading for navigation-type requests
            if (typeof url === 'string' && 
                !url.includes('api/') && 
                (options.method === 'POST' || options.method === 'PUT')) {
                pageLoadingController?.show();
            }
            
            return originalFetch.apply(this, args)
                .finally(() => {
                    pageLoadingController?.hide();
                });
        };
    });
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PageLoadingController;
}
