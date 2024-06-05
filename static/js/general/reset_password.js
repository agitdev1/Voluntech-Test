document.getElementById("reset-password-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission

    const newPassword = document.getElementById("new-password").value;
    const confirmNewPassword = document.getElementById("confirm-new-password").value;

    // Extract the token from the URL query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    // Check if the new password and confirm new password match
    if (newPassword !== confirmNewPassword) {
        document.getElementById("error-message").innerText = "Passwords do not match";
        document.getElementById("success-message").innerText = ""; // Clear any previous success message
        return; // Stop form submission if passwords do not match
    }

    // Continue with sending new password data to the backend for password reset
    try {
        const response = await fetch("/reset-password/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ token: token, new_password: newPassword })
        });

                if (response.ok) {
        document.getElementById("success-message").innerText = "Password reset successfully. Redirecting to login page...";
        document.getElementById("error-message").innerText = ""; // Clear any previous error message
        // Redirect to the login page after successful password reset
        setTimeout(function() {
            window.location.href = "/";
        }, 3000); // Delay of 3000 milliseconds (3 seconds)
    } else {
            // If the response is not successful, display an error message
            const errorData = await response.json();
            document.getElementById("error-message").innerText = errorData.detail || "Error resetting password. Please try again later.";
            document.getElementById("success-message").innerText = ""; // Clear any previous success message
        }
    } catch (error) {
        // Display error message if there's an error in the fetch request
        document.getElementById("error-message").innerText = "Error resetting password. Please try again later.";
        document.getElementById("success-message").innerText = ""; // Clear any previous success message
    }
});
