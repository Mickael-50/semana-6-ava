"""Classe Emprestimo (composição: tem um Usuario e tem um ItemAcervo)."""
from datetime import date, timedelta

from .item_acervo import ItemAcervo
from .usuario import Usuario


class Emprestimo:
    """Registro de um item emprestado a um usuário."""

    def __init__(self, usuario: Usuario, item: ItemAcervo, data_emprestimo: date | None = None):
        if not isinstance(usuario, Usuario):
            raise TypeError("usuario deve ser uma instância de Usuario.")
        if not isinstance(item, ItemAcervo):
            raise TypeError("item deve ser uma instância de ItemAcervo.")
        self._usuario = usuario
        self._item = item
        self._data_emprestimo = data_emprestimo or date.today()
        self._data_devolucao: date | None = None

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def item(self) -> ItemAcervo:
        return self._item

    @property
    def data_emprestimo(self) -> date:
        return self._data_emprestimo

    @property
    def data_devolucao(self) -> date | None:
        return self._data_devolucao

    @property
    def data_prevista(self) -> date:
        # Polimorfismo: cada tipo de item define seu prazo.
        return self._data_emprestimo + timedelta(days=self._item.prazo_emprestimo_dias)

    @property
    def ativo(self) -> bool:
        return self._data_devolucao is None

    def dias_atraso(self, referencia: date | None = None) -> int:
        fim = self._data_devolucao or referencia or date.today()
        return max(0, (fim - self.data_prevista).days)

    def calcular_multa(self, referencia: date | None = None) -> float:
        return self._item.calcular_multa(self.dias_atraso(referencia))

    def registrar_devolucao(self, data: date | None = None) -> None:
        if not self.ativo:
            raise ValueError("Este empréstimo já foi devolvido.")
        data = data or date.today()
        if data < self._data_emprestimo:
            raise ValueError("Data de devolução anterior à data do empréstimo.")
        self._data_devolucao = data

    def __str__(self) -> str:
        situacao = "ativo" if self.ativo else f"devolvido em {self._data_devolucao:%d/%m/%Y}"
        return (f"{self._usuario.nome} -> '{self._item.titulo}' | "
                f"retirada {self._data_emprestimo:%d/%m/%Y}, prevista {self.data_prevista:%d/%m/%Y} ({situacao})")

    def __repr__(self) -> str:
        return (f"Emprestimo(usuario={self._usuario!r}, item={self._item!r}, "
                f"data_emprestimo={self._data_emprestimo!r})")
