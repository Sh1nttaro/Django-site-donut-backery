// Проверяем, есть ли информация о темном режиме в Local Storage
if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode'); // Включаем темный режим
}

// Обработчик нажатия на кнопку переключения темного режима
document.getElementById('toggle-dark-mode').addEventListener('click', function() {
    // Переключаем состояние темного режима
    document.body.classList.toggle('dark-mode');
    // Сохраняем состояние в Local Storage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('dark-mode', 'enabled');
    } else {
        localStorage.removeItem('dark-mode');
    }
});