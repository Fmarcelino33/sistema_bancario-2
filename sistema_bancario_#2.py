import textwrap
from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self.agencia = "0001"
        self.saldo = 0
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao("Depósito", valor)
            print("\n=== Depósito realizado com sucesso! ===")
            print(f"Saldo atual: R$ {self.saldo:.2f}.") #AQUI SERÁ EXIBIDO O SALDO ATUAL
            return True
        else:
            print("\n@@@ Valor inválido para depósito @@@")
            return False

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Saldo insuficiente @@@")
            return False
        elif valor <= 0:
            print("\n@@@ Valor inválido para saque @@@")
            return False
        else:
            self.saldo -= valor
            self.historico.adicionar_transacao("Saque", valor)
            print("\n=== Saque realizado com sucesso! ===")
            print(f"Saldo atual: R$ {self.saldo:.2f}.") #AQUI SERÁ EXIBIDO O SALDO ATUAL
            return True

    def mostrar_extrato(self):
        print("\n================ EXTRATO ================")
        if not self.historico.transacoes:
            print("Não houve movimentações nesta conta.")
        else:
            for transacao in self.historico.transacoes:
                #print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
                print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - {transacao['data']}")
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print("=========================================")

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite_saques=3, limite=500):
        super().__init__(cliente, numero)
        self.limite_saques = limite_saques
        self.limite = limite

    def sacar(self, valor):
        saques_hoje = sum(1 for t in self.historico.transacoes 
                         if t['tipo'] == "Saque" and t['data'].startswith(datetime.now().strftime("%d-%m-%Y")))
        
        if saques_hoje >= self.limite_saques:
            print("\n@@@ Limite de saques diários atingido @@@")
            return False
        elif valor > self.limite:
            print("\n@@@ Valor excede o limite por saque @@@")
            return False
        else:
            return super().sacar(valor)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo cliente
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":  # Depositar
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado!")
                continue
            
            if not cliente.contas:
                print("Cliente não tem contas!")
                continue

            conta = cliente.contas[0]  # Pega a primeira conta (simplificado)
            valor = float(input("Valor para depósito: "))
            conta.depositar(valor)

        elif opcao == "2":  # Sacar
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado!")
                continue

            if not cliente.contas:
                print("Cliente não tem contas!")
                continue

            conta = cliente.contas[0]
            valor = float(input("Valor para saque: "))
            conta.sacar(valor)

        elif opcao == "3":  # Extrato
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado!")
                continue

            if not cliente.contas:
                print("Cliente não tem contas!")
                continue

            conta = cliente.contas[0]
            conta.mostrar_extrato()

        elif opcao == "4":  # Nova conta
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado!")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente(cliente, numero_conta)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("Conta criada com sucesso!")

        elif opcao == "5":  # Listar contas
            for conta in contas:
                print(f"\nAgência: {conta.agencia}")
                print(f"Número: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")
                print(f"CPF: {cliente.cpf}")
                print(f"Endereço:{cliente.endereco}")
                print(f"Saldo: R$ {conta.saldo:.2f}")
                print("=" * 40)

        elif opcao == "6":  # Novo cliente
            nome = input("Nome completo: ")
            cpf = input("CPF (apenas números): ")
            if any(c.cpf == cpf for c in clientes):
                print("CPF já cadastrado!")
                continue

            endereco = input("Endereço (rua, nro - bairro - cidade/UF): ")
            cliente = Cliente(nome, cpf, endereco)
            clientes.append(cliente)
            print("Cliente cadastrado com sucesso!")

        elif opcao == "0":
             print("Obrigado por usar nossos serviços. Até breve!.")
             break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()