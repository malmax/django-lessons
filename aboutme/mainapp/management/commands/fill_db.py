from django.core.management.base import BaseCommand
from mainapp.models import Works, Hobby, Learns, Organization
import os


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):

        Organization.objects.all().delete()
        Works.objects.all().delete()
        Hobby.objects.all().delete()
        Learns.objects.all().delete()

        os.system("python manage.py loaddata data.json")
        print("Import completed")