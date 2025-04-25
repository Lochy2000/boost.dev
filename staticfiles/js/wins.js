// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize celebrate buttons when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Wins.js loaded');
    
    // Handle celebration clicks
    const celebrateButtons = document.querySelectorAll('.celebrate-win');
    console.log('Found celebrate buttons:', celebrateButtons.length);
    
    celebrateButtons.forEach(button => {
        // Get win ID from data attribute
        const winId = button.getAttribute('data-win-id');
        if (!winId) {
            console.error('Button missing data-win-id attribute:', button);
            return;
        }
        
        console.log('Setting up click handler for win:', winId);
        
        // Remove any existing event listeners to prevent duplicates
        button.removeEventListener('click', handleCelebrateClick);
        
        // Add click event listener
        button.addEventListener('click', function(e) {
            e.preventDefault();
            handleCelebrateClick.call(this, winId);
        });
    });
});

// Handle celebrate button click
async function handleCelebrateClick(winId) {
    console.log('Celebrate button clicked for win:', winId);
    
    // Find the count span within this button
    const countSpan = this.querySelector('.celebration-count');
    if (!countSpan) {
        console.error('Could not find celebration count span');
        return;
    }
    
    try {
        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token:', csrfToken ? 'Found' : 'Not found');
        
        if (!csrfToken) {
            console.error('CSRF token not found. Make sure cookies are enabled.');
            return;
        }
        
        // Make the API request
        const response = await fetch(`/wins/celebrate/${winId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Network response was not ok: ${response.status} ${errorText}`);
        }
        
        const data = await response.json();
        console.log('Celebration response:', data);
        
        // Update celebration count
        countSpan.textContent = data.celebration_count;
        
        // Toggle active state
        if (data.is_celebrated) {
            this.classList.add('text-indigo-400');
            this.classList.remove('text-gray-400');
        } else {
            this.classList.remove('text-indigo-400');
            this.classList.add('text-gray-400');
        }
        
    } catch (error) {
        console.error('Error celebrating win:', error);
    }
}