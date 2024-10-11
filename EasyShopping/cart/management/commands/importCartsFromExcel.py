from django.core.management.base import BaseCommand
from cart.utils import importCartsFromExcel, importcartItemsFromExcel

class Command(BaseCommand):
    help = 'Import carts and cartItems from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('cart_file_path', type=str, help='Path to the carts Excel file')
        parser.add_argument('cart_item_file_path', type=str, help='Path to the items Excel file')

    def handle(self, *args, **kwargs):
        category_file_path = kwargs['cart_file_path']
        product_file_path = kwargs['cart_item_file_path']
        
        try:
            importCartsFromExcel(category_file_path)
            importcartItemsFromExcel(product_file_path)
            self.stdout.write(self.style.SUCCESS('Carts and cartItems imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing carts and cartItems: {e}'))
