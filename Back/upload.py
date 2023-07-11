from flask import session
import json
import csv
import logging as log
import io
from collections import OrderedDict
from openpyxl import load_workbook




def get_lines_content(post_data):
    log.debug(f"postdata:{post_data}")
    file_encoded = post_data["file"]
    log.debug(f"file encoded:{file_encoded}")
    filename = file_encoded.filename
    extension = filename.rsplit('.',1)[1]
    myfile = io.TextIOWrapper(file_encoded, encoding="utf-8-sig")  # decoding
    log.debug(f"extension:{extension}")
    if extension == 'xlsx':
        lines_list = []
        workbook = load_workbook(file_encoded)
        worksheet = workbook.worksheets[0]
        test = [cell.value for cell in list(worksheet.rows)[1]]
        if len(test) != 1 : #differentiate between real excel file and csv with excel extension
            for r in worksheet.rows:
                column = [cell.value for cell in r]
                for i in range(len(column)):
                    if isinstance(column[i], int):
                        column[i] = str(column[i])
                lines_list.append(column)
            log.debug(f"excel lines list:{lines_list}")
        else :
            for r in worksheet.rows:
                column = [cell.value for cell in r]
                lines_list.append(column[0])            
            
    else :
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
    elif extension == "tsv" or extension =='ped' :
        return "\t"
    elif extension == "xlsx" :
        return extension
    else:
        error = "Import error : Wrong extension, only tsv and csv allowed"
        return error

def line_to_list(line:str):
    """
    >>>line_to_list('lias,fat,patient,"un,deux,trois",mom,Unaffected,M,"one,two,three"')
    ['lias', 'fat', 'patient', 'un,deux,trois', 'mom', 'Unaffected', 'M', 'one,two,three']
    """
    reader = csv.reader([line])
    result = next(reader)
    return result

def get_rows_list(lines_list:list , separator:str):
    file_as_list = []
    length = len(lines_list[0].split(separator))
    for i in range(len(lines_list)):
        if separator == "," and "\"" in lines_list[i]: 
            line_col_list = line_to_list(lines_list[i])
        else:       
            line_col_list = lines_list[i].split(separator)

        if line_col_list == [""]:
            continue
        file_as_list.append(line_col_list)
        if length != len(line_col_list):
            error = "Import error : The rows do not all have the same column number. Row " + str(i) + " has not the same number of columns as the header (which is row 0)."
            return error
    return file_as_list


def reform_columns(file_list:list, authorized_colnames:list): #only if header
    to_ignore=[]
    col_names_list = []

    flat_list = [item for sublist in authorized_colnames for item in sublist]
    col_names_list = []
    for index in range(len(file_list[0])):  # get good column names and uselesscolumns
        if file_list[0][index] not in flat_list :
            to_ignore.append(index)
            log.debug(f" colname ignored {file_list[0][index]} index {index}")
            continue
        col_names_list.append(file_list[0][index])

    #remove unwanted columns
    for line in file_list :
        for i in reversed(range(len(to_ignore))):
            line.pop(to_ignore[i])

    return col_names_list, file_list

def get_columns(file_list0:list,extension:str):
    list_col_order=[]
    error=""
    authorized_colnames =[["id","Individual ID","Patient ID", "ID"],
                          ["famID","Family ID", "FAMID"," Family ID"],
                [ "alias","Alias", "Aliases"],
                ["paternalID", "Paternal ID","father", "Father"],
                ["maternalID","Maternal ID","mother", "Mother"],
                ["sex","Sex" ],
                ["phenotype",  "Phenotype"],
                ["HPOList", "HPO List", "hpolist"],
                ["starkTags","Stark Tags","starktags","STARK Tags", "tags"]]

    if extension != 'ped' or '#' in file_list0[0][0]: #if header
        session['header'] = True
        if "id" not in file_list0[0] and "Patient ID" not in file_list0[0] and "ID" not in  file_list0[0] and 'Individual ID' not in file_list0[0]:
            error="Import error : An id column is missing in the header. It can be named 'id', 'Patient ID', 'Individual ID' or 'ID'."
            return error, None
    
        if '#' in file_list0[0][0]:
            file_list0[0][0] = file_list0[0][0][1:]

        col_names_list, file_list = reform_columns(file_list0, authorized_colnames)


        # find which column is in order and add the right name for the json
        for col_name in col_names_list: #for each column
            for col_options in authorized_colnames : #for each pack of allowed column names
                if col_name in col_options : #check if column name in allowed pack        
                    list_col_order.append(col_options[0]) #add the right name for the json

        return file_list,list_col_order
    
    elif extension == 'ped' and len(file_list0[0]) == 6 :
        session['header'] = False
        list_col_order = ["famID" ,"id", "paternalID","maternalID","sex","phenotype" ]
        return file_list0,list_col_order
    
    elif extension == 'ped' and len(file_list0[0]) == 9 :
        session['header'] = False
        list_col_order = ["famID" ,"id", "paternalID","maternalID","sex","phenotype","alias", "HPOList", "starkTags" ]
        return file_list0,list_col_order
    
    else :
        error="Import error : Wrong format : a ped needs a header, or no header but 6 columns if it is a stric ped file or 9 columns if it is advanced"
        return error, None
    


def fill_dict(file_list:list, list_col_order:list):
    dict_list = []
    log.debug(f"SESSION HEADER {session['header']}")

    if session['header'] == False :
        addition=0
    else : # to not add the header to the table
        addition=1
        
    for line in range(len(file_list)-addition):  # get dictionnaries in list, for each line
        mydict = OrderedDict()
        for n in range(len(list_col_order)):  # get lines in dictionnaries, for each column
            column = list_col_order[n]
            value = file_list[line+addition][n]
            if column == "HPOList" or column == "starkTags":
                mydict[column] = value.split(',')
                
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
        dict_list.append(mydict)
    return dict_list



def merge_peds(dict_list:list):
    with open(session['CURRENT_FILE'], "r") as peds:
        log.debug(f"/up 2 curr: {session['CURRENT_FILE']}")
        data = json.load(peds)
        peds_merged = data + dict_list
        return peds_merged