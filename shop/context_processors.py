from .models import Cart


def is_admin(request):
    return {'user_is_admin': request.user.is_authenticated and request.user.is_staff}


def cart_quantity(request):
    cart_items_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return {'cart_items_count': cart_items_count}