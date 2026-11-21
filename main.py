from models import (
    Cliente,
    ContaCorrente,
    ContaPoupanca,
    ContaInvestimento,
)


def executar_demonstracao() -> None:
    print("=== 1. CRIAÇÃO DE 10+ INSTÂNCIAS DE OBJETOS ===")
    c1 = Cliente("Mickael Fiquene", "MF@email.com", "11122233322")
    c2 = Cliente("Maria Silva", "maria@email.com", "22233344455")
    c3 = Cliente("João Oliveira", "joao@email.com", "33344455566")
    c4 = Cliente("Ana Costa", "ana@email.com", "44455566677")

    conta1 = ContaCorrente("CC-001", c1, saldo_inicial=1500.0, taxa_manutencao=20.0)
    conta2 = ContaCorrente("CC-002", c2, saldo_inicial=800.0, taxa_manutencao=15.0)
    conta3 = ContaPoupanca("CP-001", c1, saldo_inicial=3000.0, taxa_rendimento=0.006)
    conta4 = ContaPoupanca("CP-002", c3, saldo_inicial=1200.0, taxa_rendimento=0.005)
    conta5 = ContaInvestimento("CI-001", c4, saldo_inicial=5000.0, taxa_retorno=0.015)
    conta6 = ContaInvestimento("CI-002", c2, saldo_inicial=2500.0, taxa_retorno=0.012)

    clientes = [c1, c2, c3, c4]
    contas = [conta1, conta2, conta3, conta4, conta5, conta6]
    print(f"Total de instâncias criadas: {len(clientes)} clientes + {len(contas)} contas = {len(clientes) + len(contas)} objetos.\n")

    print("=== 2. OPERAÇÕES E DEMONSTRAÇÃO DE POLIMORFISMO ===")
    conta1.depositar(500.0)
    conta2.sacar(100.0)

    for conta in contas:
        resultado = conta.processar_fechamento_mensal()
        print(resultado)
        print(" ->", conta)

    print("\n=== 3. MÉTODOS ESPECIAIS (DUNDER METHODS) ===")
    print("repr(c1):", repr(c1))
    print("c1 == c2:", c1 == c2)
    print("Contas ordenadas por saldo (__lt__):")
    for conta_ord in sorted(contas):
        print(f"  {conta_ord.numero}: R$ {conta_ord.saldo:.2f}")

    print("\n=== 4. TRATAMENTO DE EXCEÇÕES (try/except) ===")
    try:
        Cliente("Erro Email", "email-invalido", "55566677788")
    except ValueError as erro:
        print(f"[Capturado] Validação de e-mail: {erro}")

    try:
        ContaCorrente("CC-999", c1, saldo_inicial=-200.0)
    except ValueError as erro:
        print(f"[Capturado] Validação de saldo negativo: {erro}")

    try:
        conta2.sacar(50000.0)
    except ValueError as erro:
        print(f"[Capturado] Saque acima do saldo: {erro}")

    try:
        conta3.taxa_rendimento = -0.05
    except ValueError as erro:
        print(f"[Capturado] Validação de taxa negativa: {erro}")


if __name__ == "__main__":
    executar_demonstracao()
