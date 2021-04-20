import collections
import fnmatch
import hmac
import json
import os

from flask import abort
from flask import Response as FResponse
import requests



def query_request(query=None, method="GET", **kwargs):
    """
    Queries like /repos/:id needs to be appended to the base URL,
    Queries like https://raw.githubusercontent.com need not.

    full list of kwargs see http://docs.python-requests.org/en/master/api/#requests.request
    """

    if query[0] == "/":
        query = BASE_URL + query

    request_kwargs = {
        "auth": AUTH,
    }
    request_kwargs.update(**kwargs)
    return requests.request(method, query, **request_kwargs)


def Response(data=None, status=200, mimetype='application/json'):
    if data is None:
        data = {}

    response_object = json.dumps(data, default=lambda obj: obj.__dict__)
    return FResponse(response_object, status=status, mimetype=mimetype)

def match_webhook_secret(request):
    """Match the webhook secret sent from GitHub"""
    if os.environ.get("OVER_HEROKU", False):
        if ('X-Hub-Signature' in request.headers and
           request.headers.get('X-Hub-Signature') is not None):
            header_signature = request.headers.get('X-Hub-Signature', None)
        else:
            abort(403)
        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha1':
            abort(501)

        mac = hmac.new(os.environ["GITHUB_PAYLOAD_SECRET"].encode(),
                       msg=request.data,
                       digestmod="sha1")

        if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
            abort(403)
    return True