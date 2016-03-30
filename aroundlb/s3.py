#!/usr/bin/env python

import os
import boto3
import pprint

s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAIEBYN3OQCEYL6A4Q',
    aws_secret_access_key='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',
)

# s3 = boto3.resource('s3')
my_bucket = s3_client.list_objects(Bucket='aroundlb')

pprint.pprint(my_bucket)