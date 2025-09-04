peso_total = 0.0
for volta in range(1,11,1):
    peso_atual = float(input("Digite o peso atual: "))
    peso_total = peso_atual + peso_atual * volta
    peso_medio = peso_total / 10
print(f"Peso total: {peso_total}\nPeso médio: {peso_medio}")
