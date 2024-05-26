from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Регистрация и профиль
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Вход и выход из системы
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name='logout'),

    # Продукты
    path('product/', views.product_list, name='product'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),

    # Поиск
    path('search/', views.search, name='search'),

    # Фильтр
    path('filter/', views.filter_products, name='filter'),

    # Корзина
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),

    # Оформление заказа
    path('checkout/', views.checkout, name='checkout'),

    # Заказы
    path('order/', views.order, name='order'),

    # Обратная связь
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/thanks/', views.FeedbackThanksView.as_view(), name='feedback_thanks'),
]