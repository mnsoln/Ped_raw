import glob




def getFiles():
    files=glob.glob('../Data/*.json')
    return files


def getNameFile(files, mode):
    if mode == "split":
        file_list=[]
        for file in files:
            split = file.split('/')
            file_list.append(split[len(split)-1][:-5])
    elif mode == "get" :
        file_list=[]
        for file in files :
            file_list.append("../Data/" + file + ".json")
    return file_list


files_split = ["../Data/data2.json", "../Data/new4.json", "../Data/new.json"]
files_get = ['data2', 'new4', 'new']
print(getNameFile(files_get, "get"))
print('go')





