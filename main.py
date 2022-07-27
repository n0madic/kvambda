from flask import abort
from google.cloud import firestore

client = firestore.Client()

database = 'kvambda'


def kvambda(request):
    token = request.headers.get('Token')
    if token:
        doc_ref = client.collection(database).document(token)
        check = doc_ref.get([])
        if check.exists:
            key = firestore.Client.field_path(request.path[1:].strip())
            if request.method == 'GET':
                doc = doc_ref.get([key]).to_dict()
                if doc:
                    return doc.get(key.strip('`'))
                else:
                    abort(404)
            elif request.method == 'POST' or request.method == 'PUT':
                result = doc_ref.update({key: request.get_data()})
                if result:
                    return 'SAVED'
                else:
                    return abort(500)
            elif request.method == 'DELETE':
                result = doc_ref.update({key: firestore.DELETE_FIELD})
                if result:
                    return 'DELETED'
                else:
                    return abort(500)
        else:
            return abort(403)
    else:
        return abort(401)


if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/<path:dummy>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def index(dummy):
        return kvambda(request)

    app.run('127.0.0.1', 8000, debug=True)