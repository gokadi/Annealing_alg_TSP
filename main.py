import func
import copy
from matplotlib import pyplot as plt
import numpy as np

n=0
while n<2:
    n = int(input('Введите число ПК в сети: '))
    if n<2:
        print('Введите n больше 2')
    else:
        break
try:
    pack = float(input('Введите объем пакета: '))
except ValueError:
    print("Введите число, не символ!")
    pack = int(input('Введите объем пакета: '))
route0, energy0, dist = func.makeS1(n, pack)
print(route0)
print(energy0)
tmax, tmin = func.t_input()
route,energy,num_it,energy_hist,dist_end=func.make_new_state(tmin,tmax,n,route0,dist,energy0)
print(route)
print(energy)
print(energy_hist)
