from django.core.management.base import BaseCommand
from productDetail.utils import importSizesFromExcel, importItemsFromExcel

class Command(BaseCommand):
    help = 'Import sizes and items from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('size_file_path', type=str, help='Path to the sizes Excel file')
        parser.add_argument('item_file_path', type=str, help='Path to the items Excel file')

    def handle(self, *args, **kwargs):
        size_file_path = kwargs['size_file_path']
        item_file_path = kwargs['item_file_path']
        
        try:
            importSizesFromExcel(size_file_path)
            importItemsFromExcel(item_file_path)
            self.stdout.write(self.style.SUCCESS('Sizes and items imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing sizes and items: {e}'))
