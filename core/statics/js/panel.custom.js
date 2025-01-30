document.getElementById('notificationBell').addEventListener('click', function () {
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
});






$(document).ready(function() {
    $(document).on('click', '.item-delete', function(e) {
        e.preventDefault();
        
        const notificationId = $(this).data('notification-id');
        const deleteUrl = `/notifications/${notificationId}/mark-as-read/`;
        
        $.ajax({
            url: deleteUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Django CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // You can either remove the notification or update its style
                    $(e.target).closest('.notification-item').fadeOut();
                    // Or update its appearance:
                    // $(e.target).closest('.notification-item').addClass('read');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error marking notification as read:', error);
                alert('خطا در حذف اعلان');
            }
        });
    });
});

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