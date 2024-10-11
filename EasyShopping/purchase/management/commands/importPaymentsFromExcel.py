from django.core.management.base import BaseCommand
from purchase.utils import importPaymentsFromExcel

class Command(BaseCommand):
    help = 'Import payments from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('payment_file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        payment_file_path = kwargs['payment_file_path']
        importPaymentsFromExcel(payment_file_path)
        self.stdout.write(self.style.SUCCESS('Payments imported successfully!'))