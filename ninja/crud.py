# Copyright 2019
#
# Workshop Ninja Python

from ninja import get_model, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    url_for


crud = Blueprint('crud', __name__)


# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    ninjas, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        ninjas=ninjas,
        next_page_token=next_page_token)


@crud.route('/<id>')
def view(id):
    ninja = get_model().read(id)
    return render_template("view.html", ninja=ninja)


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        # [START image_url]
        image_url = upload_image_file(request.files.get('image'))
        # [END image_url]

        # [START image_url2]
        if image_url:
            data['imageUrl'] = image_url
        # [END image_url2]

        ninja = get_model().create(data)

        return redirect(url_for('.view', id=ninja['id']))

    return render_template("form.html", action="Add", ninja={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    ninja = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        ninja = get_model().update(data, id)

        return redirect(url_for('.view', id=ninja['id']))

    return render_template("form.html", action="Edit", ninja=ninja)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
