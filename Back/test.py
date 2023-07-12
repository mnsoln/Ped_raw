

# # Alist = ['Mon','Tue','Wed','Tue']
# # print("The given list : ",Alist)
# # print(set(Alist))
# # Compare length for unique elements
# # if(len(set(Alist)) == len(Alist)):

# #    print("All elements are unique.")
# # else:
# #    print("All elements are not unique.")

# # colname_list = [["id","Patient ID", "ID"],
# #                 ["alias", "Aliases", "Alias"],
# #                 ["father", "Father"],
# #                 ["mother", "Mother"],
# #                 ["sex", "Sex"],
# #                 ["phenotype", "Phenotype"],
# #                 ["HPOList", "HPO List", "hpolist"],
# #                 ["starkTags","Stark Tags","starktags"]
# # ]
# # ex=[["alias","id","mother"],["lol","yolo","salut"],3]

# # ex.pop(2)
# # print(ex)

# # for i in colname_list :
# #     for e in ex[0]:
# #         if e in i:
# #             print(e, i)



# import csv

# line = 'lias,fat,patient,"un,deux,trois",mom,Unaffected,M,"one,two,three"'
# line2 = '"un,deux,trois",lias,fat,patient,mom,Unaffected,M,"one,two,three"'

# # Create a CSV reader object
# reader = csv.reader([line])
# result1 = next(reader)

# reader = csv.reader([line2])
# result2 = next(reader)

# print(result1)
# print(result2)

# intt = 12
# stri = 'fam'
# lol = stri + str(intt)
# print(lol)
string = 'fam002'
print(string[-3:])
print(int(string[-3:]))
print(len(str(int(string[-3:]))))

