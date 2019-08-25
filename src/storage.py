#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import os
import cloudstorage as gcs
import logging


# Variables para acceso a Cloud Storage
CLOUD_STORAGE_BUCKET = 'bucket-ninja'

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


# [START is_local]
def is_local():
    """ Check para ver si estamos ejecutando en localhost o en GAE """

    logging.info('SERVER_NAME: %s', os.environ.get('SERVER_NAME'))

    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    else:
        return False
# [END is_local]


# [START write]
def upload_file(fileUpload, fileName):
    """Upload a file to GCS"""

    pathFileGCS = "/" + get_bucket() + "/" + fileName

    fileType = fileUpload.type
    fileContent = fileUpload.file.read()

    logging.info('WNP: Creando fichero %s de tipo %s en GCS', format(pathFileGCS), fileType)

    fileGCS = gcs.open(pathFileGCS, 'w', content_type=fileType)
    fileGCS.write(fileContent)
    fileGCS.close
    
    ######
    
    pathFileGCS = '/bucket-ninja/folder/ninja.jpg'
    fileGCS = gcs.open(pathFileGCS, 'w', content_type='text/plain')
    fileGCS.write('abcd\n')
    fileGCS.close
    logging.info('********* Contenido buffer: %s', repr(fileGCS))
    list_bucket("/" + get_bucket())
    stat_file('/bucket-ninja/AppleAtari.jpg')
    read_file('/bucket-ninja/AppleAtari.jpg')

    ######    
    
    logging.info('WNP: Fichero %s creado en GCS', format(pathFileGCS))
    
    # Montamos la url de la imagen de dependiendo si esta ejecutando en local o en GAE
    imageUrlGCS = 'http://localhost:8080/_ah/gcs' if is_local() else 'https://storage.googleapis.com'
    imageUrlGCS += pathFileGCS
    # imageUrlGCS = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':get_bucket(), 'file':fileName}
    
    return imageUrlGCS
# [END write]

# [START delete_files]
def delete_file(fileName):
    try:
        gcs.delete(fileName)
        logging.info('WNP: Archivo %s eliminado en GCS', fileName)
    except gcs.NotFoundError:
        logging.error('WNP: El archivo %s no se ha podido eliminar, no ha sido encontrado', fileName)
# [END delete_files]


# [START read]
def read_file(fileName):
    logging.info('WNP: Leyendo fichero %s', fileName)
    fileGCS =  gcs.open(fileName)
    content = fileGCS.read()
    fileGCS.close()
    return content
# [END read]


# [START stat]
def stat_file(fileName):
    statFileGCS = repr(gcs.stat(fileName))
    logging.info('WNP: File stat: %s', statFileGCS)
    return statFileGCS
# [END stat]


# [START list bucket]
def list_bucket(bucket):
    logging.info('WNP: Contenido del bucket %s >> ', bucket)
    contentBucket = gcs.listbucket(bucket)
    logging.info(' '.join([i.filename for i in contentBucket]))
# [END list bucket]

