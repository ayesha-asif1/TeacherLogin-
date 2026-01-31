document.addEventListener('DOMContentLoaded', function() {
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
    document.getElementById('student-login').addEventListener('click', function() {
        window.location.href = "/student_info"
    });
    
    document.getElementById('teacher-login').addEventListener('click', function() {
        window.location.href = "/login"
    });
    
    document.getElementById('admin-login').addEventListener('click', function() {
        window.location.href = "/login"
    });
});
// Add this inside your existing window.addEventListener('DOMContentLoaded', ... )

const currentPath = window.location.pathname;

// 1. If we are on the login page, skip or hide the splash screen immediately
if (currentPath === "/login") {
    const splash = document.getElementById('splash-screen');
    const loginPage = document.getElementById('login-page');
    const loginContainer = document.querySelector('.login-container');

    if (splash) splash.style.display = 'none'; // No splash on login
    
    if (loginPage) {
        loginPage.style.opacity = '1';
        loginPage.style.visibility = 'visible';
    }
    
    if (loginContainer) {
        loginContainer.style.opacity = '1';
        loginContainer.style.transform = 'translateY(0)';
    }
    
    // Allow scrolling on the login page
    document.body.style.overflow = 'auto';
}

// 2. Simple Client-side validation for the login form
const loginForm = document.querySelector('form');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        const password = document.querySelector('input[type="password"]').value;
        
        if (password.length < 3) {
            e.preventDefault();
            alert("Password is too short!");
        }
    });
}
// Function to open the Edit Modal with existing data
function openEditModal(entry) {
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Edit Class';
    document.getElementById('entryId').value = entry.id;
    document.getElementById('day').value = entry.day;
    document.getElementById('subject').value = entry.subject;
    document.getElementById('start_time').value = entry.start_time;
    document.getElementById('end_time').value = entry.end_time;
    document.getElementById('room').value = entry.room;
    
    document.getElementById('addModal').style.display = 'flex';
}

function openModal() {
    // Clear all fields for a fresh look
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-calendar-plus"></i> Add New Class';
    document.getElementById('entryId').value = "";
    document.getElementById('subject').value = "";
    document.getElementById('room').value = "";
    document.getElementById('start_time').value = "";
    document.getElementById('end_time').value = "";
    
    document.getElementById('addModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('addModal').style.display = 'none';
}
function saveClass() {
    const entryData = {
        action: 'add',
        day: document.getElementById('day').value,
        subject: document.getElementById('subject').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
        room: document.getElementById('room').value
    };

    fetch('/api/timetable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entryData)
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            closeModal();
            location.reload(); 
        }
    });
}

function deleteEntry(id) {
    if(confirm("Are you sure you want to delete this class?")) {
        fetch('/api/timetable', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ action: 'delete', id: id })
        }).then(() => location.reload());
    }
}