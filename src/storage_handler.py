#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging
from google.cloud import storage
import os
import datetime
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest


import config

def _get_storage_client():
    return storage.Client(config.PROJECT_ID)


def _check_extension(filename):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in config.ALLOWED_EXTENSIONS):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)

    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, folder, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    logging.info('WNP: Creando fichero %s de tipo %s en GCS', filename, content_type)

    bucket_name = config.CLOUD_STORAGE_BUCKET

    _check_extension(filename)

    filename = _safe_filename(filename)
    client = _get_storage_client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(filename)
    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    logging.info('WNP: Fichero %s creado en GCS con url %s', filename, blob.public_url)

    return filename, blob.public_url

    
def read_file(folder, filename):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    bucket_name = config.CLOUD_STORAGE_BUCKET

    client = _get_storage_client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(folder + filename)

    return blob.download_as_string()


def delete_file(folder, filename):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    bucket_name = config.CLOUD_STORAGE_BUCKET

    client = _get_storage_client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(folder + filename)
    blob.delete()
