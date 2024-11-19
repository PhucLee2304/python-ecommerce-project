from django.contrib import admin
from .models import User, Category, Product, Size, Item, UserInterest, Cart, CartItem, Order, Review
from django.utils.html import mark_safe
import matplotlib.pyplot as plt
import io
import base64
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncDate

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
    change_list_template = "admin/user/change_list.html"

    def changelist_view(self, request, extra_context=None):
        total_users = User.objects.count()

        current_month = timezone.now().replace(day=1)
        last_day_of_month = current_month.replace(month=current_month.month % 12 + 1, day=1) - timedelta(days=1)

        user_data = (
            User.objects
            .filter(date_joined__gte=current_month, date_joined__lte=last_day_of_month)
            .annotate(day=TruncDay('date_joined'))  
            .values('day') 
            .annotate(user_count=Count('day'))
            .order_by('day')
        )

        chart_labels = [user['day'].day for user in user_data]  
        chart_data = [user['user_count'] for user in user_data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(chart_labels, chart_data, marker='o', linestyle='-', color='b')
        ax.set_title('Users per Day in Current Month')
        ax.set_xlabel('Day')
        ax.set_ylabel('Number of Users')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        extra_context = extra_context or {
            'total_users': total_users,
            'chart_image': img_data,
        }

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryID', 'categoryName')
    search_fields = ('categoryName',)
    ordering = ('categoryName',)
    change_list_template = "admin/category/change_list.html"

    def changelist_view(self, request, extra_context=None):
        total_categories = Category.objects.count()
        
        extra_context = extra_context or {}
        extra_context['total_categories'] = total_categories
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'category', 'price', 'getNewPrice', 'featured', 'product_status_icon', 'product_image')
    search_fields = ('productName', 'category__categoryName')
    list_filter = ('category', 'featured')
    ordering = ('-createDate',)  
    inlines = [ItemInline] 
    change_list_template = "admin/product/change_list.html"

    def product_status_icon(self, obj):
        return mark_safe(f'<span>{obj.get_productStatus_display()}</span>')

    product_status_icon.short_description = 'Status'

    def product_image(self, obj):
        return mark_safe(f'<img src="{obj.productImage.url}" width="50" height="50" />')

    product_image.short_description = 'Product Image'

    def changelist_view(self, request, extra_context=None):
        total_products = Product.objects.count()
        
        category_data = Product.objects.values('category__categoryName').annotate(count=Count('category')).order_by('category__categoryName')
        
        chart_labels = [data['category__categoryName'] for data in category_data]
        chart_data = [data['count'] for data in category_data]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(chart_data, labels=chart_labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        extra_context = extra_context or {}
        extra_context['total_products'] = total_products
        extra_context['category_chart_image'] = img_data 

        return super().changelist_view(request, extra_context=extra_context)
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('sizeID', 'sizeName')
    search_fields = ('sizeName',)
    ordering = ('sizeName',)
    change_list_template = "admin/size/change_list.html"

    def changelist_view(self, request, extra_context=None):
        total_sizes = Size.objects.count()
        
        extra_context = extra_context or {}
        extra_context['total_sizes'] = total_sizes
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemID', 'product', 'size', 'stockQuantity')
    search_fields = ('product__productName', 'size__sizeName')
    ordering = ('product',)
    change_list_template = "admin/item/change_list.html"

    def changelist_view(self, request, extra_context=None):
        total_items = Item.objects.count()
        
        extra_context = extra_context or {}
        extra_context['total_items'] = total_items
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'timestamp', 'numberOfView')
    search_fields = ('user__username', 'category__categoryName')
    ordering = ('-timestamp',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cartID', 'user', 'totalAmount')
    search_fields = ('user__username',)
    ordering = ('user',)
    inlines = [CartItemInline]  

    def change_view(self, request, object_id, form_url='', extra_context=None):
        cart = self.get_object(request, object_id)
        
        total_items = CartItem.objects.filter(cart=cart).count()
        
        extra_context = extra_context or {}
        extra_context['total_items'] = total_items
        
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

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
    change_list_template = "admin/order/change_list.html" 

    def changelist_view(self, request, extra_context=None):
        total_orders = Order.objects.count()

        total_amount = Order.objects.filter(orderStatus='Completed').aggregate(total_amount=Sum('orderAmount'))['total_amount'] or 0

        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)

        orders_this_month = Order.objects.filter(
            orderDate__gte=first_day_of_month,
            orderDate__lte=today,
            orderStatus='Completed' 
        )

        daily_amounts = (
            orders_this_month
            .annotate(day_only=TruncDate('orderDate'))  
            .values('day_only')  
            .annotate(daily_total=Sum('orderAmount'))
            .order_by('day_only')
        )

        daily_data = {entry['day_only']: entry['daily_total'] for entry in daily_amounts}

        all_days_in_month = [first_day_of_month + timedelta(days=i) for i in range((today - first_day_of_month).days + 1)]

        chart_dates = []
        chart_amounts = []
        for day in all_days_in_month:
            chart_dates.append(day.day)  
            chart_amounts.append(daily_data.get(day, 0))  

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(chart_dates, chart_amounts, marker='o', color='b', linestyle='-', label='Total Amount')
        ax.set_title('Daily Order Amounts for This Month')
        ax.set_xlabel('Day')
        ax.set_ylabel('Total Amount')
        ax.grid(True)
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        extra_context = extra_context or {}
        extra_context['total_orders'] = total_orders
        extra_context['total_amount'] = total_amount
        extra_context['daily_data'] = daily_data
        extra_context['chart_image'] = img_data

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'reviewDate')
    search_fields = ('product__productName', 'user__username', 'rating')
    list_filter = ('rating',)
    ordering = ('-reviewDate',)
    change_list_template = "admin/review/change_list.html" 

    def changelist_view(self, request, extra_context=None):
        total_reviews = Review.objects.count() 

        extra_context = extra_context or {}
        extra_context['total_reviews'] = total_reviews 

        return super().changelist_view(request, extra_context=extra_context)

