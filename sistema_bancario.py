from abc import ABC, abstractmethod
import re


# ======================================================
# EXCEÇÕES PERSONALIZADAS
# ======================================================


class SaldoInsuficienteError(Exception):
    """Erro gerado quando uma operação excede o saldo disponível."""

    pass


# ======================================================
# CLASSE CLIENTE
# ======================================================


class Cliente:
    """Representa um cliente do sistema bancário."""

    def __init__(self, nome, email):
        """Inicializa um cliente."""

        self.nome = nome
        self.email = email

    @property
    def nome(self):
        """Retorna o nome do cliente."""

        return self._nome

    @nome.setter
    def nome(self, valor):
        """Valida e define o nome."""

        if not isinstance(valor, str):
            raise TypeError("O nome deve ser uma string.")

        valor = valor.strip()

        if len(valor) < 3:
            raise ValueError(
                "O nome deve possuir pelo menos 3 caracteres."
            )

        self._nome = valor

    @property
    def email(self):
        """Retorna o e-mail do cliente."""

        return self._email

    @email.setter
    def email(self, valor):
        """Valida e define o e-mail."""

        if not isinstance(valor, str):
            raise TypeError("O e-mail deve ser uma string.")

        valor = valor.strip().lower()

        padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.fullmatch(padrao_email, valor):
            raise ValueError("Formato de e-mail inválido.")

        self._email = valor

    def __str__(self):
        """Representação amigável do cliente."""

        return f"{self.nome} ({self.email})"

    def __repr__(self):
        """Representação técnica do cliente."""

        return (
            f"Cliente(nome='{self.nome}', "
            f"email='{self.email}')"
        )

    def __eq__(self, outro):
        """Compara clientes pelo e-mail."""

        if not isinstance(outro, Cliente):
            return False

        return self.email == outro.email


# ======================================================
# CLASSE ABSTRATA CONTA
# ======================================================


