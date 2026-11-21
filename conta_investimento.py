"""Módulo que define a classe ContaInvestimento."""

from .cliente import Cliente
from .conta import Conta


class ContaInvestimento(Conta):
    """Representa uma conta de investimento com rentabilidade e taxa de administração."""

    def __init__(
        self,
        numero: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        taxa_retorno: float = 0.012,
        taxa_administracao: float = 0.002,
    ) -> None:
        """Inicializa a conta de investimento chamando o construtor da classe mãe."""
        super().__init__(numero=numero, titular=titular, saldo_inicial=saldo_inicial)
        self.taxa_retorno = taxa_retorno
        self.taxa_administracao = taxa_administracao

    @property
    def taxa_retorno(self) -> float:
        """Retorna a taxa de retorno mensal."""
        return self._taxa_retorno

    @taxa_retorno.setter
    def taxa_retorno(self, valor: float) -> None:
        """Valida que a taxa de retorno não é negativa."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa de retorno não pode ser negativa.")
        self._taxa_retorno = float(valor)

    @property
    def taxa_administracao(self) -> float:
        """Retorna a taxa de administração mensal."""
        return self._taxa_administracao

    @taxa_administracao.setter
    def taxa_administracao(self, valor: float) -> None:
        """Valida que a taxa de administração não é negativa."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa de administração não pode ser negativa.")
        self._taxa_administracao = float(valor)

    def processar_fechamento_mensal(self) -> str:
        """Calcula o ganho líquido (retorno menos taxa de administração)."""
        ganho_bruto = self.saldo * self.taxa_retorno
        custo_adm = self.saldo * self.taxa_administracao
        liquido = ganho_bruto - custo_adm
        if self.saldo + liquido < 0:
            raise ValueError("Operação resultaria em saldo negativo.")
        self.saldo += liquido
        msg = f"Lucro líquido de R$ {liquido:.2f} aplicado no investimento {self.numero}."
        self._historico.append(msg)
        return msg
