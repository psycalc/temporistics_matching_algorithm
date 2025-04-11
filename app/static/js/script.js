// scripts.js

// You can add your custom JavaScript code here

// Функція для відправки форми зміни мови
function submitLanguageForm() {
    console.log("========== ЗМІНА МОВИ ==========");
    console.log("Функція submitLanguageForm викликана");
    
    // Отримаємо форму
    const form = document.getElementById('languageForm');
    if (!form) {
        console.error("ПОМИЛКА: Форма мови не знайдена на сторінці");
        return;
    }
    
    // Перевіряємо поточне значення мови
    const select = document.getElementById('languageSelect');
    if (!select) {
        console.error("ПОМИЛКА: Селектор мови не знайдено");
        return;
    }
    
    const selectedLanguage = select.value;
    
    // Перевіряємо обрану мову
    if (!selectedLanguage) {
        console.error("ПОМИЛКА: Не вибрано мову");
        return;
    }
    
    console.log(`Вибрана мова: ${selectedLanguage}`);
    console.log(`Поточні cookies: ${document.cookie}`);
    
    // Перевіряємо наявність CSRF токену
    const csrfToken = document.getElementById('language_csrf_token');
    if (!csrfToken) {
        console.error("ПОМИЛКА: CSRF токен не знайдено");
        return;
    }
    
    console.log(`CSRF токен присутній: ${csrfToken.name}`);
    
    // Перевіряємо атрибути форми
    console.log(`Форма action: ${form.action}`);
    console.log(`Форма method: ${form.method}`);
    
    // Додаємо обробник події для відловлювання результату відправки форми
    form.onsubmit = function(e) {
        console.log("Форма відправляється...");
        // Не блокуємо стандартну поведінку, даємо формі відправитись
    };
    
    // Відправляємо форму програмно
    console.log("Надсилаємо форму зміни мови...");
    try {
        form.submit();
        console.log("Форма успішно відправлена");
    } catch (error) {
        console.error(`ПОМИЛКА при відправці форми: ${error.message}`);
    }
    console.log("========== КІНЕЦЬ ЗМІНИ МОВИ ==========");
}

// Перевіряємо поточну мову при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    console.log("========== ЗАВАНТАЖЕННЯ СТОРІНКИ ==========");
    console.log(`Поточні cookies: ${document.cookie}`);
    
    // Функція для отримання значення з cookie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            const cookieValue = parts.pop().split(';').shift();
            console.log(`Знайдено cookie ${name}=${cookieValue}`);
            return cookieValue;
        }
        console.log(`Cookie ${name} не знайдено`);
        return null;
    }
    
    // Перевіряємо наявність мови в cookie
    const currentLocale = getCookie('locale');
    console.log(`Поточна локаль з cookie: ${currentLocale || 'не встановлена'}`);
    
    // Перевіряємо перемикач мови
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        console.log("Знайдено перемикач мови");
        
        if (currentLocale) {
            console.log(`Встановлюємо значення перемикача у ${currentLocale}`);
            languageSelect.value = currentLocale;
        } else {
            console.log(`Залишаємо значення перемикача за замовчуванням: ${languageSelect.value}`);
        }
    } else {
        console.log("Перемикач мови не знайдено на сторінці");
    }
    
    // Перевіряємо форму зміни мови
    const languageForm = document.getElementById('languageForm');
    if (languageForm) {
        console.log("Знайдено форму зміни мови");
        console.log(`Форма action: ${languageForm.action}`);
        console.log(`Форма method: ${languageForm.method}`);
    } else {
        console.log("Форму зміни мови не знайдено на сторінці");
    }
    console.log("========== КІНЕЦЬ ЗАВАНТАЖЕННЯ СТОРІНКИ ==========");
});
