from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import uuid


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

PEDS= [
    {
    'id':'Jean Pierre',
    'alias':'JP',
    'pere':'LM',
    'mere':'JM',
    'sexe':'M',
    'phenotype':'CLL',
    'listeHPO':'LDL',
    'tagStark':'41',
    }
]



def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##PED

@app.route('/ped', methods=['GET','POST'])
def all_peds():
    response_object = {'status': 'success'}
    if request.method =='POST':
        post_data = request.get_json()
        PEDS.append({
            'id':post_data.get('id'),
            'alias':post_data.get('alias'),
            'pere':post_data.get('pere'),
            'mere':post_data.get('mere'),
            'sexe':post_data.get('sexe'),
            'phenotype':post_data.get('phenotype'),
            'listeHPO':post_data.get('listeHPO'),
            'tagStark':post_data.get('tagStark'),
            })
        response_object['message'] = "Ajout de fichier ped terminé. N'oubliez pas de sauvegarder les modifications. "
    else:
        response_object['peds'] = PEDS
    return jsonify(response_object)







# sanity check route, la route du site backend ou il va chercher les infos
@app.route("/ping", methods=["POST"])
def ping_pong():
    print('oui')
    post_data = request.get_json()
    if 'ping' in post_data['msg']:
        res='pong!'
    else : res='ping!'
    return jsonify(res)


# @app.route('/ped', methods=['GET', 'POST'])
# def all_ped():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         PEDS.append({
#             'id': uuid.uuid4().hex,
#             'individu': post_data.get('individu'),
#             'alias': post_data.get('alias'),
#             'pere': post_data.get('pere'),
#             'mere': post_data.get('mere'),
#             'sexe': post_data.get('sexe'),
#             'phenotype': post_data.get('phenotype'),
#             'listeHPO': post_data.get('listeHPO'),
#             'tagStark': post_data.get('tagStark'),
#         })
#         response_object['message'] = 'Book added!'
#     else:
#         response_object['books'] = BOOKS
#     return jsonify(response_object)



@app.route('/', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/<book_id>', methods=['PUT','DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Mis à jour !'
    if request.method == 'DELETE':
            remove_book(book_id)
            response_object['message'] = 'Supprimé!'
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4280)