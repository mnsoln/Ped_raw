from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
import json
import uuid
import glob
import os
import logging as log
import io


UPLOAD_FOLDER = "../Data/Uploads/"
ALLOWED_EXTENSIONS = {"tsv", "csv", "json"}


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
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config.from_object(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# log.getLogger('flask_cors').level = log.DEBUG
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##PED


def get_files():
    files = glob.glob("../Data/*.json")
    return files


def get_name_file(files, mode):
    if mode == "split":
        file_list = []
        for file in files:
            split = file.split("/")
            file_list.append(split[len(split) - 1][:-5])
        return file_list
    elif mode == "get":
        my_file = "../Data/" + files + ".json"
        return my_file


def get_lines_content(post_data):
    file_encoded = post_data["file"]
    log.debug(f"file2:{file_encoded}")
    filename = file_encoded.filename
    extension = filename.rsplit('.',1)[1]
    myfile = io.TextIOWrapper(file_encoded, encoding="utf-8-sig")  # decoding
    file_content = myfile.read()
    log.debug(f"file content:{file_content}")
    lines_list = file_content.split("\n")
    log.debug(f"lines_list:{lines_list}")
    return lines_list, extension

def reform_columns(file_list, authorized_colnames):
    to_ignore=[]
    col_names_list = []

    flat_list = [item for sublist in authorized_colnames for item in sublist]

    for l in file_list[0]:  # get column names
        if l not in flat_list :
            to_ignore.append(file_list[0].index(l))
            log.debug(f" colname ignored {l} index {file_list[0].index(l)}")
            continue
        col_names_list.append(l)
    
    #remove unwanted columns
    for line in file_list :
        for i in range(len(to_ignore)):
            line.pop(to_ignore[i])
    log.debug(f" FILELIST 2 {file_list}")

    return col_names_list, file_list

def get_dict_list(file_list0):
    dict_list = []
    list_col_order=[]
    

    authorized_colnames =[["id","Patient ID", "ID"],
                ["alias", "Aliases", "Alias"],
                ["father", "Father"],
                ["mother", "Mother"],
                ["sex", "Sex"],
                ["phenotype", "Phenotype"],
                ["HPOList", "HPO List", "hpolist"],
                ["starkTags","Stark Tags","starktags"]]
    

    if "id" not in file_list0[0] and "Patient ID" not in file_list0[0] and "ID" not in file_list0[0]:
        raise NameError("id column mandatory")
    log.debug(f" FILELIST 1 {file_list0}")
    
    col_names_list, file_list = reform_columns(file_list0, authorized_colnames)


    # find which column is in order and add the right name for the json
    for col_name in col_names_list: #for each column
        for col_options in authorized_colnames : #for each pack of allowed column names
            if col_name in col_options : #check if column name in allowed pack        
                list_col_order.append(col_options[0]) #add the right name for the json
                log.debug(f" colname :{col_name}, col option : {col_options}")
    log.debug(f"ORDER {list_col_order}")

    for line in range(len(file_list)-1):  # get dictionnaries in list
        mydict = {}
        for n in range(len(list_col_order)):  # get lines in dictionnaries
            log.debug(f"line {line}  n {n}")

            mydict[list_col_order[n]] = file_list[line+1][n]
            log.debug(f" MYDICT {mydict}")
        dict_list.append(mydict)
    return dict_list


def merge_peds(dict_list):
    with open(CURRENT_FILE, "r") as PEDS:
        log.debug(f"/up 2 curr: {CURRENT_FILE}")
        data = json.load(PEDS)
        log.debug(f"/up data1 : {data}")
        peds_merged = data + dict_list
        return peds_merged


CURRENT_FILE = get_files()[0]


@app.route("/files", methods=["GET", "POST"])
def all_files():
    if request.method == "POST":
        global CURRENT_FILE
        files = get_files()
        selected_base = request.get_json()["mybase"]
        CURRENT_FILE = get_name_file(selected_base, "get")

        if CURRENT_FILE not in files:  # create new file
            CURRENT_FILE = "../Data/" + CURRENT_FILE
            if CURRENT_FILE.endswith(".json") == False:
                CURRENT_FILE = CURRENT_FILE + ".json"
            with open(CURRENT_FILE, "w") as new:
                new.write("[]")

        log.debug(f"request:{request.get_json()}")
        log.debug(f"curr post files:{CURRENT_FILE}")
        return {"status": "success"}

    elif request.method == "GET":
        files = get_files()
        paths = get_name_file(files, "split")
        return jsonify(paths)


@app.route("/ped", methods=["GET", "POST"])
def all_peds():
    global CURRENT_FILE
    if request.method == "POST":
        post_data = request.get_json()
        log.debug(f"/ped POST: {post_data}")
        with open(CURRENT_FILE, "w") as PEDS:
            PEDS.write(json.dumps(post_data))
        return {"status": "success"}

    elif request.method == "GET":
        log.debug(f"/ped GET: {CURRENT_FILE}")
        with open(CURRENT_FILE, "r") as PEDS:
            log.debug(f"/ped GET 2 curr: {CURRENT_FILE}")
            data = PEDS.read()
            log.debug(f"/ped GET data1 : {data}")
        return data

    else:
        raise NotImplementedError("Only GET and POST requests implemented for /ped")


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        post_data = request.files
        log.debug(f"file2:{post_data}")
        file_as_list = []
        id_list = []

        if "file" not in request.files:
            raise ImportError("No file imported")

        lines_list, extension = get_lines_content(post_data)

        if extension == "csv" :
            separator = ","
        elif extension == "tsv" :
            separator = "\t"
        else:
            raise TypeError("wrong extension, only tsv and csv allowed")
        
        

        length = len(lines_list[0].split(separator))
        for i in range(len(lines_list)):
            line_col_list = lines_list[i].split(separator)
            if line_col_list == [""]:
                continue

            log.debug(f"col_list {line_col_list}")
            file_as_list.append(line_col_list)
            if length != len(line_col_list):
                log.debug(f"error : not same column numbers col:{i}")
                raise IndexError("Not same numbers of columns col:", i)
        log.debug(f"file_list{file_as_list}")



        dict_list = get_dict_list(file_as_list)

        peds_merged = merge_peds(dict_list)

        # unique ids
        for i in range(len(peds_merged)):
            id_list.append(peds_merged[i]["id"])
        if len(set(id_list)) != len(id_list):
            raise NameError("IDs are not unique")
        else:
            log.debug("sortie")
            return jsonify(peds_merged)


# sanity check route, la route du site backend ou il va chercher les infos
@app.route("/ping", methods=["POST"])
def ping_pong():
    post_data = request.get_json()
    if "MEDINA Solène !" in post_data["msg"]:
        res = "NICAISE Samuel !"
    else:
        res = "MEDINA Solène !"
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4280, debug=True)
