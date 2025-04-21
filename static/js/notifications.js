class NotificationManager {
    constructor() {
        this.notificationIcon = document.getElementById('notification-icon');
        this.notificationCount = document.getElementById('notification-count');
        this.notificationDropdown = document.getElementById('notification-dropdown');
        this.notifications = [];
        
        console.log('Notification manager initialized');
        console.log('Notification icon found:', !!this.notificationIcon);
        console.log('Notification count found:', !!this.notificationCount);
        console.log('Notification dropdown found:', !!this.notificationDropdown);
        
        // Initialize
        this.setupEventListeners();
        this.fetchNotifications();
        
        // Poll for new notifications every 30 seconds
        setInterval(() => this.fetchNotifications(), 30000);
    }
    
    setupEventListeners() {
        // Toggle dropdown on icon click
        this.notificationIcon?.addEventListener('click', () => {
            this.notificationDropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.notificationDropdown?.contains(e.target) && 
                !this.notificationIcon?.contains(e.target)) {
                this.notificationDropdown?.classList.add('hidden');
            }
        });
    }
    
    async fetchNotifications() {
        try {
            console.log('Fetching notifications...');
            const response = await fetch('/users/notifications/');
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to fetch notifications: ${response.status} ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Notifications received:', data);
            
            if (!data.notifications) {
                console.error('Invalid notification data format:', data);
                return;
            }
            
            this.notifications = data.notifications;
            
            // Update UI
            this.updateNotificationCount();
            this.renderNotifications();
            
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }
    
    updateNotificationCount() {
        const count = this.notifications.length;
        console.log('Updating notification count:', count);
        
        if (this.notificationCount) {
            this.notificationCount.textContent = count;
            
            // Show/hide the count badge
            if (count === 0) {
                this.notificationCount.classList.add('hidden');
            } else {
                this.notificationCount.classList.remove('hidden');
            }
            
            console.log('Notification count updated to', count, 'is hidden:', this.notificationCount.classList.contains('hidden'));
        } else {
            console.error('Notification count element not found');
        }
    }
    
    renderNotifications() {
        console.log('Rendering notifications');
        
        if (!this.notificationDropdown) {
            console.error('Notification dropdown element not found');
            return;
        }
        
        if (this.notifications.length === 0) {
            console.log('No notifications to display');
            this.notificationDropdown.innerHTML = `
                <div class="py-3 px-4 text-sm text-gray-400">
                    No new notifications
                </div>
            `;
            return;
        }
        
        console.log('Rendering', this.notifications.length, 'notifications');
        
        try {
            const notificationsHtml = this.notifications
                .map(notification => this.renderNotification(notification))
                .join('');
            
            this.notificationDropdown.innerHTML = notificationsHtml;
            console.log('Notifications rendered successfully');
        } catch (error) {
            console.error('Error rendering notifications:', error);
            this.notificationDropdown.innerHTML = `
                <div class="py-3 px-4 text-sm text-red-400">
                    Error loading notifications
                </div>
            `;
        }
    }
    
    renderNotification(notification) {
        return `
            <a href="${notification.link}" 
               class="block px-4 py-3 hover:bg-gray-700 transition-colors border-b border-gray-700 last:border-0"
               onclick="notificationManager.markAsRead(${notification.id}, event)">
                <div class="flex items-center">
                    <div class="flex-shrink-0 mr-3">
                        ${this.getNotificationIcon(notification.type)}
                    </div>
                    <div class="flex-1">
                        <p class="text-sm text-white">${notification.content}</p>
                        <p class="text-xs text-gray-400 mt-1">
                            ${this.formatDate(notification.created_at)}
                        </p>
                    </div>
                </div>
            </a>
        `;
    }
    
    getNotificationIcon(type) {
        const icons = {
            'celebration': '<i class="fas fa-thumbs-up text-indigo-400"></i>',
            'level_up': '<i class="fas fa-level-up-alt text-green-400"></i>',
            'achievement': '<i class="fas fa-trophy text-yellow-400"></i>',
            'challenge': '<i class="fas fa-flag-checkered text-red-400"></i>'
        };
        return icons[type] || '<i class="fas fa-bell text-gray-400"></i>';
    }
    
    formatDate(isoDate) {
        const date = new Date(isoDate);
        const now = new Date();
        const diff = now - date;
        
        // Less than 1 minute
        if (diff < 60000) return 'Just now';
        
        // Less than 1 hour
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
        }
        
        // Less than 1 day
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours} hour${hours === 1 ? '' : 's'} ago`;
        }
        
        // Format as date
        return date.toLocaleDateString();
    }
    
    async markAsRead(notificationId, event) {
        event.preventDefault();
        console.log('Marking notification as read:', notificationId);
        
        try {
            const csrfToken = getCookie('csrftoken');
            if (!csrfToken) {
                console.error('CSRF token not found');
                return;
            }
            
            const response = await fetch(`/users/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to mark notification as read: ${response.status} ${errorText}`);
            }
            
            // Store the notification link before removing it from the array
            const notification = this.notifications.find(n => n.id === parseInt(notificationId));
            const notificationLink = notification?.link;
            
            console.log('Successfully marked notification as read, removing from list');
            
            // Remove from local list and update UI
            this.notifications = this.notifications.filter(n => n.id !== parseInt(notificationId));
            this.updateNotificationCount();
            this.renderNotifications();
            
            // Navigate to the notification link if it exists
            if (notificationLink) {
                console.log('Navigating to:', notificationLink);
                window.location.href = notificationLink;
            } else {
                console.log('No link found for notification');
            }
            
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
}); 