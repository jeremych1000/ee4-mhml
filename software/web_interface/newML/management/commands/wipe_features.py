from django.core.management.base import BaseCommand, CommandError
from newML.models import *
from newML.functions import *
import os
import sys


class Command(BaseCommand):
    help = "clear all feature under username"

    def add_arguments(self, parser):
        parser.add_argument("usernames", nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options["usernames"]:
            userObj = User.objects.get(username=username)
        if not userObj:
            raise CommandError("No existing users for name: " + username)
        else:
            fobjs = FeatureEntry.objects.all().filter(user=userObj)
            if fobjs.count != 0:
                for f in fobjs:
                    f.delete()
