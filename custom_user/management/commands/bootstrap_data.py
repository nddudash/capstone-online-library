from django.core.management.base import BaseCommand
from django.db import IntegrityError
from custom_user.models import CustomUser
from django.contrib.auth.hashers import make_password
from book.models import Book

#//////////////////////////////////////////////////////////////////#
#///////////////// DO NOT USE FOR PRODUCTION!!!! /////////////////#
#//////////////////////////////////////////////////////////////////#


class Command(BaseCommand):
    help = "Prepopulates a Database with a basic Admin account, some Books, and some Users."

    def handle(self, *args, **options):
        try:
            # Create a default Admin with default credentials (DO NOT USE IN PRODUCTION!)
            CustomUser.objects.create(
                username="admin",
                password=make_password("password"),
                profile_image="profile.jpg",
                is_staff=True,
                is_superuser=True,
            )

            # Create a Couple users
            CustomUser.objects.create(
                username="NickD",
                password=make_password("something_or_other"),
            )

            CustomUser.objects.create(
                username="LongJohn",
                password=make_password("YarHar"),
            )

            CustomUser.objects.create(
                username="Deetz",
                password=make_password("CheckEm"),
            )

            CustomUser.objects.create(
                username="Suds",
                password=make_password("SpongeB"),
            )

            CustomUser.objects.create(
                username="Shipmaster",
                password=make_password("PortAndStarboard"),
            )

            Book.objects.create(
                gutenberg_id=84,
                title="Frankenstein; Or, The Modern Prometheus",
                author="Shelley, Mary Wollstonecraft",
                copies_available=4,
                text="https://www.gutenberg.org/files/84/84-h.zip",
                image_url = "https://www.gutenberg.org/cache/epub/84/pg84.cover.medium.jpg"
            )

            Book.objects.create(
                gutenberg_id=1080,
                title="A Modest Proposal: For preventing the children of poor people in Ireland, from being a burden on their parents or country, and for making them beneficial to the publick",
                author="Swift, Jonathan",
                copies_available=1,
                text="https://www.gutenberg.org/files/1080/1080-h/1080-h.htm",
                image_url = "https://www.gutenberg.org/cache/epub/1080/pg1080.cover.small.jpg"
            )

            Book.objects.create(
                gutenberg_id=31214,
                title="Broad-Sword and Single-Stick: With Chapters on Quarter-Staff, Bayonet, Cudgel, Shillalah, Walking-Stick, Umbrella and Other Weapons of Self-Defence",
                author="Headley, Rowland George Allanson-Winn, Baron",
                copies_available=2,
                text="https://www.gutenberg.org/files/31214/31214-h/31214-h.htm",
                image_url = "https://www.gutenberg.org/cache/epub/31214/pg31214.cover.small.jpg"
            )

            Book.objects.create(
                gutenberg_id=63256,
                title="The American Diary of a Japanese Girl",
                author="Noguchi, Yoné",
                copies_available=0,
                text="https://www.gutenberg.org/files/63256/63256-h/63256-h.htm",
                image_url = "https://www.gutenberg.org/cache/epub/63256/pg63256.cover.small.jpg"
            )

            Book.objects.create(
                gutenberg_id=27365,
                title="Tales of Space and Time",
                author="Wells, H. G. (Herbert George)",
                copies_available=0,
                text="https://www.gutenberg.org/files/27365/27365-h/27365-h.htm",
                image_url = "https://www.gutenberg.org/cache/epub/27365/pg27365.cover.medium.jpg"
            )

            Book.objects.create(
                gutenberg_id=11,
                title="Alice's Adventures in Wonderland",
                author="Carroll, Lewis",
                copies_available=3,
                text="https://www.gutenberg.org/files/11/11-h/11-h.htm",
                image_url = "https://www.gutenberg.org/cache/epub/11/pg11.cover.medium.jpg"
            )

            self.stdout.write(self.style.SUCCESS(
                'Admin, Users, and Books Successfully Prepopulated!'))

        except IntegrityError:
            existing_users = CustomUser.objects.all()
            existing_books = Book.objects.all()

            self.stderr.write(self.style.WARNING(
                f"""
                Integrity Error Detected! Operation Failed!
                
                Your Database may already contain object's that conflict with
                the attempted Prepopulated Data.
                Existing Users: {existing_users}
                Existing Books: {existing_books}
                """
            ))
