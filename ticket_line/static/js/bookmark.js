document.querySelectorAll('.bookmark-btn').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();

        fetch(button.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // CSRF トークン
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_bookmarked) {
                button.textContent = 'ブックマーク解除';
            } else {
                button.textContent = 'ブックマーク追加';
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
