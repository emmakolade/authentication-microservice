from django.core.management.base import BaseCommand
from ...models import StaffID
from ...staff_ids import STAFF_IDS


class Command(BaseCommand):
    help = "add staff codes to the database"

    def handle(self, *args, **options):
        for code in STAFF_IDS:
            StaffID.objects.get_or_create(code=code)
        self.stdout.write(self.style.SUCCESS(
            'staff IDs successfully added to the database'))
        # return super().handle(*args, **options)

        """
        run this command to add staff list to the database:  
        python manage.py add_staff_ids

        """
