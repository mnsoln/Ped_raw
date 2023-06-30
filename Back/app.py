from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
#from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import json
import uuid
import glob
import os
import logging as log
import io


UPLOAD_FOLDER = '../Data/Uploads/'
ALLOWED_EXTENSIONS = {'tsv', 'csv', 'json'}


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


# instantiate the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config.from_object(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# log.getLogger('flask_cors').level = log.DEBUG
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})



##PED

def get_files():
    files=glob.glob('../Data/*.json')
    return files


def get_name_file(files, mode): 
    if mode == "split":
        file_list=[]
        for file in files:
            split = file.split('/')
            file_list.append(split[len(split)-1][:-5])
        return file_list
    elif mode == "get" :
        my_file = ("../Data/" + files + ".json")
        return my_file
    

def get_linesontent(post_data):
    file_encoded = post_data['file']
    log.debug(f"file2:{file_encoded}")
    filename = file_encoded.filename
    file = io.TextIOWrapper(file_encoded, encoding='utf-8-sig') #decoding
    file_content=file.read()
    log.debug(f"file content:{file_content}")
    lines_list = file_content.split('\n')
    log.debug(f"lines_list:{lines_list}")
    return lines_list

def getDictList(file_list):
    dict_list=[]
    colNames_list=[]
    for l in file_list[0]: #get column names
        colNames_list.append(l)
    for line in range(len(file_list)-1): #get dictionnaries in list
        dict={}
        for n in range(len(colNames_list)): #get lines in dictionnaries
            dict[colNames_list[n]] = file_list[line+1][n]
        dict_list.append(dict)
    log.debug(f"dict list{dict_list}")
    return dict_list

def mergePeds(dict_list):
    with open(CURRENT_FILE,'r') as PEDS:
        log.debug(f"/up 2 curr: {CURRENT_FILE}")
        data = json.load(PEDS)
        log.debug(f"/up data1 : {data}")
        peds_merged = data + dict_list
        return peds_merged



CURRENT_FILE = get_files()[0]


@app.route('/files', methods=['GET', 'POST'])
def all_files():

    if request.method =='POST':
        global CURRENT_FILE
        files=get_files()
        selected_base = request.get_json()["mybase"]
        CURRENT_FILE = get_name_file(selected_base, "get")

        if CURRENT_FILE not in files: #create new file
            CURRENT_FILE ="../Data/" + CURRENT_FILE
            if CURRENT_FILE.endswith(".json") == False :
                CURRENT_FILE = CURRENT_FILE + ".json"
            with open(CURRENT_FILE,'w') as new:
                new.write("[]")

        log.debug(f"request:{request.get_json()}")
        log.debug(f"curr post files:{CURRENT_FILE}")
        return {'status': 'success'}
    
    elif request.method =='GET':
        files = get_files()
        paths = get_name_file(files, "split")
        return jsonify(paths)
    


@app.route('/ped', methods=['GET','POST'])
def all_peds():
    global CURRENT_FILE
    if request.method =='POST':
        post_data = request.get_json()
        log.debug(f"/ped POST: {post_data}")
        with open(CURRENT_FILE,'w') as PEDS:
            PEDS.write(json.dumps(post_data))    
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

@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        post_data = request.files
        log.debug(f"file2:{post_data}")
        file_asList=[]
        id_list=[]
        
        if 'file' not in request.files:
            raise ImportError('No file imported')
        
        lines_list = get_linesontent(post_data)

        length=len(lines_list[0].split(','))
        for i in range(len(lines_list)):

            line_col_list = lines_list[i].split(',')
            if line_col_list == ['']:
                continue

            log.debug(f"col_list {line_col_list}")
            file_asList.append(line_col_list)
            if length != len(line_col_list):
                log.debug(f"error : not same column numbers col:{i}")
                raise IndexError('Not same numbers of columns col:',i)
        log.debug(f"file_list{file_asList}")

        dict_list = getDictList(file_asList)

        peds_merged = mergePeds(dict_list)

        #unique ids 
        for i in range(len(peds_merged)):
            id_list.append(peds_merged[i]['id'])   
        if(len(set(id_list)) != len(id_list)):
            raise NameError('IDs are not unique')
        else :
            log.debug('sortie')
            return jsonify(peds_merged)
    







# sanity check route, la route du site backend ou il va chercher les infos
@app.route("/ping", methods=["POST"])
def ping_pong():
    post_data = request.get_json()
    if 'MEDINA Solène !' in post_data['msg']:
        res='NICAISE Samuel !'
    else : res='MEDINA Solène !'
    return jsonify(res)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4280, debug=True)
