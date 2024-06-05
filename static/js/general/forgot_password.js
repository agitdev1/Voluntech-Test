
document.getElementById("forgot-password-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission
    const email = document.getElementById("email").value;
   // Check if the email contains the "@" symbol
   if (!email.includes(".com")) {
        document.getElementById("error-message").innerText = "Please enter a valid email address";
        document.getElementById("success-message").innerText = ""; // Clear any previous success message
        return; // Stop form submission if email is invalid
    }

    // Continue with sending email data to the backend for password reset
    try {
        const response = await fetch("/send-password-reset-email/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email })
        });

        if (response.ok) {
            // If the response is successful, update the DOM with the success message
            document.getElementById("success-message").innerText = "Password reset email sent successfully";
            document.getElementById("error-message").innerText = ""; // Clear any previous error message
        } else {
            // If the response is not successful, display an error message
            document.getElementById("error-message").innerText = "Email entered is not registered.";
            document.getElementById("success-message").innerText = ""; // Clear any previous success message
        }
    } catch (error) {
        // Display error message if there's an error in the fetch request
        document.getElementById("error-message").innerText = "Error sending password reset email. Please try again later.";
        document.getElementById("success-message").innerText = ""; // Clear any previous success message
    }
});
