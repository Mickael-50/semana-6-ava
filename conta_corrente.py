"""Módulo que define a classe ContaCorrente."""

from .cliente import Cliente
from .conta import Conta


class ContaCorrente(Conta):
    """Representa uma conta corrente com tarifa mensal e limite extra."""

    def __init__(
        self,
        numero: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        taxa_manutencao: float = 15.0,
    ) -> None:
        """Inicializa a conta corrente chamando o construtor da classe mãe."""
        super().__init__(numero=numero, titular=titular, saldo_inicial=saldo_inicial)
        self.taxa_manutencao = taxa_manutencao

    @property
    def taxa_manutencao(self) -> float:
        """Retorna a taxa de manutenção mensal."""
        return self._taxa_manutencao

    @taxa_manutencao.setter
    def taxa_manutencao(self, valor: float) -> None:
        """Valida que a taxa de manutenção não é negativa."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa de manutenção não pode ser negativa.")
        self._taxa_manutencao = float(valor)

    def processar_fechamento_mensal(self) -> str:
        """Desconta a tarifa mensal de manutenção da conta corrente."""
        if self.saldo >= self.taxa_manutencao:
            self.saldo -= self.taxa_manutencao
            msg = f"Tarifa de R$ {self.taxa_manutencao:.2f} descontada da conta {self.numero}."
        else:
            msg = f"Saldo insuficiente para cobrar tarifa na conta {self.numero}."
        self._historico.append(msg)
        return msg
