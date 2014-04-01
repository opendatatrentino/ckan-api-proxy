# Ckan API proxy

Proxy to access Ckan API in a safer RESTful way, via [Ckan API client](https://github.com/rshk/ckan-api-client/)

## Concepts

This is a simple Flask web application that exposes RESTful API on top of the Ckan
API, passing through [Ckan API client](https://github.com/rshk/ckan-api-client/).

The URL of the ckan instance to which to connect and the API key are passed
using, respectively, the ``x-ckan-url`` and ``x-ckan-apikey`` request headers.

## Example

- launch a ckan instance on 127.0.0.1:5000 (and get an API key)
- launch ckan-api-proxy on 127.0.0.1:8000

List datasets:

```
http get localhost:8000/dataset 'x-ckan-url:http://localhost:5000'
```

Get a specific dataset:

```
http get localhost:8000/dataset/05be9edb-be90-4cac-84c4-2822e8481ed8 \
    'x-ckan-url:http://localhost:5000'
```

Get resources from a dataset:

```
http get localhost:8000/dataset/05be9edb-be90-4cac-84c4-2822e8481ed8/resources \
    'x-ckan-url:http://localhost:5000'
```

Add a resource to a dataset:

```
http POST localhost:8000/dataset/05be9edb-be90-4cac-84c4-2822e8481ed8/resources \
    'x-ckan-url:http://localhost:5000' 'x-ckan-apikey:aaaabbbb-0000-1111-cccc-ddddeeeeffff' \
    name='my-new-resource' url='http://example.com/data.json' format='JSON'
```
