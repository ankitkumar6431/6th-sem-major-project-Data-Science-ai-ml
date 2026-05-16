document.addEventListener('DOMContentLoaded', function () {
    const loginContainer = document.getElementById('login-container');
    const registerContainer = document.getElementById('register-container');
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');

    // Show Login Form by Default
    loginContainer.classList.add('active');

    // Show Register Form
    if (showRegister) {
        showRegister.addEventListener('click', function (e) {
            e.preventDefault();
            loginContainer.classList.remove('active');
            registerContainer.classList.add('active');
        });
    }

    // Show Login Form
    if (showLogin) {
        showLogin.addEventListener('click', function (e) {
            e.preventDefault();
            registerContainer.classList.remove('active');
            loginContainer.classList.add('active');
        });
    }
});