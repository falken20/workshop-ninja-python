#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import os
import cloudstorage as gcs
import logging

from google.appengine.api import app_identity


# Variables para acceso a Cloud Storage
CLOUD_STORAGE_BUCKET = 'workshop-ninja-python.appspot.com'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# [START retries]
gcs.set_default_retry_params(
    gcs.RetryParams(
        initial_delay=0.2, 
        max_delay=5.0, 
        backoff_factor=2, 
        max_retry_period=15
        ))
# [END retries]


# [START get_default_bucket]
def get_bucket():
    bucket_name = CLOUD_STORAGE_BUCKET

    logging.info('WNP: Obtenemos el nombre del bucket --> %s', bucket_name)
    return bucket_name
# [END get_default_bucket]


# [START write]
def upload_file(fileUpload, fileName):
    """Upload a file."""

    pathFileGCS = "/" + get_bucket() + "/" + fileName

    fileType = fileUpload.type
    fileContent = fileUpload.file.read()

    logging.info('WNP: Creando fichero %s de tipo %s en GCS', format(pathFileGCS), fileType)

    fileGCS = gcs.open(pathFileGCS, 'w', content_type=fileType, retry_params=gcs.RetryParams(backoff_factor=1.1))
    #fileGCS.write(fileContent)
    fileGCS.write('abcd\n')
    fileGCS.close

    listBucket = gcs.listbucket("/" + get_bucket())
    logging.info('>'.join([i.filename for i in listBucket]))
    
    logging.info('WNP: Fichero %s creado en GCS', format(pathFileGCS))
    
    imageUrlGCS = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':get_bucket(), 'file':fileName}
    return imageUrlGCS
# [END write]

# [START read]
def read_file(self, fileName):
    self.response.write(
        'Abbreviated file content (first line and last 1K):\n')

    with gcs.open(fileName) as cloudstorage_file:
        self.response.write(cloudstorage_file.readline())
        gcs.seek(-1024, os.SEEK_END)
        self.response.write(cloudstorage_file.read())
# [END read]

def stat_file(self, fileName):
    self.response.write('File stat:\n')

    stat = gcs.stat(fileName)
    self.response.write(repr(stat))


# [START delete_files]
def delete_files(self):
    self.response.write('Deleting files...\n')
    for fileName in self.tmp_filenames_to_clean_up:
        self.response.write('Deleting file {}\n'.format(fileName))
        try:
            gcs.delete(fileName)
        except gcs.NotFoundError:
            pass
# [END delete_files]

