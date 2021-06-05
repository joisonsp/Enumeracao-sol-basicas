#Trabalho de JÓISON OLIVEIRA PEREIRA e CARLOS AUGUSTO PEREIRA MAIA
#MATRÍCULAS: 20170068553 e 20190173162

# -*- coding: utf-8 -*-

print("TRABALHO DE JOISON OLIVEIRA PEREIRA E CARLOS AUGUSTO PEREIRA MAIA")
print("MATRICULAS: 20170068553 e 20190173162")

import numpy as np 
import itertools as itl

def crie_matriz(nLinhas, nColunas, valor):
    matriz = [] # lista vazia
    j = 0
    for i in range(nLinhas):
        # cria a linha i
        linha = [] # lista vazia
        for j in range(nColunas):
            linha.append(valor[j])
        # coloque linha na matriz
        matriz.append(linha)
    return matriz

#lendo arquivo
file = open("instance1.txt","r")

instancia = []

for line in file:
    instancia.append(line.rstrip())
    
#Numero de Variaveis
nVar = int(instancia[0].split()[0])
print("Numero de variaveis: "+ str(nVar))

#Numero de Restrições
nRes = int(instancia[0].split()[1])
print("Numero de restricoes: " + str(nRes))

#Os coeficientes
coeficientes = [] 
for coef in range(0,nVar):
    coeficientes.append(int(instancia[1].split()[coef]))
print("Coeficientes: "+ str(coeficientes))

#As restrições
trestricoes = instancia[2:]
restricoes = []

#b = instancia[2:][nVar]
#print('B É: ' + str(b))

for i in trestricoes:
    restricoes.append((i.split()))
i = -1
t = len(restricoes)
while i < t-1:
    i=i+1
    j=0
    while j < (nVar+1):
        restricoes[i][j] = int(restricoes[i][j])
        j=j+1
print("Restricoes: ", restricoes)

i = 0
b = []
while i <= t-1:
    b.append(restricoes[i][nVar])
    i+=1

print("Coeficientes restritivos: " + str(b))

#print(instancia)

# Colocando na forma padrão

nVar = nVar + nRes

i = 0

while i < nRes:
    coeficientes.append(0)
    i+=1

# Transpondo a matriz dos coeficientes

coeficientes = crie_matriz(1,nVar,coeficientes)

print("FORMA PADRAO")
print("Coeficientes da função objetivo na forma padrao: "+ str(coeficientes))

# Transpondo b

b = crie_matriz(1, nRes, b)

b = np.transpose(b)

print("B TRANSPOSTO: " + str(b))

# Criando A

x = []
x_aux = []

a = restricoes
i=0
for i in range(len(a)):
    a[i].pop()

    for j in range(nRes):
        if j == i:
            a[i].append(-1)
        else:
            a[i].append(0)
print("A: "+ str(a))

for i in range(len(a)):
    x_aux = []
    for j in range(len(a[0])):
        x_aux.append(str(j+1))
    x.append(x_aux)

print("variaveis x: "+ str(x))

def interpola(matriz, comb):
    combinacoes = list(itl.combinations(matriz, comb))
    listas = []
    listas_aux = []
    for i in range(len(combinacoes)):
        for j in range(comb):
            listas_aux.append(list(itl.combinations(matriz, comb))[i][j])
        listas.append(listas_aux)
        global tam
        tam = len(listas)
        listas_aux = []
    return listas

combina = []
for v in range(nRes):
  lista = a[v]
  #print("LISTA É:" +str(lista))
  combina = list(combina + interpola(lista, nRes))
#combina = np.transpose(combina)
#print("Combinacoes da matriz A: "+ str(combina))

combina_x = []
for v in range(nRes):
  lista_x = x[v]
  #print("LISTA_X É:" +str(lista_x))
  combina_x = list(combina_x + interpola(lista_x, nRes))

#print("Combinacoes da matriz X: "+ str(combina_x))

posicao = []

possiveis_sol = []
s = []
j = tam
i = 0
for i in range(len(combina)):
    if j < (len(combina) - 1):
        s.append(combina[i]) 
        s.append(combina[j])
    elif j == len(combina)-1:
        break
    #s = np.transpose(s)
    #print("S É: " + str(s))
    if np.linalg.det(s) != 0:
        possiveis_sol = possiveis_sol + s
        posicao.append(combina_x[i])
    j+=1    
    s = []

#print("posicao: " + str(posicao))
#print("Possiveis solucoes: " + str(possiveis_sol))

# Criando a matriz B com as possíveis soluções
B_solucoes = []
B_aux = []
i = 0
j = 1

x_aux = []
x_solucoes = []

while i < len(possiveis_sol):
    B_aux.append(possiveis_sol[i])
    B_aux.append(possiveis_sol[j])

    i += 2
    j += 2
    B_solucoes.append(B_aux)
    x_solucoes.append(x_aux)
    B_aux = []

#print("Todas as solucoes basicas: " + str(B_solucoes))

# Aplicando a formula XB = B^-1b

inversa = np.linalg.inv(B_solucoes)

#print("A INVERSA É:" +str(inversa))

x_B = []

x_B = inversa.dot(b)

print("")
print("Todas as solucoes basicas: ")
print("x_B:" + str(x_B))

# Listando as soluções viáveis
solucoes_viaveis = []
solucoes_aux = []

posicao_solucao = []

i = 0
for solucao in x_B:
    for elemento in solucao:
        if elemento > 0:
            solucoes_aux.append(round(float (elemento)))
        else:
            solucoes_aux.clear()
            break
    if len(solucoes_aux) > 0:
        solucoes_viaveis.append(solucoes_aux)
        posicao_solucao.append(i)
        solucoes_aux = []
    i+=1

print("Solucoes Viaveis: " + str(solucoes_viaveis))
#print("Posicao_solucao: " + str(posicao_solucao))

# Atualizando os valores das variáveis

v_faltantes = []
v_faltantes_aux = []

for i in range(len(solucoes_viaveis)):
    v_faltantes_aux = []
    for j in range(nVar):
        v_faltantes_aux.append(0)
    v_faltantes.append(v_faltantes_aux)

#print("v_faltantes: " + str(v_faltantes))

posicao_a = []
for i in range(len(posicao_solucao)):
    posicao_a.append(posicao[posicao_solucao[i]])

#print("posicao_a:"+str(posicao_a))

posicao = posicao_a

for i in range(len(solucoes_viaveis)):
    for j in range(nRes):
        v_faltantes[i][int(posicao[i][j])-1] = solucoes_viaveis[i][j]
#print("V_faltantes:" + str(v_faltantes))

# Calculando Z

solucoes_viaveis = v_faltantes

lista_z = []
z_aux = []
soma = 0

for solucao in solucoes_viaveis:
    z_aux.append(np.multiply(solucao, coeficientes)) 
print("Resultado do produto entre os coeficientes da funcao objetivo e os valores das variaveis: " )
print(z_aux)
for array in z_aux:
    soma = 0
    for funcao in array:
        for elemento in funcao:
            soma += elemento
    lista_z.append(soma)

print ("Lista dos resultados da funcao objetivo:" +str(lista_z))

# Achando a solução ótima

maior = 0
for elemento in lista_z:
    if elemento > maior:
        maior = elemento

print ("A solucao otima encontrada: " + str(maior))