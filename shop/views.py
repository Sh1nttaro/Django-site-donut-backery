from django.db.models import Sum
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ProductForm, FeedbackForm, OrderForm, ProfileForm
from .models import Product, Order, Profile, Cart, CartItem, OrderItem
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


# Вкладка Home
def home(request):
    products = Product.objects.all()[:4]  # Получаем первые 4 товара для отображения на главной странице
    return render(request, 'shop/home.html', {'products': products})


# Вкладка Register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required  # Проверка на авторизацию пользователя
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)  # Получаем или создаем профиль пользователя
    orders = Order.objects.filter(user=request.user)  # Получаем заказы пользователя

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'shop/profile.html', {'user': request.user, 'form': form, 'orders': orders})


# Вкладка Add_product
@login_required  # Проверка на авторизацию пользователя
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage(location='static/products/')  # Указываем папку для сохранения изображений
                filename = fs.save(image.name, image)
                product.image = 'products/' + filename  # Генерируем адрес изображения
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


# Вкладка Search
def search(request):
    query = request.GET.get('q')  # Получаем поисковый запрос
    sort_by = request.GET.get('sort_by')  # Получаем параметр сортировки
    all_products = Product.objects.all()  # Получаем все продукты для использования в шаблоне

    # Фильтруем товары по запросу
    products = Product.objects.filter(name__icontains=query) if query else all_products

    # Применяем сортировку, если параметр сортировки указан
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'alphabetical':
        products = products.order_by('name')

    # Передаем оба списка продуктов в контексте
    return render(request, 'shop/search.html', {'products': products, 'all_products': all_products})


# Вкладка Edit
@login_required  # Проверка на авторизацию пользователя
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)  # Получаем товар или выводим ошибку 404
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('add_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

# Вкладка Feedback
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            if request.user.is_authenticated:
                feedback_instance.name = request.user.username
                feedback_instance.email = request.user.email
            feedback_instance.save()
            return render(request, 'shop/feedback_thanks.html', {'user_info': {'username': feedback_instance.name, 'email': feedback_instance.email}})
    else:
        form = FeedbackForm()
    return render(request, 'shop/feedback.html', {'form': form})


class FeedbackThanksView(TemplateView):
    template_name = "shop/feedback_thanks.html"


# Вкладка Filter
def filter_products(request):
    products = Product.objects.all()  # Получаем все товары
    price_from = request.GET.get('price_from')  # Минимальная цена
    price_to = request.GET.get('price_to')  # Максимальная цена
    if price_from:
        products = products.filter(price__gte=price_from)  # Фильтруем товары по минимальной цене
    if price_to:
        products = products.filter(price__lte=price_to)  # Фильтруем товары по максимальной цене
    return render(request, 'shop/filter_results.html', {'products': products})


# Вкладка Order
@login_required  # Проверка на авторизацию пользователя
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('order')
    else:
        form = OrderForm()
    return render(request, 'shop/order.html', {'form': form})


# Вкладка Product
def product_list(request):
    all_products = Product.objects.all()  # Получаем все товары
    return render(request, 'shop/product.html', {'all_products': all_products})


# Вкладка Delete Product
@login_required  # Проверка на авторизацию пользователя
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)  # Получаем товар или выводим ошибку 404
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product')
    return render(request, 'shop/delete_product.html', {'product': product})


# Вкладка View Cart
@login_required  # Проверка на авторизацию пользователя
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)  # Получаем или создаем корзину пользователя
    cart_items = cart.items.all()  # Получаем все элементы корзины
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Рассчитываем общую стоимость для каждого элемента корзины
    return render(request, 'shop/cart.html', {'cart_items': cart_items})


# Вкладка Update Cart
@login_required  # Проверка на авторизацию пользователя
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)  # Получаем элемент корзины или выводим ошибку 404
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')


# Вкладка Checkout
@login_required  # Проверка на авторизацию пользователя
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)  # Получаем корзину пользователя или выводим ошибку 404
    cart_items = cart.items.all()  # Получаем все элементы корзины

    if request.method == 'POST':
        if cart_items:
            order, _ = Order.objects.get_or_create(user=request.user)  # Получаем или создаем заказ
            for item in cart_items:
                order_item, created = OrderItem.objects.get_or_create(order=order, product=item.product)
                if not created:
                    order_item.quantity += item.quantity
                    order_item.save()
                else:
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            cart.delete()  # Очищаем корзину после оформления заказа
            messages.success(request, 'Order placed successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Your cart is empty. Add items before checking out.')
            return redirect('cart')
    else:
        return render(request, 'shop/checkout.html', {'cart_items': cart_items})


# Вкладка Add to Cart
@login_required  # Проверка на авторизацию пользователя
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, pk=product_id)  # Получаем товар или выводим ошибку 404
        cart, _ = Cart.objects.get_or_create(user=request.user)  # Получаем или создаем корзину пользователя

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return redirect('cart')
    return HttpResponseBadRequest("Invalid request method")


# Вкладка Remove from Cart
@login_required  # Проверка на авторизацию пользователя
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        # Получаем все элементы корзины с заданным item_id
        cart_items = CartItem.objects.filter(id=item_id)

        # Удаляем каждый элемент корзины
        for cart_item in cart_items:
            cart_item.delete()

        # Пересчитываем общую стоимость корзины
        cart_total = 0
        cart = cart_items[0].cart if cart_items else None
        if cart:
            cart_total = cart.items.aggregate(total=Sum('product__price'))['total'] or 0

        return JsonResponse({'cart_total': cart_total})

    return JsonResponse({'error': 'Invalid request'}, status=400)