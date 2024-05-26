from django.contrib import admin
from .models import Product, Feedback


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    list_filter = ['created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    fieldsets = (
        (None, {'fields': ('name', 'email')}),
        ('Message', {'fields': ('message',)}),
    )

    # Определяем readonly_fields в зависимости от экземпляра
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'email', 'created_at']
        else:
            return ['created_at']