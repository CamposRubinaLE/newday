__author__ = 'lucaru9'
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdayDB',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

AWS_S3_ACCESS_KEY_ID = "AKIAIWUY6T6MV2V7JQ4A"  # Your S3 Access Key
AWS_S3_SECRET_ACCESS_KEY = "9J2G58GkW1THCIRbouhFUVS3jgDRe0jwJYMQrPID"  # Your S3 Secret
AWS_STORAGE_BUCKET_NAME = "devnewday"

DEFAULT_FILE_STORAGE = "newday.s3utils.MediaS3BotoStorage"
