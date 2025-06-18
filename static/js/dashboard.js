/**
 * Dashboard Card Link Enhancement
 * Ensures that dashboard cards are properly clickable and accessible
 */

class DashboardCardManager {
    constructor() {
        this.init();
    }

    init() {
        console.log('Dashboard Card Manager initialized');
        this.setupCardLinks();
        this.setupAccessibility();
        this.fixFloatingElements();
    }

    setupCardLinks() {
        const cardLinks = document.querySelectorAll('.dashboard-card-link');
        console.log(`Found ${cardLinks.length} dashboard card links`);

        cardLinks.forEach((link, index) => {
            const href = link.getAttribute('href');
            console.log(`Setting up card link ${index + 1}: ${href}`);

            // Remove any existing event listeners to prevent duplicates
            link.removeEventListener('click', this.handleCardClick);
            
            // Add click handler
            link.addEventListener('click', (e) => this.handleCardClick(e, href));
            
            // Add hover effects
            link.addEventListener('mouseenter', () => this.handleCardHover(link, true));
            link.addEventListener('mouseleave', () => this.handleCardHover(link, false));
        });
    }

    handleCardClick(event, href) {
        console.log('Dashboard card clicked:', href);
        
        // Prevent any potential interference
        event.preventDefault();
        event.stopPropagation();
        
        // Add visual feedback
        const card = event.currentTarget.querySelector('.content-card');
        if (card) {
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = '';
            }, 150);
        }
        
        // Navigate after brief animation
        setTimeout(() => {
            if (href && href !== '#') {
                window.location.href = href;
            } else {
                console.error('Invalid href for card link:', href);
            }
        }, 100);
    }

    handleCardHover(link, isHovering) {
        const card = link.querySelector('.content-card');
        if (!card) return;

        if (isHovering) {
            card.style.cursor = 'pointer';
            card.style.transform = 'translateY(-4px)';
        } else {
            card.style.transform = 'translateY(0)';
        }
    }

    setupAccessibility() {
        const cardLinks = document.querySelectorAll('.dashboard-card-link');
        
        cardLinks.forEach(link => {
            // Ensure links are focusable
            if (!link.hasAttribute('tabindex')) {
                link.setAttribute('tabindex', '0');
            }

            // Add keyboard navigation
            link.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    link.click();
                }
            });

            // Add focus styles
            link.addEventListener('focus', () => {
                link.style.outline = '2px solid var(--accent-purple, #8b5cf6)';
                link.style.outlineOffset = '2px';
                link.style.borderRadius = '16px';
            });

            link.addEventListener('blur', () => {
                link.style.outline = '';
                link.style.outlineOffset = '';
                link.style.borderRadius = '';
            });
        });
    }

    fixFloatingElements() {
        // Ensure floating elements don't interfere with clicks
        const floatingElements = document.querySelectorAll('.floating-element');
        console.log(`Found ${floatingElements.length} floating elements`);
        
        floatingElements.forEach(element => {
            element.style.pointerEvents = 'none';
            element.style.zIndex = '1';
        });

        // Ensure grid overlay doesn't interfere
        const gridOverlay = document.querySelector('.grid-overlay');
        if (gridOverlay) {
            gridOverlay.style.pointerEvents = 'none';
            gridOverlay.style.zIndex = '1';
        }
    }

    // Debug method to check for click interference
    debugClickInterference() {
        console.log('Debugging click interference...');
        
        const cardLinks = document.querySelectorAll('.dashboard-card-link');
        cardLinks.forEach((link, index) => {
            const rect = link.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const elementAtPoint = document.elementFromPoint(centerX, centerY);
            console.log(`Card ${index + 1} center element:`, elementAtPoint);
            
            if (elementAtPoint !== link && !link.contains(elementAtPoint)) {
                console.warn(`Card ${index + 1} may have click interference from:`, elementAtPoint);
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardCardManager = new DashboardCardManager();
    
    // Debug mode - remove in production
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        setTimeout(() => {
            window.dashboardCardManager.debugClickInterference();
        }, 1000);
    }
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardCardManager;
}