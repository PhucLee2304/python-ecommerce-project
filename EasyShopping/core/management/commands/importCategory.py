from django.core.management.base import BaseCommand
from core.utils import importCategoryFromExcel

class Command(BaseCommand):
    help = 'Import category from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('category_file_path', type=str, help='Path to the category Excel file')

    def handle(self, *args, **kwargs):
        category_file_path = kwargs['category_file_path']
        
        try:
            importCategoryFromExcel(category_file_path)
            self.stdout.write(self.style.SUCCESS('Category imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing categories: {e}'))