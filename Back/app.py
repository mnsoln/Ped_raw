from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
#from werkzeug.middleware.proxy_fix import ProxyFix
import json
import uuid
import glob
import sys
import logging as log


def set_log_level(verbosity):
    verbosity = verbosity.lower()
    configs = {
        "debug": log.DEBUG,
        "info": log.INFO,
        "warning": log.WARNING,
        "error": log.ERROR,
        "critical": log.CRITICAL,
    }
    if verbosity not in configs.keys():
        raise ValueError(
            f"Unknown verbosity level: {verbosity}\nPlease use any in: {configs.keys()}"
        )
    log.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=configs[verbosity],
    )

set_log_level("debug")

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

# log.getLogger('flask_cors').level = log.DEBUG
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})



##PED

def getFiles():
    files=glob.glob('../Data/*.json')
    return files

CURRENT_FILE = getFiles()[0]


@app.route('/files', methods=['GET', 'POST'])
def all_files():

    if request.method =='POST':
        global CURRENT_FILE
        files=getFiles()
        CURRENT_FILE = request.get_json()["mybase"]
        if CURRENT_FILE not in files:
            CURRENT_FILE ="../Data/"+CURRENT_FILE
            if CURRENT_FILE.endswith(".json") == False :
                CURRENT_FILE = CURRENT_FILE + ".json"
            with open(CURRENT_FILE,'w') as new:
                new.write("[]")
        log.debug(f"request:{request.get_json()}")
        log.debug(f"curr post files:{CURRENT_FILE}")
        return {'status': 'success'}
    
    elif request.method =='GET':
        paths=getFiles()
        #files=[]
        # for path in paths:
        #     split=path.split('/')
        #     files.append(split[len(split)-1][:-5])
        return jsonify(paths)
    


@app.route('/ped', methods=['GET','POST'])
def all_peds():
    global CURRENT_FILE
    files=getFiles()
    #print(files)
    if request.method =='POST':
        post_data = request.get_json()
        log.debug(f"/ped POST: {post_data}")
        with open(CURRENT_FILE,'w') as PEDS:
            PEDS.write(json.dumps(post_data))    
        # with open("/Data/data.json",'w') as PEDS:
        #     PEDS.write(json.dumps(post_data))    
        # response_object['message'] = "Ajout de fichier ped terminé. N'oubliez pas de sauvegarder les modifications. "
        return {'status': 'success'}
    
    elif request.method =='GET':
        log.debug(f"/ped GET: {CURRENT_FILE}")
        with open(CURRENT_FILE,'r') as PEDS:
            log.debug(f"/ped GET 2 curr: {CURRENT_FILE}")
            data = PEDS.read()
            log.debug(f"/ped GET data1 : {data}")
        return data
    
    else:
        raise NotImplementedError('Only GET and POST requests implemented for /ped')


# @app.route('/newfile', methods=['GET', 'POST'])
# def new_file():
#     if request.method =='POST':
#         post_data = request.get_json()





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
