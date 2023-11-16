from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from decouple import config
from rest_framework.authtoken.models import Token

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = config("DJANGO_SUPERUSER_USERNAME","shubham")
        email = config('DJANGO_SUPERUSER_EMAIL',"shubhamnath5@gmail.com")
        password = config('DJANGO_SUPERUSER_PASSWORD',"shubham112233")

        if not User.objects.filter(username=username).exists():
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(
                email=email, username=username, password=password)
            token,created = Token.objects.get_or_create(user=admin)
            print(f"Super User Account created, here is the Auth Token {token.key}")
        else:
            print('Admin account has already been initialized.')