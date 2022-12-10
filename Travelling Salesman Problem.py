#pip install python-tsp

import pandas as pd
import urllib.request, json
import requests
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

#Data Collect
C = ['01001000', '13040709', '13484350','13083710','13970390','13971260',
     '13087506','13035000','13073003','03065010','04142091','13480357',
     '13098422','13331530','13400330','13065030','13348290','86055660','13348884']

'''
n = int(input("Digite o total de endereços desejados:\n"))
for k in range(0,n):
  C.append(input("Digite um CEP:\n"))
  while len(C[k]) !=8:
    C[k] = input("O CEP digitado é inválido! Digite novamente o CEP:\n")
print(C)
'''

#Address Mapper
print()
a = len(C)
Origem = []

for i in range(0,a):
    with urllib.request.urlopen(f"https://viacep.com.br/ws/{C[i]}/json/") as url:
        address = json.loads(url.read().decode())
    Origem.append(address['logradouro'] + ' - ' + address['bairro'] + ', '+ address['localidade']+' - '+address['uf']) # ', ' + Numero[i]+
    print(Origem[i])

l = len(Origem) #Coleta do tamanho da base de dados
count = 1 #Contador
D = np.zeros((l,l), dtype=np.float64) #Determinação da matriz de distâncias
T = np.zeros((l,l), dtype=np.float64) #Determinação da matriz de tempo

#Distance Counter
for i in range(0,l):
    for j in range(i+1,l):
        api_key = 'AIzaSyBqXlse9a2mSpKbEUjbY0umtQ27s_hM0_E'
        #api_key = 'AIzaSyAlfGOnPJkxy_8c1zG1LiFntMB_Gp64sbQ' #Chave de consulta reserva
        
        rota = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + Origem[i] + "&destinations=" + \
               Origem[j] + "&key=" + api_key #URL de coleta de dados
        response = requests.get(url=rota)
        
        result = response.json()
        D[i][j] = (float(result["rows"][0]['elements'][0]['distance']['value'])) #Criação da Matriz de distâncias triângular superior
        D[j][i] = D[i][j] #Criação da simetria da matriz
        T[i][j] = (float(result["rows"][0]['elements'][0]['duration']['value'])) #Criação da Matriz de distâncias triângular superior
        T[j][i] = D[i][j] #Criação da simetria da matriz
        
'''        
print()
print('Matriz de Distâncias:\n', D) #Impressão da matriz de distâncias
print()
print('Matriz de Distâncias:\n', T) #Impressão da matriz de distâncias
print()    
'''

#Solver TSP por distâncias
dist, distance = solve_tsp_dynamic_programming(D)
print("\nA ordem de estrega será:")
for i in range(0,l):
  print(i+1,'-',Origem[dist[i]])

#Solver TSP por tempo
time, distance = solve_tsp_dynamic_programming(T)
print("\nA ordem de estrega será:")
for i in range(0,l):
  print(i+1,'-',Origem[time[i]])