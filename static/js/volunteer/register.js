// SKILLS MODAL
document.addEventListener("DOMContentLoaded", function() {
    const maxAllowed = 5;

    // Limit for skills checkboxes
    const skillsCheckboxes = document.querySelectorAll('#skillModal input[type="checkbox"]');
    skillsCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            let checkedCount = Array.from(skillsCheckboxes).filter(item => item.checked).length;
            if (checkedCount > maxAllowed) {
                this.checked = false;
                alert('You can select up to ' + maxAllowed + ' skills.');
            }
        });
    });

    // Limit for causes checkboxes
    const causesCheckboxes = document.querySelectorAll('#causesModal input[type="checkbox"]');
    causesCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            let checkedCount = Array.from(causesCheckboxes).filter(item => item.checked).length;
            if (checkedCount > maxAllowed) {
                this.checked = false;
                alert('You can select up to ' + maxAllowed + ' causes.');
            }
        });
    });

    const modal = document.getElementById("skillModal");
    const skillsInput = document.getElementById("skills");
    const closeBtn = document.querySelector(".close");
    const saveBtn = document.getElementById("saveSkills");
    const skillOptions = document.querySelectorAll("#skillOptions input[type='checkbox']");

    // Open modal when skills input is clicked
    skillsInput.addEventListener("click", function() {
        modal.style.display = "flex";
        modal.style.justifyContent = "center";
        modal.style.alignItems = "center";
    });

    // Close modal when close button is clicked
    closeBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Close modal when clicked outside the modal content
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // Save selected skills when save button is clicked
    saveBtn.addEventListener("click", function() {
        const selectedSkills = Array.from(skillOptions)
            .filter(skill => skill.checked)
            .map(skill => skill.value);

        // Update the skills input with selected skills
        skillsInput.value = selectedSkills.join(", ");

        // Close modal after saving
        modal.style.display = "none";
    });
});
// CAUSES MODAL
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("causesModal");
    const closeBtn = document.querySelector("#causesModal .close");
    const saveBtn = document.getElementById("saveCauses");
    const causeOptions = document.querySelectorAll("#causeOptions input[type='checkbox']");

    // Open modal when button is clicked
    const openCausesModalButton = document.getElementById("cause");
    openCausesModalButton.addEventListener("click", function() {
        modal.style.display = "flex";
        modal.style.justifyContent = "center";
        modal.style.alignItems = "center";
    });

    // Close modal when close button is clicked
    closeBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Close modal when clicked outside the modal content
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // Save selected causes when save button is clicked
    saveBtn.addEventListener("click", function() {
        const selectedCauses = Array.from(causeOptions)
            .filter(cause => cause.checked)
            .map(cause => cause.value);

        // Update the form input with selected causes
        const causeInput = document.getElementById("cause");
        causeInput.value = selectedCauses.join(", ");

        // Close modal after saving
        modal.style.display = "none";
    });
});

// Show Password checkbox
const showPasswordCheckbox = document.getElementById("peek");
const passwordInput = document.getElementById("password");

showPasswordCheckbox.addEventListener("change", function() {
    if (this.checked) {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
});

//Form submission
document.addEventListener("DOMContentLoaded", function() {
const form = document.getElementById("volunteerForm");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(form);
    const emailValue = formData.get("email");
    const passwordValue = formData.get("password");

    // Password complexity requirements
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    if (!passwordRegex.test(passwordValue)) {
        alert("Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, and one number.");
        return;
    }

    // Continue with form submission
    try {
        const response = await fetch(`/check_email?email=${emailValue}`, {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error("Failed to check email availability");
        }

        const data = await response.json();

        if (!data.available) {
            const signInInstead = confirm("This email is already registered. Would you like to sign in instead?");
            if (signInInstead) {
                window.location.href = "/"; // Redirect to login page
                return;
            } else {
                return; // Do not proceed with registration
            }
        }
    } catch (error) {
        console.error("Error:", error.message);
        // Optionally, display error message to user
        alert("An error occurred while checking email availability. Please try again later.");
        return;
    }

    // If email is available, continue with form submission
    try {
        const response = await fetch("/register/volunteer", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to submit form");
        }
        // Prompt the user that registration was successful
        window.alert("Registered successfully.");
        setTimeout(function() {
            window.location.href = "/volunteer";
        }, 1000); // 1000 milliseconds = 1 second
    } catch (error) {
        console.error("Error:", error.message);
        // Optionally, display error message to user
        alert("An error occurred while registering. Please try again later.");
    }
});
});

function Showpass() {
var x = document.getElementById("password");
if (x.type === "password") {
x.type = "text";
} else {
x.type = "password";
}
}
