from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import json
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

#PEDS= [
#    {
#    'id':'Jean Pierre',
#    'alias':'JP',
#    'pere':'LM',
#    'mere':'JM',
#    'sexe':'M',
#    'phenotype':'CLL',
#    'listeHPO':'LDL',
#    'tagStark':'41',
#    }
#]



def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# instantiate the app
app = Flask(__name__)
# app.config.from_object(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##PED

@app.route('/ped', methods=['GET','POST'])
def all_peds():
    #global PEDS
    if request.method =='POST':
        post_data = request.get_json()
        print("post request made:", post_data)
        with open("/Data/data.json",'w') as PEDS:
            PEDS.write(json.dumps(post_data))
    
        # response_object['message'] = "Ajout de fichier ped terminé. N'oubliez pas de sauvegarder les modifications. "
        return {'status': 'success'}
    else:
        with open("/Data/data.json",'r') as PEDS:
            data = PEDS.read()
        return data







# sanity check route, la route du site backend ou il va chercher les infos
@app.route("/ping", methods=["POST"])
def ping_pong():
    print('oui')
    post_data = request.get_json()
    if 'ping' in post_data['msg']:
        res='pong!'
    else : res='ping!'
    return jsonify(res)



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
    app.run(host="0.0.0.0", port=4280, debug=True)
