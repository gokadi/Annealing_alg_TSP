import numpy as np
import random as rd
import copy
from math import exp,log1p


def makeS1(n, pack):
    # Tmax, Tmin, dist, pack
    energy = 0
    dist = np.random.sample((n, n)) * 100
    for i in range(n):  # формируем симметричную матрицу стоимостей из случайных чисел
        for j in range(n):
            dist[i][j] = round(dist[j][i], 2)
            dist[j][j] = 0
    print(dist)
    # делим матрицу стоимостей на объем входящего пакета
    for i in range(n):
        for j in range(n):
            dist[i][j] = dist[i][j] / pack
    # print(dist)
    route = np.array([z + 1 for z in range(n)])
    for i in range(n - 1):
        energy = energy + dist[route[i] - 1][route[i + 1] - 1]

    # for i in range(np.max(route)-1):
    #     dist[route[i]-1][route[i+1]-1]=10000
    return route, energy, dist

# Ввод температуры с проверкой на ввод символа и проверкой tmax>tmin
def t_input():
    tmax = 0
    tmin = 0
    while tmax <= tmin:
        try:
            tmin = round(float(input('Введите минимальную температуру: ')), 2)
            tmax = round(float(input('Введите максимальную температуру: ')), 2)
            if tmax <= tmin:
                print('Введите корректные значения(tmax>tmin)!')
        except ValueError:
            print('Введите число в корректной форме!')
    return tmax, tmin


def make_p(p):
    a = rd.random()
    if a <= p:
        return 1
    else:
        return 0


def fliparr(route_p, n):
    # Цикл ниже делает из массива 1,2,3,4-> 1,4,3,2. 1 Элемент на месте, остальные- переворачиваются
    id1 = rd.randrange(2, n, 1)
    id2 = rd.randrange(2, n, 1)
    if id1> id2:
        tmp=id1
        id1=id2
        id2=tmp
        #id1, id2 = id2, id1
    else:
        if id1== id2:
            id2 += 1
    #print(id1+1,id2)
    # temp = np.zeros((2, id2 - id1 + 1))
    #print(route_p[id1],route_p[id2])
    #print(id1,id2)
    route_p[id1:id2+1] = copy.deepcopy(np.flipud(route_p[id1:id2+1]))#вот тут route_p
    #(np.flipud(route[id1 - 1:id2))
    #print(route_p)
    # temp[0] = copy.deepcopy(route[id1:id2 + 1])
    # temp = np.fliplr(temp)
    # print(temp)
    # for k in range(id2 - id1 + 1):
    #    route_p[id1 + k] = copy.deepcopy(temp[0, k])
    return route_p

def decrease_temp_1(tmax,tcurr, k):
    tcurr = tmax - k
    k = k + 1
    return tcurr, k

def decrease_temp_2(tmax,tcurr,k):
    tcurr=tmax/k
    k=k+1
    return tcurr,k

def decrease_temp_3(tmax,tcurr,k):
    c=0.7
    tcurr=tcurr*c
    return tcurr,k

def decrease_temp_4(tmax,tcurr,k):
    tcurr=tmax/(log1p(1+k))
    k=k+10
    return tcurr,k

def decrease_temp_5(tmax,tcurr,k):
    tcurr=tcurr/exp(0.05*k)
    #k=k+1
    return tcurr,k

# алгоритм отжига
def make_new_state(tmin, tmax, n, route, dist, energy,modde):
    tcurr = tmax
    energy_hist=[]
    energy_hist.append(energy)
    route_p = copy.deepcopy(route)
    num_it=0
    k = 2
    while tcurr > tmin:
        energy_p = 0
        # print('итерация цикла')
        route_p = fliparr(route_p, n)
        # print(route_p)
        for i in range(n - 1):
            energy_p = energy_p + dist[route_p[i] - 1][route_p[i + 1] - 1]
            # print(i," ",energy_p)
            # print(route_p)
        if energy_p <= energy:
            energy = energy_p
            route = copy.deepcopy(route_p)
            num_it=num_it+1
            energy_hist.append(energy_p)
        else:
            p = exp(-(energy_p - energy) / tcurr)
            if make_p(p):
                # print(p)
                energy = energy_p
                route = copy.deepcopy(route_p)
                num_it = num_it + 1
                energy_hist.append(energy_p)
        if modde ==1:
            tcurr, k = decrease_temp_1(tmax,tcurr, k)
        if modde ==2:
            tcurr, k = decrease_temp_2(tmax,tcurr, k)
        if modde ==3:
            tcurr, k = decrease_temp_3(tmax,tcurr, k)
        if modde ==4:
            tcurr, k = decrease_temp_4(tmax,tcurr, k)
        if modde ==5:
            tcurr, k = decrease_temp_5(tmax,tcurr, k)
        # print(energy)
        if tcurr <= tmin:
            break


    return route, energy,num_it,energy_hist