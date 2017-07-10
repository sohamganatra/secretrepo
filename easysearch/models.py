from django.db import models

from django.utils import timezone

from analytics.settings import BASE_DIR
from .config import *

import re
import textract
import requests
import json
from datetime import datetime


def parse_pdf(pdfname):
    text = textract.process(BASE_DIR + '/pdf/' + pdfname)
    # text = text.decode()
    # pattern = re.compile('^[a-zA-Z0-9_ ]+$')
    # use four space as paragraph delimiter to convert the text into list of paragraphs.
    # convert the /n to four spaces and use four space as the delimiter.
    pattern = re.compile('([^\s\w]|_)+')

    text = text.replace("\n", "    ")
    text = text.replace("\t", "    ")

    # print text

    text = pattern.sub('', text)

    # print "\n"
    # print text

    paragraphs = re.split('\s{4,}', text)

    paragraphs_empty_removed = list(filter(None, paragraphs))

    return paragraphs_empty_removed


class Department(models.Model):
    DEPARTMENT = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.DEPARTMENT


class Segment(models.Model):
    SEGMENT = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.SEGMENT


class Category(models.Model):
    CATEGORY = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.CATEGORY


class Pdf(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, db_index=True)
    segment = models.ForeignKey(
        Segment, on_delete=models.SET_NULL, null=True, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, db_index=True)
    name = models.CharField(max_length=100, primary_key=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self):
        paragraphs = parse_pdf(self.name)
        para_no = 0
        for paragraph in paragraphs:
            para_no = para_no + 1
            print(str(self.time.date()))
            epoch = datetime.utcfromtimestamp(0)
            epoch = epoch.replace(tzinfo=None)
            print(paragraph)
            payload = {
                'information': paragraph,
                'department': self.department.DEPARTMENT,
                'segment': self.segment.SEGMENT,
                'category': self.category.CATEGORY,
                'link': self.name,
                'lastmodified': str((
                    self.time.replace(tzinfo=None) - epoch).total_seconds())
            }
            url = ES_SERVER_INDEX + 'external/' + \
                str(para_no) + self.pk + '?pretty'
            headers = {'Content-type': 'application/json'}
            addition = requests.put(
                url, data=json.dumps(payload), headers=headers)
            print(addition.content)
        super(Pdf, self).save()
