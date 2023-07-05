from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
import json
import uuid
import glob
import csv
import logging as log
import io
from collections import OrderedDict

UPLOAD_FOLDER = "../Data/Uploads/"
ALLOWED_EXTENSIONS = {"tsv", "csv", "json"}


def set_log_level(verbosity: str):
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


def get_name_file(files:list, mode:str):
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

def check_extension(extension:str,first_line:list):
    if extension == "csv" :
        if '\t' in first_line:
            return "\t"
        else :
            return ","
    elif extension == "tsv" :
        return "\t"
    else:
        error = "Import error : Wrong extension, only tsv and csv allowed"
        return error

def line_to_list(line):
    """
    >>>line_to_list('lias,fat,patient,"un,deux,trois",mom,Unaffected,M,"one,two,three"')
    ['lias', 'fat', 'patient', 'un,deux,trois', 'mom', 'Unaffected', 'M', 'one,two,three']
    """
    reader = csv.reader([line])
    result = next(reader)
    return result

def get_rows_list(lines_list,separator):
    file_as_list = []
    length = len(lines_list[0].split(separator))
    for i in range(len(lines_list)):
        if separator == "," and "\"" in lines_list[i]: 
            log.debug(f" boucle guillemet {lines_list[i]}")
            line_col_list = line_to_list(lines_list[i])
            log.debug(f" boucle guillemet {line_col_list}")
        else:       
            line_col_list = lines_list[i].split(separator)

        if line_col_list == [""]:
            continue
        log.debug(f"col_list {line_col_list}")
        file_as_list.append(line_col_list)
        log.debug(f" len col {len(lines_list[0].split(separator))} len row {len(line_col_list)}")
        if length != len(line_col_list):
            error = "Import error : The rows do not all have the same column number. Row " + str(i) + " has not the same number of columns as the header (which is row 0)."
            return error
    return file_as_list


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

def get_columns(file_list0):
    list_col_order=[]
    error=""
    authorized_colnames =[["id","Patient ID", "ID"],
                ["alias", "Aliases", "Alias"],
                ["father", "Father"],
                ["mother", "Mother"],
                ["sex", "Sex"],
                ["phenotype", "Phenotype"],
                ["HPOList", "HPO List", "hpolist"],
                ["starkTags","Stark Tags","starktags"]]
    
    if "id" not in file_list0[0] and "Patient ID" not in file_list0[0] and "ID" not in file_list0[0]:
        error="Import error : An id column is missing. It can be named 'id', 'Patient ID' or 'ID'."
        return error, None
    log.debug(f" FILELIST 1 {file_list0}")
    
    col_names_list, file_list = reform_columns(file_list0, authorized_colnames)


    # find which column is in order and add the right name for the json
    for col_name in col_names_list: #for each column
        for col_options in authorized_colnames : #for each pack of allowed column names
            if col_name in col_options : #check if column name in allowed pack        
                list_col_order.append(col_options[0]) #add the right name for the json
                log.debug(f" colname :{col_name}, col option : {col_options}")

    return file_list,list_col_order


def fill_dict(file_list, list_col_order):
    dict_list = []
    for line in range(len(file_list)-1):  # get dictionnaries in list, for each line
        mydict = OrderedDict()
        for n in range(len(list_col_order)):  # get lines in dictionnaries, for each column
            log.debug(f"line {line}  n {n}")
            column = list_col_order[n]
            value = file_list[line+1][n]
            if column == "HPOList" or column == "starkTags":
                mydict[column] = value.split(',')
                log.debug(f"rentre dans boucle {column} avec value :{value}, donne {mydict[column]}")
            elif column == "sex" :
                if value in ["F","Female","female",2,"2"] :
                    mydict[column] = "F"
                elif value in ["M","Male","male",1,"1"]:
                    mydict[column] = "M"
                else :
                    mydict[column] = "Unknown"
            elif column == "phenotype" :
                if value in ["Affected","affected",2,"yes","Yes","2"]:
                    mydict[column] = "Affected"
                elif value in ["Unaffected", "unaffected","no", "No",1,"1"]:
                    mydict[column] = "Unaffected"
                else :
                    mydict[column] = "Missing"
            else :
                mydict[column] = value
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

if len(get_files()) < 1:
    CURRENT_FILE = ""
else :
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
        id_list = []

        if "file" not in request.files:
            error = "Import error : No file imported"
            return error

        lines_list, extension = get_lines_content(post_data)

        separator = check_extension(extension,lines_list[0])
        if separator.startswith("Import"):
            error = separator
            return error

        file_as_list = get_rows_list(lines_list,separator)
        if isinstance(file_as_list, str) == True:
            error = file_as_list
            return error

        file_list,list_col_order = get_columns(file_as_list)
        if list_col_order == None:
            error = file_list
            return error

        dict_list = fill_dict(file_list, list_col_order)

        peds_merged = merge_peds(dict_list)

        # unique ids
        for i in range(len(peds_merged)):
            id_list.append(peds_merged[i]["id"])
        if len(set(id_list)) != len(id_list):
            error = "Import error : IDs are not unique."
            return error
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
