document.getElementById('notificationBell').addEventListener('click', function () {
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
});
document.querySelectorAll('.notification-item').forEach((item) => {
    item.addEventListener('click', function () {
        const notificationId = this.dataset.notificationId;
        fetch(`/notifications/read/${notificationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.remove();  // حذف از لیست
                const badge = document.querySelector('.notification-badge');
                const count = parseInt(badge.textContent) - 1;
                badge.textContent = count > 0 ? count : '';
                badge.style.display = count > 0 ? 'block' : 'none';
            }
        });
    });
});
