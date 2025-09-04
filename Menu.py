print("0 - Sair")
print("1 - Positivo, Negativo ou Nulo")
print("2 - Calcular desconto")
print("3 - Maior entre dois números")
opcao = int(input("Digite uma opção: "))
if opcao == 1:
    num = int(input("Digite um numero: "))
    if num > 0:
        print("Positivo")
    elif num < 0:
        print("Negativo")
    else:
        print("Nulo")
elif opcao == 2:
    compra = float(input("Digite o valor da compra: "))
    if compra > 300:
        compra_desc = compra*0.9
    else:
        compra_desc = compra*0.95
    print(f'Valor da compra: {compra:.2f}\nValor da compra desc: {compra_desc:.2f}')
elif opcao == 3:
    num1 = int(input("Digite um numero: "))
    num2 = int(input("Digite outro numero: "))
    if num1 > num2:
        print(num1)
    elif num1 < num2:
        print(num2)
    else:
        print("Número inválido")
elif opcao == 0:
    print("Obrigado por usar o programa")
else:
    print("opção inválida")