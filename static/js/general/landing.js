// JavaScript code to handle form submission
document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Send login data to the backend
    const response = await fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json" // Specify JSON content type
        },
        body: JSON.stringify(loginData) // Convert login data to JSON string
    });

    if (response.ok) {
        // Redirect to the appropriate page based on user type
        const responseData = await response.json();
        if (responseData.user_type === "volunteer") {
            window.location.href = "/volunteer";
        } else if (responseData.user_type === "organization") {
            window.location.href = "/organization";
        } else {
            console.error("Unknown user type");
        }
    } else {
        // Display error message
        const errorMessage = await response.text();
        console.error(errorMessage);
    }
});
