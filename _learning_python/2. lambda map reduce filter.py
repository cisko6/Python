------------------------------------------------- MAP -----------------------------------------------------------------------------
# Map funkcia sa pouziva na aplikaciu funkcie na cele zoskupenie
numbers = [2, 3, 4, 5, 6]

def return_power(number, power=2):
    return number**power

print(list(map(return_power, numbers)))
print(list(map(lambda x: x**2, numbers)))

-------------------------------------------- FILTER ----------------------------------------------------------------------------------
# Filter funkcia sa pouziva na vyfiltrovanie elementov v zoskupeni pomocou funkcie
numbers = [2, 3, 4, 5, 6]

def is_even(number):
    return number % 2 == 0

print(list(filter(is_even, numbers)))
print(list(filter(lambda x: x%2 == 0, numbers)))

------------------------------------------------REDUCE------------------------------------------------------------------------------
# Reduce funkcia sa pouziva na spajanie elementov c poli reduce funkcia ma dve hodnoty cumulativnu hodnotu a aktualny prvok.
from functools import reduce

numbers = [2, 3, 4, 5, 6]

def reduce_sum(a, b):
    return a + b

print(reduce(reduce_sum, numbers))
print(reduce(lambda x,y: x+y, numbers))

------------------------------------------------------------------------------------------------------------------------------
# sprav z kazdeho cisla tuple ktory vrati cislo a jeho zapornu hodnotu
numbers = [1,2,3,4,5]
print(list(map( lambda number: (number, number*(-1)), numbers)))

------------------------------------------------ KUS EXTREMIK ------------------------------------------------------------------------------
# faktorial použitím MAP a REDUCE
from functools import reduce
numbers = range(1,11)
print(list(map(lambda x: reduce(lambda y,z: y*z,range(1,x+1)) , numbers)))