class Conta(ABC):
    """
    Classe abstrata que define o comportamento
    básico de uma conta bancária.
    """

    def __init__(
        self,
        numero,
        cliente,
        saldo=0.0
    ):
        """Inicializa uma conta."""

        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo

    @property
    def numero(self):
        """Retorna o número da conta."""

        return self._numero

    @numero.setter
    def numero(self, valor):
        """Valida o número da conta."""

        if not isinstance(valor, str):
            raise TypeError(
                "O número da conta deve ser uma string."
            )

        valor = valor.strip()

        if valor == "":
            raise ValueError(
                "O número da conta não pode ficar vazio."
            )

        self._numero = valor

    @property
    def cliente(self):
        """Retorna o cliente dono da conta."""

        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        """Garante que a conta receba um Cliente."""

        if not isinstance(valor, Cliente):
            raise TypeError(
                "A conta deve possuir um objeto Cliente."
            )

        self._cliente = valor

    @property
    def saldo(self):
        """Retorna o saldo atual."""

        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        """Valida o saldo."""

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "O saldo deve ser numérico."
            )

        if valor < 0:
            raise ValueError(
                "O saldo não pode ser negativo."
            )

        self._saldo = float(valor)

    def depositar(self, valor):
        """Realiza um depósito."""

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "O valor do depósito deve ser numérico."
            )

        if valor <= 0:
            raise ValueError(
                "O depósito deve ser maior que zero."
            )

        self._saldo += valor

        print(
            f"Depósito de R$ {valor:.2f} "
            f"realizado na conta {self.numero}."
        )

    def sacar(self, valor):
        """Realiza um saque."""

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "O valor do saque deve ser numérico."
            )

        if valor <= 0:
            raise ValueError(
                "O saque deve ser maior que zero."
            )

        if valor > self._saldo:
            raise SaldoInsuficienteError(
                "Saldo insuficiente para realizar o saque."
            )

        self._saldo -= valor

        print(
            f"Saque de R$ {valor:.2f} "
            f"realizado na conta {self.numero}."
        )

    @abstractmethod
    def calcular_rendimento(self):
        """
        Define um contrato para cálculo de rendimento.

        Cada classe filha deve implementar
        sua própria versão.
        """

        pass

    @abstractmethod
    def tipo_conta(self):
        """Retorna o tipo da conta."""

        pass

    def __str__(self):
        """Representação amigável."""

        return (
            f"{self.tipo_conta()} | "
            f"Conta: {self.numero} | "
            f"Cliente: {self.cliente.nome} | "
            f"Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self):
        """Representação técnica."""

        return (
            f"{self.__class__.__name__}("
            f"numero='{self.numero}', "
            f"cliente={repr(self.cliente)}, "
            f"saldo={self.saldo})"
        )

    def __eq__(self, outra):
        """Compara contas pelo número."""

        if not isinstance(outra, Conta):
            return False

        return self.numero == outra.numero

    def __lt__(self, outra):
        """Permite ordenar contas pelo saldo."""

        if not isinstance(outra, Conta):
            return NotImplemented

        return self.saldo < outra.saldo


# ======================================================
# CONTA CORRENTE
# ======================================================


class ContaCorrente(Conta):
    """Representa uma conta corrente."""

    def __init__(
        self,
        numero,
        cliente,
        saldo=0.0,
        taxa_mensal=15.0
    ):
        """Inicializa uma conta corrente."""

        super().__init__(
            numero,
            cliente,
            saldo
        )

        self.taxa_mensal = taxa_mensal

    @property
    def taxa_mensal(self):
        """Retorna a taxa mensal."""

        return self._taxa_mensal

    @taxa_mensal.setter
    def taxa_mensal(self, valor):
        """Valida a taxa mensal."""

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "A taxa mensal deve ser numérica."
            )

        if valor < 0:
            raise ValueError(
                "A taxa mensal não pode ser negativa."
            )

        self._taxa_mensal = float(valor)

    def calcular_rendimento(self):
        """
        Conta corrente não gera rendimento.

        O resultado representa a cobrança
        da taxa mensal.
        """

        return -self.taxa_mensal

    def tipo_conta(self):
        """Retorna o tipo da conta."""

        return "Conta Corrente"

    def __str__(self):
        """Representação amigável."""

        return (
            f"{super().__str__()} | "
            f"Taxa mensal: R$ {self.taxa_mensal:.2f}"
        )

    def __repr__(self):
        """Representação técnica."""

        return (
            f"ContaCorrente("
            f"numero='{self.numero}', "
            f"cliente={repr(self.cliente)}, "
            f"saldo={self.saldo}, "
            f"taxa_mensal={self.taxa_mensal})"
        )


# ======================================================
# CONTA POUPANÇA
# ======================================================


class ContaPoupanca(Conta):
    """Representa uma conta poupança."""

    def __init__(
        self,
        numero,
        cliente,
        saldo=0.0,
        taxa_rendimento=0.005
    ):
        """Inicializa uma conta poupança."""

        super().__init__(
            numero,
            cliente,
            saldo
        )

        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        """Retorna a taxa de rendimento."""

        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        """Valida a taxa de rendimento."""

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "A taxa de rendimento deve ser numérica."
            )

        if valor < 0:
            raise ValueError(
                "A taxa de rendimento não pode ser negativa."
            )

        self._taxa_rendimento = float(valor)

    def calcular_rendimento(self):
        """Calcula o rendimento da poupança."""

        return (
            self.saldo
            * self.taxa_rendimento
        )

    def tipo_conta(self):
        """Retorna o tipo da conta."""

        return "Conta Poupança"

    def __str__(self):
        """Representação amigável."""

        percentual = (
            self.taxa_rendimento
            * 100
        )

        return (
            f"{super().__str__()} | "
            f"Rendimento: {percentual:.2f}%"
        )

    def __repr__(self):
        """Representação técnica."""

        return (
            f"ContaPoupanca("
            f"numero='{self.numero}', "
            f"cliente={repr(self.cliente)}, "
            f"saldo={self.saldo}, "
            f"taxa_rendimento={self.taxa_rendimento})"
        )


