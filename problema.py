# importando bibliotecas
#!pip install pulp
import pulp

#PARAM:
custo = [5.1, 3.6, 6.8]

receita = [330, 300, 420]

pilotos_aptos = [30, 20, 10]

aviao = range(len(custo))

pesos_de_manutencao = [1, 3/4, 5/3]


# Declaração do objeto que representa o modelo matemático
modelo = pulp.LpProblem('problema 1', pulp.LpMaximize)


# VARIÁVEIS DE DECISÃO:
# x[i] = número de aviões do tipo i a serem adquiridos

avioes_adquiridos = pulp.LpVariable.dicts('avioes', aviao, lowBound=0)
pilotos_md = pulp.LpVariable.dicts('pilotos_md', aviao, lowBound=0)
#cat=pulp.LpInteger


# FUNÇÃO OBJETIVO:
modelo += pulp.lpSum(receita[i] * avioes_adquiridos[i] for i in aviao)


# RESTRIÇÕES:
#restrição de verba
modelo += pulp.lpSum(custo[i]*avioes_adquiridos[i] for i in aviao) <= 220

# Restrições de pilotos
modelo += (2*avioes_adquiridos[0]) <= pilotos_aptos[0] + pilotos_md[0]

modelo += (2*avioes_adquiridos[1]) <= pilotos_aptos[1] + pilotos_md[1]

modelo += (2*avioes_adquiridos[2]) <= pilotos_aptos[2] - pilotos_md[0] - pilotos_md[1]


#restrição de oficinas de manutenção
modelo += pulp.lpSum(pesos_de_manutencao[i]*avioes_adquiridos[i] for i in aviao) <= 40

status = modelo.solve()
print('status: ', pulp.LpStatus[status])
print('funcao objetivo: ', modelo.objective.value())
print('solucoes')
for a in aviao:
  print(a, avioes_adquiridos[a].value())