# Copyright 2019
#
# Workshop Ninja Python

from ninja import get_model, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    url_for


crud = Blueprint('crud', __name__)


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

    current_app.logger.info("Fichero subido %s como %s.", file.filename, public_url)

    return public_url


# Vista que lista todos los ninjas y los muestra usando list.html
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    ninjas, next_page_token = get_model().list(cursor=token)

    return render_template("list.html", ninjas=ninjas, next_page_token=next_page_token)


# Vista que lista un determinado ninja en view.html
@crud.route('/<id>')
def view(id):
    ninja = get_model().read(id)
    return render_template("view.html", ninja=ninja)


# Vista que muestra el formulario form.html para añadir un nuevo ninja
# Cuando el usuario pulsa salvar la misma vista gestiona la acción HTTP POST del formulario
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        ninja = get_model().create(data)

        return redirect(url_for('.view', id=ninja['id']))

    return render_template("form.html", action="Add", ninja={})


# Vista que muestra el formulario form.html para modificar un ninja
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


# Elimina un determinado ninja
@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
