from django.core.management.base import BaseCommand
from core.utils import importItemFromExcel

class Command(BaseCommand):
    help = 'Import item from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('item_file_path', type=str, help='Path to the item Excel file')

    def handle(self, *args, **kwargs):
        item_file_path = kwargs['item_file_path']
        
        try:
            importItemFromExcel(item_file_path)
            self.stdout.write(self.style.SUCCESS('Item imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing items: {e}'))
