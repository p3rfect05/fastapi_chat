import math
from sys import maxsize
from itertools import permutations

def tsp(graph, s):
    V = len(graph)
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
    min_cost = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:
        current_cost = 0
        k = s
        for j in i:
            current_cost += graph[k][j]
            k = j
        current_cost += graph[k][s]
        min_cost = min(min_cost, current_cost)
    return min_cost
#graph1 = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]] # РґР»СЏ РїСЂРѕРІРµСЂРєРё (РїРѕСЃРјРѕС‚СЂРµС‚СЊ РєР°СЂС‚РёРЅРєСѓ)
graph2 = [[math.inf, 8, 4, 10], [8, math.inf, 7, 5], [4, 7, math.inf, 3], [10, 5, 3, math.inf]]

adj1 = [
    [math.inf, 7, 12, 25, 10],
    [10, math.inf, 9, 5, 11],
    [13, 8, math.inf, 6, 4],
    [6, 11, 15, math.inf, 15],
    [5, 9, 12, 17, math.inf]
]
adj2 = [
    [math.inf, 7, 11, 10, 13, 10],
    [15, math.inf, 14, 10, 12, 6],
    [9, 6, math.inf, 10, 1, 6],
    [19, 7, 5, math.inf, 13, 13],
    [4, 7, 5, 10, math.inf, 11],
    [8, 7, 3, 10, 4, math.inf]
]
print(tsp(adj2, 0))
'''
Р—Р°РґР°С‡Р° РєРѕРјРјРёРІРѕСЏР¶С‘СЂР° (Travelling Salesman Problem, TSP) вЂ” Р·Р°РґР°С‡Р° РєРѕРјР±РёРЅР°С‚РѕСЂРЅРѕР№ РѕРїС‚РёРјРёР·Р°С†РёРё. 
РљР°Рє РїСЂР°РІРёР»Рѕ, РµС‘ СЃСѓС‚СЊ СЃРІРѕРґРёС‚СЃСЏ Рє РїРѕРёСЃРєСѓ РѕРїС‚РёРјР°Р»СЊРЅРѕРіРѕ РїСѓС‚Рё, 
РїСЂРѕС…РѕРґСЏС‰РµРіРѕ С‡РµСЂРµР· РІСЃРµ РїСЂРѕРјРµР¶СѓС‚РѕС‡РЅС‹Рµ РїСѓРЅРєС‚С‹ РїРѕ РѕРґРЅРѕРјСѓ СЂР°Р·Сѓ Рё РІРѕР·РІСЂР°С‰Р°СЋС‰РµРіРѕСЃСЏ РІ РёСЃС…РѕРґРЅСѓСЋ С‚РѕС‡РєСѓ.
'''