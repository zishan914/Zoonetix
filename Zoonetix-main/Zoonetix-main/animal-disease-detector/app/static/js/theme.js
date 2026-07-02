const themeStorageKey = 'zoonetixTheme';

function updateThemeButton() {
    const themeToggle = document.getElementById('themeToggleBtn');
    if (!themeToggle) return;
    if (document.body.classList.contains('theme-light')) {
        themeToggle.textContent = '🌙 Dark';
        themeToggle.title = 'Switch to dark mode';
    } else {
        themeToggle.textContent = '☀️ Light';
        themeToggle.title = 'Switch to light mode';
    }
}

function setTheme(theme) {
    document.body.classList.toggle('theme-light', theme === 'light');
    localStorage.setItem(themeStorageKey, theme);
    updateThemeButton();
}

function toggleTheme() {
    const isLight = document.body.classList.contains('theme-light');
    setTheme(isLight ? 'dark' : 'light');
}

function initTheme() {
    const savedTheme = localStorage.getItem(themeStorageKey);
    const theme = savedTheme === 'light' ? 'light' : 'dark';
    setTheme(theme);

    const themeToggle = document.getElementById('themeToggleBtn');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

window.toggleTheme = toggleTheme;
window.addEventListener('load', initTheme);
