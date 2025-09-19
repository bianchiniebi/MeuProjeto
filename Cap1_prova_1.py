import subprocess
import pandas as pd

# VETORES
culturas_disponiveis = ["Café", "Cana-de-açúcar"]
insumos_cafe = ["Fosfato", "Nitrogênio", "Calagem"]
insumos_cana = ["NPK", "Ureia", "Cloreto de Potássio"]

# VETORES PARA ARMAZENAR REGISTROS
culturas = []
areas = []
insumos = []
quantidades = []

# FUNÇÃO PARA MOSTRAR TABELA
def mostrar_tabela():
    if len(culturas) == 0:
        print("Nenhum dado cadastrado!")
        return
    print("{:<3} {:<17} {:<13} {:<25} {:<10}".format("ID", "Cultura", "Área(m²)", "Insumo", "Qtd(L)"))
    print("-"*68)
    for i in range(len(culturas)):
        print("{:<3} {:<17} {:<13} {:<25} {:<10}".format (i, culturas[i], round(areas[i], 2), insumos[i], round(quantidades[i], 2)))


# FUNÇÃO PARA ESCOLHA
def input_numero(prompt, min_val=None, max_val=None):
    while True:
        valor = input(prompt)
        if valor.isdigit():
            valor_int = int(valor)
            if (min_val is not None and valor_int < min_val) or (max_val is not None and valor_int > max_val):
                print("Número fora do intervalo, tente novamente.")
            else:
                return valor_int
        else:
            print("Digite apenas números inteiros!")

def input_float(prompt):
    while True:
        try:
            valor = float(input(prompt))
            return valor
        except:
            print("Digite um número válido!")

# MENU
while True:
    print("\nMENU PRINCIPAL")
    print("1 - Inserir dados")
    print("2 - Mostrar dados")
    print("3 - Alterar dados")
    print("4 - Deletar dados")
    print("5 - Calcular estatísticas (R)")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    # INSERIR DADOS
    if opcao == "1":
        print("\nCulturas disponíveis:")
        for i, c in enumerate(culturas_disponiveis):
            print(i, "-", c)
        escolha = input_numero("Escolha a cultura (número): ", 0, len(culturas_disponiveis)-1)
        cultura = culturas_disponiveis[escolha]
        insumos_disp = insumos_cafe if cultura == "Café" else insumos_cana

        lado1 = input_float("Digite o 1º lado da área (m): ")
        lado2 = input_float("Digite o 2º lado da área (m): ")
        area = lado1 * lado2

        print("\nInsumos disponíveis:")
        for i, ins in enumerate(insumos_disp):
            print(i, "-", ins)
        escolha_ins = input_numero("Escolha o insumo (número): ", 0, len(insumos_disp)-1)
        insumo = insumos_disp[escolha_ins]

        qtd = input_float("Quantidade por metro (mL): ")
        ruas = input_numero("Número de ruas: ")
        comp = input_float("Comprimento da rua (m): ")
        total = qtd * ruas * comp / 1000

        culturas.append(cultura)
        areas.append(area)
        insumos.append(insumo)
        quantidades.append(round(total,2))
        print("Registro adicionado!")

    # MOSTRAR DADOS
    elif opcao == "2":
        mostrar_tabela()

    # ALTERAR DADOS
    elif opcao == "3":
        if len(culturas) == 0:
            print("Nenhum dado para alterar!")
            continue
        mostrar_tabela()
        idx = input_numero("Digite o ID do registro que deseja alterar: ", 0, len(culturas)-1)

        print("\n--- Alterando registro ---")
        print("\nCulturas disponíveis:")
        for i, c in enumerate(culturas_disponiveis):
            print(i, "-", c)
        escolha = input_numero("Escolha a cultura (número): ", 0, len(culturas_disponiveis)-1)
        cultura = culturas_disponiveis[escolha]
        culturas[idx] = cultura
        insumos_disp = insumos_cafe if cultura == "Café" else insumos_cana

        lado1 = input_float("Digite o 1º lado da área (m): ")
        lado2 = input_float("Digite o 2º lado da área (m): ")
        areas[idx] = lado1 * lado2

        print("\nInsumos disponíveis:")
        for i, ins in enumerate(insumos_disp):
            print(i, "-", ins)
        escolha_ins = input_numero("Escolha o insumo (número): ", 0, len(insumos_disp)-1)
        insumos[idx] = insumos_disp[escolha_ins]

        qtd = input_float("Quantidade por metro (mL): ")
        ruas = input_numero("Número de ruas: ")
        comp = input_float("Comprimento da rua (m): ")
        quantidades[idx] = round(qtd * ruas * comp / 1000,2)

        print("Registro alterado com sucesso!")

    # DELETAR DADOS
    elif opcao == "4":
        if len(culturas) == 0:
            print("Nenhum dado para deletar!")
            continue
        mostrar_tabela()
        idx = input_numero("Digite o ID para deletar: ", 0, len(culturas)-1)
        culturas.pop(idx)
        areas.pop(idx)
        insumos.pop(idx)
        quantidades.pop(idx)
        print("Registro deletado!")

    # ESTATÍSTICAS COM R
    elif opcao == "5":
        if len(culturas) == 0:
            print("Nenhum dado cadastrado!")
            continue

        # Salvar CSV
        df = pd.DataFrame({
            "Cultura": culturas,
            "Area_m2": areas,
            "Insumo": insumos,
            "Qtd_L": quantidades
        })
        df.to_csv("dados_temp.csv", index=False)

        # Criar script R externo
        with open("estatisticas.R", "w", encoding="utf-8") as f:
            f.write("""
dados <- read.csv("dados_temp.csv")
if(length(dados$Area_m2) > 1) { desvio_area <- sd(dados$Area_m2) } else { desvio_area <- 0 }
if(length(dados$Qtd_L) > 1) { desvio_qtd <- sd(dados$Qtd_L) } else { desvio_qtd <- 0 }
cat(sprintf("Média da área (m²): %.2f\\n", mean(dados$Area_m2)))
cat(sprintf("Desvio padrão da área (m²): %.2f\\n", desvio_area))
cat(sprintf("Média da quantidade (L): %.2f\\n", mean(dados$Qtd_L)))
cat(sprintf("Desvio padrão da quantidade (L): %.2f\\n", desvio_qtd))
""")

        # Executar script R
        resultado = subprocess.run(
            ["Rscript", "estatisticas.R"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        print("\n### Estatísticas calculadas pelo R ###")
        print(resultado.stdout)

    # SAIR
    elif opcao == "6":
        print("Encerrando o programa...")
        break

    else:
        print("Opção inválida! Tente novamente.")
