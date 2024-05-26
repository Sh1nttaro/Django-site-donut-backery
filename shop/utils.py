import os
from django.utils.text import slugify


def product_image_path(instance, filename):
    # Получаем расширение файла
    extension = os.path.splitext(filename)[1]
    # Генерируем имя файла, используя название продукта
    filename = slugify(instance.name) + extension
    # Возвращаем путь в формате 'products/имя_картинки.png'
    return os.path.join('products', filename)
