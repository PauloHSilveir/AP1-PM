from pulp import LpProblem, LpVariable, LpMaximize, LpInteger, PULP_CBC_CMD, value, LpStatus

# -----------------------
# Dados do problema
# -----------------------
c1, c2, c3 = 5.1, 3.6, 6.8        # custos (milhões $)
r1, r2, r3 = 330, 300, 420        # receitas (milhões $)
budget = 220                      # verba disponível (milhões $)

pilots_717 = 30                   # pilotos habilitados em 717
pilots_737 = 20                   # pilotos habilitados em 737-500
pilots_md = 10                    # pilotos habilitados em MD-11 (podem voar todos)
maint_capacity_eq = 40            # capacidade manutenção (em equivalentes de 717)

# -----------------------
# Modelo
# -----------------------
prob = LpProblem("Compra_Avioes", LpMaximize)

# Variáveis de decisão
n1 = LpVariable("n1_717", lowBound=0, cat=LpInteger)          # nº Boeing 717
n2 = LpVariable("n2_737500", lowBound=0, cat=LpInteger)       # nº Boeing 737-500
n3 = LpVariable("n3_MD11", lowBound=0, cat=LpInteger)         # nº MD-11

# Alocação de pilotos MD
y1 = LpVariable("y1_MD_to_717", lowBound=0, cat=LpInteger)
y2 = LpVariable("y2_MD_to_737", lowBound=0, cat=LpInteger)
y3 = LpVariable("y3_MD_to_MD11", lowBound=0, cat=LpInteger)

# -----------------------
# Função objetivo
# -----------------------
prob += r1*n1 + r2*n2 + r3*n3, "Receita_Total"

# -----------------------
# Restrições
# -----------------------

# Orçamento
prob += c1*n1 + c2*n2 + c3*n3 <= budget, "Orcamento"

# Capacidade manutenção (equivalentes 717)
prob += n1 + (3/4)*n2 + (5/3)*n3 <= maint_capacity_eq, "Manutencao"

# Pilotos
prob += 2*n1 <= pilots_717 + y1, "Pilotos_717"
prob += 2*n2 <= pilots_737 + y2, "Pilotos_737"
prob += 2*n3 <= y3, "Pilotos_MD11"

# Total de pilotos MD disponíveis
prob += y1 + y2 + y3 <= pilots_md, "Pilotos_MD_total"

# -----------------------
# Resolver
# -----------------------
prob.solve(PULP_CBC_CMD(msg=1))  # msg=1 para exibir saída do solver

# -----------------------
# Resultados
# -----------------------
print("Status:", LpStatus[prob.status])
print("Receita total ótima (milhões $):", value(prob.objective))

print("\nNº de aeronaves a comprar:")
print("  Boeing 717      =", int(n1.value()))
print("  Boeing 737-500 =", int(n2.value()))
print("  MD-11          =", int(n3.value()))

print("\nAlocação de pilotos MD:")
print("  y1 (para 717)  =", int(y1.value()))
print("  y2 (para 737)  =", int(y2.value()))
print("  y3 (para MD-11) =", int(y3.value()))
