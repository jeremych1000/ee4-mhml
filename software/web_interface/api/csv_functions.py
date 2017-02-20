import csv, os
from collections import deque
from django.conf import settings


def csv_append(filename, data):
    with open(filename, 'a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(data)
        return True
    return IOError


def csv_insert_header(path, filename, header):
    os.makedirs(path, exist_ok=True)
    open(filename, 'a', newline='').close()
    with open(filename, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(header)
        return True
    return IOError


def get_last_row(filename):
    with open(filename, 'r', newline='') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow


def check_duplicate(name, username=None):
    if username is None:
        path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), name)
    else:
        path = os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), username), name)
    # print("check duplidate Path is ", path)
    return os.path.isfile(path)