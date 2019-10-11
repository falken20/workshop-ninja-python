#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging
import base64
import datetime
from google.cloud import storage
from google.cloud import exceptions
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest


import config


def _get_storage_client():
    logging.info('WNP: Obtenemos el cliente para guardar en GCS %s', config.PROJECT_ID)
    return storage.Client(config.PROJECT_ID)


def _check_extension(filename):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in config.ALLOWED_EXTENSIONS):
        raise BadRequest('{0} tiene un nombre o extension invalido'.format(filename))


def _safe_filename(filename):
    """
    Genera un nombre de archivo seguro que es poco probable que choque con objetos existentes en GCS
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)

    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_base64_file(data, mime, filename):
    """
    Sube un archivo a GCS a partir del base 64 y devuelve la url publica
    """
    logging.info('WNP: Creando fichero %s a partir de base 64 en GCS bucket: %s', filename, config.CLOUD_STORAGE_BUCKET)
    bucket_name = config.CLOUD_STORAGE_BUCKET
    client = _get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(base64.b64decode(data), content_type=mime)
    logging.info('WNP: Fichero %s creado en GCS', filename)
    return "https://storage.cloud.google.com/" + bucket_name + "/" + filename


def delete_file(filename):
    """
    Borra un determinado archivo de GCS.
    """
    try:
        bucket_name = config.CLOUD_STORAGE_BUCKET
        client = _get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.delete()
    except exceptions.NotFound:
        logging.warning('WNP: No se ha podido localizar el archivo %s en GSC', filename)

    except Exception as e:
        logging.error('WNP: Unexpected error: %s', e)


def upload_file(file_stream, folder, filename, content_type):
    """
    Sube un archivo a GCS y devuelve el nombre del archivo adaptado y la url publica
    """

    logging.info('WNP: Creando fichero %s de tipo %s en GCS', filename, content_type)

    bucket_name = config.CLOUD_STORAGE_BUCKET

    try:
        _check_extension(filename)

        filename = _safe_filename(filename)
        client = _get_storage_client()
        bucket = client.bucket(bucket_name)

        blob = bucket.blob(folder + filename)
        blob.upload_from_string(
            file_stream,
            content_type=content_type)

        logging.info('WNP: Fichero %s creado en GCS con url %s', filename, blob.public_url)

        return filename, blob.public_url

    except (BadRequest, Exception) as e:
        logging.error('WNP: Error en fichero %s al subirlo en GCS: %s', filename, e)
        return None, None


def read_file(folder, filename):
    """
    Lee un determinado fichero de GCS.
    """

    bucket_name = config.CLOUD_STORAGE_BUCKET

    client = _get_storage_client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(folder + filename)

    return blob.download_as_string()