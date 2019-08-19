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
CLOUD_STORAGE_BUCKET = 'workshop-ninja-python'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# [START retries]
gcs.set_default_retry_params(
    gcs.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
        ))
# [END retries]


# [START get_default_bucket]
def get(self):
    bucket_name = CLOUD_STORAGE_BUCKET

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Using bucket name: {}\n\n'.format(bucket_name))

    print('WNP: Obtenemos el nombre del bucket --> ', bucket_name)
# [END get_default_bucket]


# [START write]
def create_file(self, filename):
    """Create a file."""

    print('WNP: Creating file {}\n'.format(filename))

    # The retry_params specified in the open call will override the default
    # retry params for this particular file handle.
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    with gcs.open(
        filename, 'w', content_type='text/plain', options={
            'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
            retry_params=write_retry_params) as cloudstorage_file:
                cloudstorage_file.write('abcde\n')
                cloudstorage_file.write('f'*1024*4 + '\n')
    self.tmp_filenames_to_clean_up.append(filename)
# [END write]

# [START read]
def read_file(self, filename):
    self.response.write(
        'Abbreviated file content (first line and last 1K):\n')

    with cloudstorage.open(filename) as cloudstorage_file:
        self.response.write(cloudstorage_file.readline())
        cloudstorage_file.seek(-1024, os.SEEK_END)
        self.response.write(cloudstorage_file.read())
# [END read]

def stat_file(self, filename):
    self.response.write('File stat:\n')

    stat = gcs.stat(filename)
    self.response.write(repr(stat))


# [START delete_files]
def delete_files(self):
    self.response.write('Deleting files...\n')
    for filename in self.tmp_filenames_to_clean_up:
        self.response.write('Deleting file {}\n'.format(filename))
        try:
            gcs.delete(filename)
        except gcs.NotFoundError:
            pass
# [END delete_files]

