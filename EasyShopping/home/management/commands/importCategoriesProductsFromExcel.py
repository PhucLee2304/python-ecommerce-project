from django.core.management.base import BaseCommand
from home.utils import importCategoriesFromExcel, importProductsFromExcel

class Command(BaseCommand):
    help = 'Import categories and products from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('category_file_path', type=str, help='Path to the categories Excel file')
        parser.add_argument('product_file_path', type=str, help='Path to the products Excel file')

    def handle(self, *args, **kwargs):
        category_file_path = kwargs['category_file_path']
        product_file_path = kwargs['product_file_path']
        
        try:
            importCategoriesFromExcel(category_file_path)
            importProductsFromExcel(product_file_path)
            self.stdout.write(self.style.SUCCESS('Categories and products imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing categories and products: {e}'))
