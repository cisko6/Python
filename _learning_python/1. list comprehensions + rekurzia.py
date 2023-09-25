
############################ NA KILOMETER #####################################################
"""def list_of_lists(pole_cisel):
    result = []
    for cislo in pole_cisel:
        pomresult = []
        count = 0
        while True:
            if count >= cislo:
                break
            pomresult.append(count)
            count += 1
        result.append(pomresult)
    return result

print(list_of_lists([1,2,3,4,5]))"""
############################### LIST COMPREHENSIONS ##################################################

""""def lit_of_lists(pole_cisel):
    return [ list(range(0, cislo+1)) for cislo in pole_cisel if cislo >= 0]
print(lit_of_lists([0,1,2,3]))"""

########## PRIKLAD 2
# Suppose, we want to separate the letters of the word human and add the letters as items of a list
"""def fnc(string):
    return [letter for letter in string ]
result = fnc("human")
print(" ".join(result))"""


############################# SKUSKA REKURZIE ####################################################

"""def rekurzia(cislo, pole):
    if cislo < 0:
        return pole
    pole.append(cislo)
    return rekurzia(cislo - 1, pole)

pole = []
rekurzia(5, pole)
print(list(reversed(pole)))"""

#################################################################################
