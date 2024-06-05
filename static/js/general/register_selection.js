    const sections = document.querySelectorAll('.section');

    sections.forEach(section => {
      section.addEventListener('click', handleSignup);
    });

    function handleSignup(event) {
      const signupType = event.currentTarget.dataset.registerType;
      window.location.href = `/register/${signupType}`;
    }
