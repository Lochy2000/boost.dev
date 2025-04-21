// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Notification handling
    const levelUpNotification = document.getElementById('level-up-notification');
    const achievementNotification = document.getElementById('achievement-notification');
    
    // Level up notification
    if (levelUpNotification) {
        const closeButton = levelUpNotification.querySelector('[data-dismiss-target]');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                levelUpNotification.classList.add('hidden');
            });
        }
    }

    // Achievement notification
    if (achievementNotification) {
        const closeButton = achievementNotification.querySelector('[data-dismiss-target]');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                achievementNotification.classList.add('hidden');
            });
        }
    }
}); 