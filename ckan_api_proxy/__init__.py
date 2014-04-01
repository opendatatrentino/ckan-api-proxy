import cgi
import json

import flask
from flask.ext.restful import Resource, Api
from werkzeug.exceptions import NotFound, BadRequest, HTTPException
from werkzeug.exceptions import NotImplemented as NotImplementedExc
from ckan_api_client.high_level import CkanHighlevelClient
from ckan_api_client.exceptions import HTTPError
from ckan_api_client.objects import CkanDataset, CkanResource

app = flask.Flask(__name__)
api = Api(app)


# Todo: read these from HTTP request headers:
# x-ckan-url
# x-ckan-apikey
CKAN_URL = 'http://127.0.0.1:5000'
CKAN_API_KEY = '9aa2ee4e-5baa-46e1-adda-bc876db398a0'


def get_ckan_client():
    ckan_url = flask.request.headers.get('x-ckan-url')
    ckan_apikey = flask.request.headers.get('x-ckan-apikey')
    if ckan_url is None:
        raise BadRequest("You must pass a x-ckan-url header")
    return CkanHighlevelClient(base_url=ckan_url, api_key=ckan_apikey)


# def json_response(data):
#     headers = {
#         'Content-type': 'application/json',
#     }
#     data = json.dumps(data)
#     return data, 200, headers


def _get_dataset(dataset_id):
    client = get_ckan_client()
    try:
        return client.get_dataset(dataset_id)
    except HTTPError as e:
        if e.status_code == 404:
            raise NotFound('The requested dataset does not exist.')
        raise


class DatasetCollection(Resource):
    def get(self):
        client = get_ckan_client()
        dataset_ids = client.list_datasets()
        page_ids = dataset_ids[:10]
        return [client.get_dataset(id).serialize() for id in page_ids]

    def post(self):
        raise NotImplementedExc()


class Dataset(Resource):
    def get(self, dataset_id):
        client = get_ckan_client()
        try:
            dataset = client.get_dataset(dataset_id)
        except HTTPError as e:
            if e.status_code == 404:
                raise NotFound('The requested dataset does not exist.')
            raise
        return dataset.serialize()

    def put(self, dataset_id):
        raise NotImplementedExc()


class DatasetResourceCollection(Resource):
    def get(self, dataset_id):
        dataset = _get_dataset(dataset_id)
        return dataset.serialize()['resources']

    def post(self, dataset_id):
        # todo: add resource to the dataset
        content_type_hdr = flask.request.headers['content-type']
        content_type, stuff = cgi.parse_header(content_type_hdr)
        if content_type != 'application/json':
            raise BadRequest('Invalid content type: json required')
        new_resource_json = json.loads(flask.request.data)
        new_resource = CkanResource(new_resource_json)

        dataset = _get_dataset(dataset_id)
        dataset.resources.append(new_resource)

        client = get_ckan_client()
        updated = client.update_dataset(dataset)
        return updated.serialize()


class DatasetResource(Resource):
    def get(self, dataset_id, resource_id):
        dataset = _get_dataset(dataset_id)
        for resource in dataset.serialize()['resources']:
            if resource['id'] == resource_id:
                return resource
        raise NotFound("The resource was not found")

    def put(self, dataset_id, resource_id):
        raise NotImplementedExc()

    def delete(self, dataset_id, resource_id):
        dataset = _get_dataset(dataset_id)
        respos = None
        for i, resource in enumerate(dataset.resources):
            if resource.id == resource_id:
                respos = i
        if respos is None:
            raise NotFound("The resource was not found")
        dataset.resources.pop(respos)

        client = get_ckan_client()
        client.update_dataset(dataset)


api.add_resource(DatasetCollection, '/dataset')
api.add_resource(Dataset, '/dataset/<dataset_id>')
api.add_resource(DatasetResourceCollection, '/dataset/<dataset_id>/resources')
api.add_resource(DatasetResource, '/dataset/<dataset_id>/resources/<resource_id>')  # noqa
