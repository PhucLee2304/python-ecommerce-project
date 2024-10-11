from django.core.management.base import BaseCommand
from review.utils import importReviewsFromExcel

class Command(BaseCommand):
    help = 'Import reviews from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('review_file_path', type=str, help='Path to the reviews Excel file')

    def handle(self, *args, **kwargs):
        review_file_path = kwargs['review_file_path']
        
        try:
            importReviewsFromExcel(review_file_path)
            self.stdout.write(self.style.SUCCESS('Reviews imported successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing reviews: {e}'))
