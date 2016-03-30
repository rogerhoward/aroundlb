import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import boto3

class Command(BaseCommand):
    args = '<dir>'
    help = 'Testing ingest.'

    def handle(self, *args, **options):
        print 'ingest begin'

        s3_client = boto3.client(
            's3',
            aws_access_key_id='AKIAIEBYN3OQCEYL6A4Q',
            aws_secret_access_key='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',
        )

        # s3 = boto3.resource('s3')
        my_bucket = s3_client.list_objects(Bucket='aroundlb')

        print my_bucket