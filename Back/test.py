

# Alist = ['Mon','Tue','Wed','Tue']
# print("The given list : ",Alist)
# print(set(Alist))
# Compare length for unique elements
# if(len(set(Alist)) == len(Alist)):

#    print("All elements are unique.")
# else:
#    print("All elements are not unique.")

colname_list = [["id","Patient ID", "ID"],
                ["alias", "Aliases", "Alias"],
                ["father", "Father"],
                ["mother", "Mother"],
                ["sex", "Sex"],
                ["phenotype", "Phenotype"],
                ["HPOList", "HPO List", "hpolist"],
                ["starkTags","Stark Tags","starktags"]
]
ex=[["alias","id","mother"],["lol","yolo","salut"],3]

ex.pop(2)
print(ex)

# for i in colname_list :
#     for e in ex[0]:
#         if e in i:
#             print(e, i)
