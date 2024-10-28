from django.core.management.base import BaseCommand
from core.utils import importSizeFromExcel

class Command(BaseCommand):
    help = 'Import size from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('size_file_path', type=str, help='Path to the size Excel file')

    def handle(self, *args, **kwargs):
        size_file_path = kwargs['size_file_path']
        
        try:
            importSizeFromExcel(size_file_path)
            self.stdout.write(self.style.SUCCESS('Size imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing sizes: {e}'))
