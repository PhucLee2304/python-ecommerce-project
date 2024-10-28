from django.core.management.base import BaseCommand
from core.utils import importProductFromExcel

class Command(BaseCommand):
    help = 'Import product from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('product_file_path', type=str, help='Path to the product Excel file')

    def handle(self, *args, **kwargs):
        product_file_path = kwargs['product_file_path']
        
        try:
            importProductFromExcel(product_file_path)
            self.stdout.write(self.style.SUCCESS('Product imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing products: {e}'))