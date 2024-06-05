document.addEventListener('DOMContentLoaded', function() {
    const skillModal = document.getElementById('skillModal');
    const causeModal = document.getElementById('causesModal');
    const skillButton = document.getElementById('skills');
    const causeButton = document.getElementById('cause');
    const saveSkillsButton = document.getElementById('saveSkills');
    const saveCausesButton = document.getElementById('saveCauses');
    const skillCheckboxes = document.querySelectorAll('#skillOptions input[type="checkbox"]');
    const causeCheckboxes = document.querySelectorAll('#causeOptions input[type="checkbox"]');

    // Open modals
    skillButton.addEventListener('click', () => {
        skillModal.style.display = 'flex';
        skillModal.style.transform = 'translate(0, 0)';
    });
    causeButton.addEventListener('click', () => {
        causeModal.style.display = 'flex';
        causeModal.style.transform = 'translate(0, 0)';
    });

    // Close modals
    document.querySelectorAll('.close').forEach(closeButton => {
        closeButton.addEventListener('click', () => {
            skillModal.style.display = 'none';
            causeModal.style.display = 'none';
        });
    });

    // Save skills and causes
    function saveSelections(inputField, checkboxes, modal, saveButton) {
        saveButton.addEventListener('click', () => {
            let selectedItems = [];
            checkboxes.forEach(checkbox => {
                if (checkbox.checked) selectedItems.push(checkbox.value);
            });
            inputField.value = selectedItems.join(', ');
            modal.style.display = 'none';
        });
    }

    saveSelections(skillButton, skillCheckboxes, skillModal, saveSkillsButton);
    saveSelections(causeButton, causeCheckboxes, causeModal, saveCausesButton);

    // Enforce maximum of 3 selections
    function enforceMaxSelections(checkboxes) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                let checkedCount = Array.from(checkboxes).filter(c => c.checked).length;
                if (checkedCount > 3) {
                    checkbox.checked = false;
                    alert('You can select a maximum of 3 items.');
                }
            });
        });
    }

    enforceMaxSelections(skillCheckboxes);
    enforceMaxSelections(causeCheckboxes);

    document.getElementById('createOpportunityForm').onsubmit = async function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        const opportunityData = {
            organizer: data.organizer,
            name: data.name,
            description: data.description,
            limit: parseInt(data.limit, 10),
            start_date: data.startDate,
            end_date: data.endDate,
            location: data.location,
            skills: data.skills.split(', ').map(skill => skill.trim()),
            cause: data.cause.split(', ').map(cause => cause.trim())
        };

        if (!validateOpportunityData(opportunityData)) {
            alert('Invalid data provided.');
            return;
        }

        try {
            const response = await fetch('/create-opportunity/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(opportunityData)
            });

            if (response.ok) {
                alert('Opportunity created successfully!');
                window.location.reload();
            } else {
                const responseData = await response.json();
                alert('Failed to create opportunity: ' + (responseData.detail || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + JSON.stringify(error.message));
        }
    };

    function validateOpportunityData(data) {
        return true;
    }
});