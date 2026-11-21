"""Módulo que define a classe ContaPoupanca."""

from .cliente import Cliente
from .conta import Conta


class ContaPoupanca(Conta):
    """Representa uma conta poupança com rendimento mensal sobre o saldo."""

    def __init__(
        self,
        numero: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        taxa_rendimento: float = 0.005,
    ) -> None:
        """Inicializa a conta poupança chamando o construtor da classe mãe."""
        super().__init__(numero=numero, titular=titular, saldo_inicial=saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self) -> float:
        """Retorna a taxa percentual mensal de rendimento."""
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor: float) -> None:
        """Valida que a taxa de rendimento é positiva ou zero."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa de rendimento não pode ser negativa.")
        self._taxa_rendimento = float(valor)

    def processar_fechamento_mensal(self) -> str:
        """Aplica o rendimento mensal ao saldo da conta poupança."""
        rendimento = self.saldo * self.taxa_rendimento
        self.saldo += rendimento
        msg = f"Rendimento de +R$ {rendimento:.2f} creditado na poupança {self.numero}."
        self._historico.append(msg)
        return msg
