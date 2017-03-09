from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from newML.models import *
from newML.functions import *
import os
import sys


class Command(BaseCommand):
    help = "load feature under username from csv files"

    def add_arguments(self, parser):
        parser.add_argument("usernames", nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options["usernames"]:
            userDataPath = os.path.join('.', os.path.join('media', os.path.join('data', username)))
            sys.stdout.write("Path related to username is: " + userDataPath + '\n')
            sys.stdout.write("Loading csv data for " + username + '...')
            if not os.path.isdir(userDataPath):
                raise CommandError("User data path does not exist")
            else:
                filesList = os.listdir(userDataPath)
                for file in filesList:
                    if file.endswith(".csv"):
                        filepath = os.path.join(userDataPath, file)
                        Ds, Fs, Os = CSV2Feature(filepath, 600)
                        userObj = User.objects.get(username=username)
                        if not userObj:
                            raise CommandError("No existing users for name: " + username)
                        else:
                            for d, f, o, in zip(Ds, Fs, Os):
                                d_obj = datetime.strptime(d, '%d/%m/%y %H:%M:%S')
                                try:
                                    FeatureEntry.objects.create(user=userObj, date=d_obj, mean_hr=f[0], std_hr=f[1],
                                                                mean_rr=f[2], std_rr=f[3],
                                                                mean_gsr=f[4], std_gsr=f[5], mean_temp=f[6],
                                                                std_temp=f[7], mean_acc=f[8], kurt_hr=f[9],
                                                                kurt_rr=f[10],
                                                                kurt_gsr=f[11],
                                                                label=o)
                                except IntegrityError:
                                    sys.stdout.write("There is duplcated feature! Skip this feature...\n")
                                    continue
                sys.stdout.write("Done\n")
