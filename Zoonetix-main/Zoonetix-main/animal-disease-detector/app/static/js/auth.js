// Auth Form Handling
const loginToggle = document.getElementById('loginToggle');
const signupToggle = document.getElementById('signupToggle');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');

// Form toggle functionality
loginToggle.addEventListener('click', () => {
    loginToggle.classList.add('active');
    signupToggle.classList.remove('active');
    loginForm.classList.add('active');
    signupForm.classList.remove('active');
    clearAllErrors();
    clearAllMessages();
});

signupToggle.addEventListener('click', () => {
    signupToggle.classList.add('active');
    loginToggle.classList.remove('active');
    signupForm.classList.add('active');
    loginForm.classList.remove('active');
    clearAllErrors();
    clearAllMessages();
});

// Password visibility toggle
const togglePasswordBtns = document.querySelectorAll('.toggle-password');
togglePasswordBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const inputId = btn.getAttribute('data-target');
        const input = document.getElementById(inputId);
        if (input.type === 'password') {
            input.type = 'text';
            btn.textContent = '🙈';
        } else {
            input.type = 'password';
            btn.textContent = '👁️';
        }
    });
});

// Clear all error messages
function clearAllErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => {
        msg.classList.remove('show');
        msg.textContent = '';
    });
}

// Clear all form messages
function clearAllMessages() {
    const messages = document.querySelectorAll('.form-message');
    messages.forEach(msg => {
        msg.classList.remove('show', 'success', 'error');
        msg.textContent = '';
    });
}

// Show error message
function showError(fieldId, message) {
    const errorElement = document.getElementById(fieldId + 'Error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

// Show form message
function showMessage(formType, message, isSuccess = false) {
    const messageElement = document.getElementById(formType + 'Message');
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.classList.add('show');
        messageElement.classList.add(isSuccess ? 'success' : 'error');
    }
}

// Show loader
function showLoader(formType, show = true) {
    const loader = document.getElementById(formType + 'Loader');
    const button = document.querySelector(`#${formType}Form button[type="submit"]`);
    if (loader) {
        if (show) {
            loader.classList.add('show');
            button.disabled = true;
        } else {
            loader.classList.remove('show');
            button.disabled = false;
        }
    }
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Login form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors();
    clearAllMessages();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    // Validation
    if (!email) {
        showError('loginEmail', 'Email is required');
        return;
    }
    if (!validateEmail(email)) {
        showError('loginEmail', 'Please enter a valid email');
        return;
    }
    if (!password) {
        showError('loginPassword', 'Password is required');
        return;
    }

    showLoader('login', true);

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage('login', data.detail || 'Login failed', false);
            showLoader('login', false);
            return;
        }

        // Store token in cookie
        document.cookie = `access_token=${data.access_token}; path=/; max-age=2592000`;

        showMessage('login', 'Login successful! Redirecting...', true);
        
        // Redirect to main app after 1 second
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);

    } catch (error) {
        showMessage('login', 'An error occurred. Please try again.', false);
        showLoader('login', false);
    }
});

// Signup form submission
signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors();
    clearAllMessages();

    const email = document.getElementById('signupEmail').value.trim();
    const username = document.getElementById('signupUsername').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validation
    let hasError = false;

    if (!email) {
        showError('signupEmail', 'Email is required');
        hasError = true;
    } else if (!validateEmail(email)) {
        showError('signupEmail', 'Please enter a valid email');
        hasError = true;
    }

    if (!username) {
        showError('signupUsername', 'Username is required');
        hasError = true;
    } else if (username.length < 3) {
        showError('signupUsername', 'Username must be at least 3 characters');
        hasError = true;
    }

    if (!password) {
        showError('signupPassword', 'Password is required');
        hasError = true;
    } else if (password.length < 6) {
        showError('signupPassword', 'Password must be at least 6 characters');
        hasError = true;
    }

    if (!confirmPassword) {
        showError('confirmPassword', 'Please confirm your password');
        hasError = true;
    } else if (password !== confirmPassword) {
        showError('confirmPassword', 'Passwords do not match');
        hasError = true;
    }

    if (hasError) {
        return;
    }

    showLoader('signup', true);

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password,
                confirm_password: confirmPassword
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage('signup', data.detail || 'Registration failed', false);
            showLoader('signup', false);
            return;
        }

        // Store token in cookie
        document.cookie = `access_token=${data.access_token}; path=/; max-age=2592000`;

        showMessage('signup', 'Account created successfully! Redirecting...', true);
        
        // Redirect to main app after 1 second
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);

    } catch (error) {
        showMessage('signup', 'An error occurred. Please try again.', false);
        showLoader('signup', false);
    }
});
