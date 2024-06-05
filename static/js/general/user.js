function logout() {
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin'  // Include cookies in the request
    })
    .then(response => {
        if (response.ok) {
            // Redirect to the home page after logout
            window.location.href = '/';
        } else {
            // Handle error
            console.error('Failed to logout');
        }
    })
    .catch(error => {
        // Handle network error
        console.error('Network error:', error);
    });
}
// Redirect to the edit profile page
document.getElementById("edit-btn").addEventListener("click", function() {
    window.location.href = "/edit-profile"; // Route for editing profile
});