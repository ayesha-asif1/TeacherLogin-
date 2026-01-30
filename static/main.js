document.addEventListener('DOMContentLoaded', function () {
    const splashScreen = document.getElementById('splash-screen');
    const loginPage = document.getElementById('login-page');
    const loginContainer = document.querySelector('.login-container');
    const letters = document.querySelectorAll('.letter');

    // Animate letters one by one
    letters.forEach((letter, index) => {
        setTimeout(() => {
            letter.style.animation = `letterAppear 0.8s ease forwards`;
            letter.style.opacity = '1';
            letter.style.transform = 'translateY(0)';
        }, index * 600);
    });

    // Add CSS for letter animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes letterAppear {
            0% { 
                opacity: 0;
                transform: translateY(30px);
            }
            100% { 
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // After animations complete, show login page
    setTimeout(() => {
        // Hide splash screen
        splashScreen.style.opacity = '0';

        // Show login page with animation
        setTimeout(() => {
            splashScreen.style.display = 'none';
            loginPage.style.opacity = '1';
            loginPage.style.visibility = 'visible';

            // Animate login container
            setTimeout(() => {
                loginContainer.style.opacity = '1';
                loginContainer.style.transform = 'translateY(0)';
            }, 300);
        }, 1000);
    }, 6500); // Total animation time

    // Add click events to login options
    document.getElementById('student-login').addEventListener('click', function () {
        alert('Student login selected. In a real application, this would redirect to the student login page.');
    });

    document.getElementById('teacher-login').addEventListener('click', function () {
        // Hide options and show form
        document.getElementById('login-options').style.display = 'none';
        const form = document.getElementById('teacher-login-form');
        form.style.display = 'block';
        form.style.opacity = '1';
        form.style.visibility = 'visible';
    });

    document.getElementById('back-to-options').addEventListener('click', function () {
        // Hide form and show options
        document.getElementById('teacher-login-form').style.display = 'none';
        document.getElementById('login-options').style.display = 'flex';
    });

    document.getElementById('admin-login').addEventListener('click', function () {
        alert('Administrator login selected. In a real application, this would redirect to the admin login page.');
    });
});