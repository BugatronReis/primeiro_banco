from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
        
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    
    def gerar_relatorio(self, tipo=None):
        for transacao in self._transacoes:
            if tipo is None or transacao["tipo"].lower() == tipo.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor <= 0:
            print("\nErro: O valor deve ser positivo.")
            return False
            
        if valor > self.saldo:
            print("\nErro: Saldo insuficiente.")
            return False
            
        self._saldo -= valor
        print(f"\n✓ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\nErro: O valor deve ser positivo.")
            return False
            
        self._saldo += valor
        print(f"\n✓ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes_do_dia() 
             if transacao["tipo"] == "Saque"]
        )
        
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        
        if excedeu_limite:
            print(f"\nErro: Valor máximo por saque é R$ {self._limite:.2f}.")
            return False
            
        if excedeu_saques:
            print(f"\nErro: Limite máximo de {self._limite_saques} saques diários atingido.")
            return False
            
        return super().sacar(valor)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\nErro: Limite diário de 10 transações atingido!")
            return
            
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

# Criação do cliente e conta
cliente = PessoaFisica(
    nome="João Silva",
    data_nascimento="15/01/1980",
    cpf="123.456.789-00",
    endereco="Rua ABC, 123 - Centro - São Paulo/SP"
)

conta = ContaCorrente.nova_conta(cliente=cliente, numero=1)
cliente.adicionar_conta(conta)

# Sistema interativo
while True:
    print("\n" + "="*20)
    print("\n=== Menu ===")
    print("="*20)
    print("1. Depositar")
    print("2. Sacar")
    print("3. Extrato")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        try:
            valor = float(input("\nInforme o valor do depósito: "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)
        except ValueError:
            print("\nErro: Valor inválido. Use números (ex: 100.50).")

    elif opcao == "2":
        try:
            valor = float(input("\nInforme o valor do saque: "))
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)
        except ValueError:
            print("\nErro: Valor inválido. Use números (ex: 50.00).")

    elif opcao == "3":
        print("\n" + "="*52)
        print("=== EXTRATO BANCÁRIO ===")
        print("="*52)
        print(f"{'Data/Hora':20} {'Operação':10} {'Valor':>15}")
        print("-"*52)
        
        tem_transacoes = False
        for transacao in conta.historico.gerar_relatorio():
            tem_transacoes = True
            tipo = "depósito" if transacao["tipo"] == "Deposito" else "saque"
            sinal = "+" if tipo == "depósito" else "-"
            valor_formatado = f"R$ {transacao['valor']:.2f}"
            print(f"{transacao['data']:20} {tipo:10} {sinal}{valor_formatado:>14}")
        
        if not tem_transacoes:
            print("Nenhuma transação realizada.".center(52))
        
        print("-"*52)
        print(f"{'SALDO ATUAL:':30} R$ {conta.saldo:.2f}")
        print("="*52)

    elif opcao == "4":
        print("\nObrigado por usar nosso sistema bancário!")
        break

    else:
        print("\nOpção inválida. Por favor, escolha 1, 2, 3 ou 4.")