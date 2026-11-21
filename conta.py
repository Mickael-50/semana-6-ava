"""Módulo que define a classe abstrata Conta."""

from abc import ABC, abstractmethod
from typing import List, Optional
from .cliente import Cliente


class Conta(ABC):
    """Classe abstrata base para todos os tipos de conta bancária."""

    def __init__(
        self,
        numero: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        historico: Optional[List[str]] = None,
    ) -> None:
        """Inicializa uma conta validando número, titular e saldo inicial."""
        self.numero = numero
        self.titular = titular
        self.saldo = saldo_inicial
        self._historico: List[str] = list(historico) if historico is not None else []
        self._historico.append(f"Conta aberta com saldo inicial de R$ {self.saldo:.2f}")

    @property
    def numero(self) -> str:
        """Retorna o número identificador da conta."""
        return self._numero

    @numero.setter
    def numero(self, valor: str) -> None:
        """Valida que o número da conta não está vazio."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O número da conta não pode ser vazio.")
        self._numero = valor.strip()

    @property
    def titular(self) -> Cliente:
        """Retorna o objeto Cliente titular da conta."""
        return self._titular

    @titular.setter
    def titular(self, valor: Cliente) -> None:
        """Garante que o titular é uma instância válida de Cliente."""
        if not isinstance(valor, Cliente):
            raise TypeError("O titular deve ser uma instância da classe Cliente.")
        self._titular = valor

    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        """Impede que o saldo assuma valor negativo diretamente."""
        if not isinstance(valor, (int, float)):
            raise TypeError("O saldo deve ser um valor numérico.")
        if valor < 0:
            raise ValueError("O saldo não pode ser negativo.")
        self._saldo = float(valor)

    @property
    def historico(self) -> List[str]:
        """Retorna uma cópia do histórico de movimentações."""
        return list(self._historico)

    def depositar(self, valor: float) -> None:
        """Realiza um depósito positivo na conta."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self.saldo += float(valor)
        self._historico.append(f"Depósito: +R$ {valor:.2f}")

    def sacar(self, valor: float) -> None:
        """Realiza um saque respeitando o saldo disponível."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self.saldo:
            raise ValueError(f"Saldo insuficiente na conta {self.numero}.")
        self.saldo -= float(valor)
        self._historico.append(f"Saque: -R$ {valor:.2f}")

    @abstractmethod
    def processar_fechamento_mensal(self) -> str:
        """Executa a regra mensal específica de cada tipo de conta."""

    def __str__(self) -> str:
        """Retorna representação amigável da conta."""
        return (
            f"[{self.__class__.__name__}] Nº {self.numero} | "
            f"Titular: {self.titular.nome} | Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self) -> str:
        """Retorna representação técnica da conta."""
        return (
            f"{self.__class__.__name__}(numero={self.numero!r}, "
            f"titular={self.titular!r}, saldo_inicial={self.saldo!r})"
        )

    def __eq__(self, outro: object) -> bool:
        """Compara duas contas pelo número."""
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.numero == outro.numero

    def __lt__(self, outro: object) -> bool:
        """Permite ordenar contas pelo saldo atual."""
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.saldo < outro.saldo
