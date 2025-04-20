document.addEventListener('DOMContentLoaded', () => {
    const showLogin = document.getElementById('show-login');
    const showRegister = document.getElementById('show-register');
    const slider = document.getElementById('form-slider');

    showLogin.addEventListener('click', () => {
        slider.style.transform = 'translateX(0%)';
        showLogin.classList.add('active');
        showRegister.classList.remove('active');
    });

    showRegister.addEventListener('click', () => {
        slider.style.transform = 'translateX(-50%)';
        showRegister.classList.add('active');
        showLogin.classList.remove('active');
    });
});

function togglePassword(id) {
    const input = document.getElementById(id);
    input.type = input.type === 'password' ? 'text' : 'password';
}