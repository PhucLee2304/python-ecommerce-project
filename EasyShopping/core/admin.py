from django.contrib import admin
from .models import User, Category, Product, Size, Item, UserInterest, Cart, CartItem, Order, Review
from django.utils.html import mark_safe

# Inline for CartItems related to a Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Number of empty forms displayed
    min_num = 1
    max_num = 10
    fields = ['item', 'quantity']

# Inline for Items related to a Product
class ItemInline(admin.TabularInline):
    model = Item
    extra = 1  # Number of empty forms displayed
    min_num = 1  # Minimum number of items required
    max_num = 10  # Maximum number of items allowed
    fields = ['size', 'stockQuantity']

# Cấu hình UserAdmin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'gender', 'dateOfBirth')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('gender',)
    ordering = ('-date_joined',)

# Cấu hình CategoryAdmin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryID', 'categoryName')
    search_fields = ('categoryName',)
    ordering = ('categoryName',)

# Cấu hình ProductAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'category', 'price', 'getNewPrice', 'inStock', 'featured', 'product_status_icon', 'product_image')
    search_fields = ('productName', 'category__categoryName')
    list_filter = ('category', 'inStock', 'featured')
    ordering = ('-date',)
    inlines = [ItemInline]  # Display Items inline within the Product admin

    def product_status_icon(self, obj):
        return mark_safe(f'<span>{obj.get_productStatus_display()}</span>')

    product_status_icon.short_description = 'Status'

    def product_image(self, obj):
        return mark_safe(f'<img src="{obj.productImage.url}" width="50" height="50" />')

    product_image.short_description = 'Product Image'

# Cấu hình SizeAdmin
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('sizeID', 'sizeName')
    search_fields = ('sizeName',)
    ordering = ('sizeName',)

# Cấu hình ItemAdmin
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemID', 'product', 'size', 'stockQuantity')
    search_fields = ('product__productName', 'size__sizeName')
    ordering = ('product',)

# Cấu hình UserInterestAdmin
@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'timestamp')
    search_fields = ('user__username', 'product__productName')
    ordering = ('-timestamp',)

# Cấu hình CartAdmin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cartID', 'user', 'totalAmount')
    search_fields = ('user__username',)
    ordering = ('user',)
    inlines = [CartItemInline]  # Display CartItems inline within the Cart admin

# Cấu hình CartItemAdmin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity')
    search_fields = ('cart__user__username', 'item__product__productName')
    ordering = ('cart',)

# Cấu hình OrderAdmin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'user', 'item', 'orderAmount', 'itemQuantity', 'orderStatus', 'orderDate')
    search_fields = ('user__username', 'item__product__productName')
    list_filter = ('orderStatus',)
    ordering = ('-orderDate',)

# Cấu hình ReviewAdmin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'reviewDate')
    search_fields = ('product__productName', 'user__username', 'rating')
    list_filter = ('rating',)
    ordering = ('-reviewDate',)
