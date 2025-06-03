// Get CSRF Token
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) return decodeURIComponent(cookieValue);
    }
    return null;
}

// Configure Axios with CSRF Token
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');