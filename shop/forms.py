from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, Order, Profile, Feedback, CartItem


# Форма регистрации пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма профиля
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']


# Форма продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


# Форма обратной связи
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


# Форма поиска продукта
class ProductSearchForm(forms.Form):
    GLAZING_CHOICES = [
        ('', 'Выберите глазурь'),
        ('chocolate', 'Шоколадная'),
        ('vanilla', 'Ванильная'),
    ]
    SORT_BY_CHOICES = [
        ('', 'Сортировать по'),
        ('name', 'Названию'),
        ('price_asc', 'Цене (по возрастанию)'),
        ('price_desc', 'Цене (по убыванию)'),
    ]
    min_price = forms.DecimalField(label='Минимальная цена', required=False)
    glazing = forms.ChoiceField(label='Глазурь', choices=GLAZING_CHOICES, required=False)
    sort_by = forms.ChoiceField(label='Сортировать по', choices=SORT_BY_CHOICES, required=False)


# Форма заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []


# Функция для удаления элемента из корзины
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        cart_total = sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart_item.cart))
        return JsonResponse({'cart_total': cart_total})
    return JsonResponse({'error': 'Invalid request'}, status=400)