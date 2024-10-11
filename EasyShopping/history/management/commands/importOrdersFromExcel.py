from django.core.management.base import BaseCommand
from history.utils import importOrdersFromExcel

class Command(BaseCommand):
    help = 'Import orders from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('order_file_path', type=str, help='Path to the orders Excel file')

    def handle(self, *args, **kwargs):
        order_file_path = kwargs['order_file_path']
        
        try:
            importOrdersFromExcel(order_file_path)
            self.stdout.write(self.style.SUCCESS('Orders imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing orders: {e}'))