# ======================================================
# BANCO
# ======================================================


class Banco:
    """
    Representa um banco.

    O Banco TEM contas, portanto esta relação
    utiliza composição em vez de herança.
    """

    def __init__(
        self,
        nome,
        contas=None
    ):
        """Inicializa o banco."""

        self.nome = nome

        if contas is None:
            contas = []

        self._contas = []

        for conta in contas:
            self.adicionar_conta(conta)

    @property
    def nome(self):
        """Retorna o nome do banco."""

        return self._nome

    @nome.setter
    def nome(self, valor):
        """Valida o nome do banco."""

        if not isinstance(valor, str):
            raise TypeError(
                "O nome do banco deve ser uma string."
            )

        valor = valor.strip()

        if len(valor) < 2:
            raise ValueError(
                "Nome do banco inválido."
            )

        self._nome = valor

    @property
    def contas(self):
        """Retorna uma cópia da lista de contas."""

        return self._contas.copy()

    def adicionar_conta(self, conta):
        """Adiciona uma conta ao banco."""

        if not isinstance(conta, Conta):
            raise TypeError(
                "Somente objetos do tipo Conta podem ser adicionados."
            )

        if conta in self._contas:
            raise ValueError(
                "Essa conta já está cadastrada."
            )

        self._contas.append(conta)

    def saldo_total(self):
        """Calcula o saldo total das contas."""

        return sum(
            conta.saldo
            for conta in self._contas
        )

    def __str__(self):
        """Representação amigável."""

        return (
            f"Banco {self.nome} | "
            f"{len(self._contas)} contas | "
            f"Saldo total: R$ {self.saldo_total():.2f}"
        )

    def __repr__(self):
        """Representação técnica."""

        return (
            f"Banco("
            f"nome='{self.nome}', "
            f"contas={repr(self._contas)})"
        )


# ======================================================
# DEMONSTRAÇÃO / TESTES
# ======================================================


