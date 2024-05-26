// Функция для изменения количества товаров
function changeQuantity(productId, amount) {
    var quantitySpan = document.getElementById('quantity-' + productId);
    var quantityInput = document.getElementById('quantity-input-' + productId);
    var currentQuantity = parseInt(quantitySpan.innerText);
    var newQuantity = currentQuantity + amount;

    // Проверяем, чтобы новое количество товаров было не меньше нуля
    if (newQuantity >= 0) {
        quantitySpan.innerText = newQuantity;
        quantityInput.value = newQuantity;
    }
}