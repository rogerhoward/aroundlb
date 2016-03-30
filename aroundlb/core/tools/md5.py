import hashlib, shutil

from django.conf import settings
from celery import shared_task

# import core.tools.media as media
# import core.tools.misc as misc
# import core.tools.md5 as md5


def getmd5(message):    
	return hashlib.md5(message.encode('utf-8')).hexdigest()
	

def getfilemd5(path):
	md5 = hashlib.md5()
	with open(path,'rb') as f: 
	    for chunk in iter(lambda: f.read(8192), b''): 
	         md5.update(chunk)
	return md5.hexdigest()