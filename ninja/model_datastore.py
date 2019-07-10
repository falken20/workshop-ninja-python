# Copyright 2019
#
# Workshop Ninja Python

from flask import current_app
from google.cloud import datastore
# Import the Namespace Manager API
from google.appengine.api import namespace_manager



builtin_list = list


def init_app(app):
    pass


# Crea un cliente para interactuar con la API de Cloud Datastore
def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])

    # Establecemos un namespace para almacenar nuestras entidades
    print('Establecemos el namespaces: ', current_app.config['NAMESPACE_ID'])
    namespace_manager.set_namespace(current_app.config['NAMESPACE_ID'])

# Convierte la clave de entidad del almacen de datos en un id que la app  pueda utilizar
def from_datastore(entity):
    """
    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

# Lista todos los ninja ordenados por nombre
def list(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='Ninja', order=['name'])
    # Usamos query.fetch para proporcionar a un iterador las peticiones de consulta
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    # Obtenemos los resultados de page en page y devolvemos un cursor para permitir al usuario cargar la page siguiente de resultados
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor

# Lee un determinado ninja
def read(id):
    ds = get_client()
    key = ds.key('Ninja', int(id))
    results = ds.get(key)
    return from_datastore(results)

# Actualiza un ninja, si el parametro data es null se trata de un nuevo ninja
def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Ninja', int(id))
    else:
        key = ds.key('Ninja')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update

# Elimina un determinado ninja
def delete(id):
    ds = get_client()
    key = ds.key('Ninja', int(id))
    ds.delete(key)
