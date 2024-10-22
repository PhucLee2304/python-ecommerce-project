from django.contrib import admin
from .models import User, Category, Product, Size, Item, UserInterest, Cart, CartItem, Order, Review
from django.utils.html import mark_safe

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  
    min_num = 1
    max_num = 10
    fields = ['item', 'quantity']

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1 
    min_num = 1  
    max_num = 10  
    fields = ['size', 'stockQuantity']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'gender', 'dateOfBirth')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('gender',)
    ordering = ('-date_joined',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryID', 'categoryName')
    search_fields = ('categoryName',)
    ordering = ('categoryName',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'category', 'price', 'getNewPrice', 'featured', 'product_status_icon', 'product_image')
    search_fields = ('productName', 'category__categoryName')
    list_filter = ('category', 'featured')
    ordering = ('-createDate',)  
    inlines = [ItemInline] 

    def product_status_icon(self, obj):
        return mark_safe(f'<span>{obj.get_productStatus_display()}</span>')

    product_status_icon.short_description = 'Status'

    def product_image(self, obj):
        return mark_safe(f'<img src="{obj.productImage.url}" width="50" height="50" />')

    product_image.short_description = 'Product Image'

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('sizeID', 'sizeName')
    search_fields = ('sizeName',)
    ordering = ('sizeName',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemID', 'product', 'size', 'stockQuantity')
    search_fields = ('product__productName', 'size__sizeName')
    ordering = ('product',)

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'timestamp')
    search_fields = ('user__username', 'product__productName')
    ordering = ('-timestamp',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cartID', 'user', 'totalAmount')
    search_fields = ('user__username',)
    ordering = ('user',)
    inlines = [CartItemInline]  

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity')
    search_fields = ('cart__user__username', 'item__product__productName')
    ordering = ('cart',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'user', 'item', 'orderAmount', 'itemQuantity', 'orderStatus', 'orderDate')
    search_fields = ('user__username', 'item__product__productName')
    list_filter = ('orderStatus',)
    ordering = ('-orderDate',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'reviewDate')
    search_fields = ('product__productName', 'user__username', 'rating')
    list_filter = ('rating',)
    ordering = ('-reviewDate',)