def demonstrar_sistema():
    """Executa a demonstração completa do sistema."""

    print("=" * 65)
    print("SISTEMA BANCÁRIO ORIENTADO A OBJETOS")
    print("=" * 65)

    # ==================================================
    # CRIAÇÃO DE CLIENTES
    # ==================================================

    cliente_1 = Cliente(
        "Rafael Tajra",
        "rafael@email.com"
    )

    cliente_2 = Cliente(
        "Ana Souza",
        "ana@email.com"
    )

    cliente_3 = Cliente(
        "Lucas Silva",
        "lucas@email.com"
    )

    cliente_4 = Cliente(
        "Mariana Costa",
        "mariana@email.com"
    )

    cliente_5 = Cliente(
        "Carlos Lima",
        "carlos@email.com"
    )

    # 5 instâncias até aqui.

    # ==================================================
    # CRIAÇÃO DE CONTAS
    # ==================================================

    conta_1 = ContaCorrente(
        "001",
        cliente_1,
        1500,
        20
    )

    conta_2 = ContaPoupanca(
        "002",
        cliente_2,
        3000,
        0.006
    )

    conta_3 = ContaCorrente(
        "003",
        cliente_3,
        800,
        15
    )

    conta_4 = ContaPoupanca(
        "004",
        cliente_4,
        5000,
        0.007
    )

    conta_5 = ContaCorrente(
        "005",
        cliente_5,
        2200,
        18
    )

    conta_6 = ContaPoupanca(
        "006",
        cliente_1,
        10000,
        0.008
    )

    # Agora temos 11 instâncias:
    # 5 clientes + 6 contas.

    contas = [
        conta_1,
        conta_2,
        conta_3,
        conta_4,
        conta_5,
        conta_6
    ]

    # ==================================================
    # BANCO - COMPOSIÇÃO
    # ==================================================

    banco = Banco(
        "Banco Python",
        contas
    )

    print("\n===== BANCO =====")

    print(
        banco
    )

    # ==================================================
    # REPRESENTAÇÃO DOS OBJETOS
    # ==================================================

    print("\n===== CONTAS =====")

    for conta in contas:
        print(conta)

    # ==================================================
    # POLIMORFISMO
    # ==================================================

    print("\n===== POLIMORFISMO =====")

    for conta in contas:

        resultado = (
            conta.calcular_rendimento()
        )

        print(
            f"{conta.tipo_conta()} "
            f"{conta.numero}: "
            f"resultado mensal = "
            f"R$ {resultado:.2f}"
        )

    # A mesma chamada:
    #
    # conta.calcular_rendimento()
    #
    # produz comportamentos diferentes para
    # ContaCorrente e ContaPoupanca.

    # ==================================================
    # DEPÓSITO
    # ==================================================

    print("\n===== DEPÓSITO =====")

    conta_1.depositar(
        500
    )

    print(
        f"Novo saldo: "
        f"R$ {conta_1.saldo:.2f}"
    )

    # ==================================================
    # SAQUE
    # ==================================================

    print("\n===== SAQUE =====")

    try:

        conta_2.sacar(
            500
        )

        print(
            f"Novo saldo: "
            f"R$ {conta_2.saldo:.2f}"
        )

    except SaldoInsuficienteError as erro:

        print(
            f"Erro: {erro}"
        )

    # ==================================================
    # TRATAMENTO DE SALDO INSUFICIENTE
    # ==================================================

    print(
        "\n===== TESTE DE EXCEÇÃO: "
        "SALDO INSUFICIENTE ====="
    )

    try:

        conta_3.sacar(
            5000
        )

    except SaldoInsuficienteError as erro:

        print(
            f"Erro tratado: {erro}"
        )

    # ==================================================
    # TESTE DE E-MAIL INVÁLIDO
    # ==================================================

    print(
        "\n===== TESTE DE EXCEÇÃO: "
        "E-MAIL INVÁLIDO ====="
    )

    try:

        Cliente(
            "Cliente Inválido",
            "email-invalido"
        )

    except ValueError as erro:

        print(
            f"Erro tratado: {erro}"
        )

    # ==================================================
    # TESTE DE SALDO NEGATIVO
    # ==================================================

    print(
        "\n===== TESTE DE EXCEÇÃO: "
        "SALDO NEGATIVO ====="
    )

    try:

        ContaCorrente(
            "007",
            cliente_1,
            -100
        )

    except ValueError as erro:

        print(
            f"Erro tratado: {erro}"
        )

    # ==================================================
    # __EQ__
    # ==================================================

    print("\n===== MÉTODO __eq__ =====")

    print(
        f"conta_1 == conta_2? "
        f"{conta_1 == conta_2}"
    )

    # ==================================================
    # __REPR__
    # ==================================================

    print("\n===== MÉTODO __repr__ =====")

    print(
        repr(conta_1)
    )

    # ==================================================
    # __LT__ + SORTED
    # ==================================================

    print(
        "\n===== CONTAS ORDENADAS "
        "POR SALDO ====="
    )

    contas_ordenadas = sorted(
        contas
    )

    for conta in contas_ordenadas:

        print(
            f"Conta {conta.numero}: "
            f"R$ {conta.saldo:.2f}"
        )

    # ==================================================
    # RELATÓRIO FINAL
    # ==================================================

    print("\n===== RESUMO FINAL =====")

    print(
        f"Quantidade de clientes criados: 5"
    )

    print(
        f"Quantidade de contas criadas: "
        f"{len(contas)}"
    )

    print(
        f"Saldo total administrado: "
        f"R$ {banco.saldo_total():.2f}"
    )

    print("\n")
    print("=" * 65)
    print("FIM DA DEMONSTRAÇÃO")
    print("=" * 65)


# ======================================================
# EXECUÇÃO
# ======================================================


if __name__ == "__main__":
    demonstrar_sistema()
