"""Classe Biblioteca (agregadora do sistema)."""
from datetime import date

from .emprestimo import Emprestimo
from .excecoes import UsuarioNaoCadastradoError
from .item_acervo import ItemAcervo
from .usuario import Usuario


class Biblioteca:
    """Gerencia acervo, usuários e empréstimos."""

    def __init__(self, nome: str, itens: list[ItemAcervo] | None = None):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome da biblioteca não pode ser vazio.")
        self._nome = nome.strip()
        self._itens: list[ItemAcervo] = []  # criado aqui, nunca como default mutável
        self._usuarios: list[Usuario] = []
        self._emprestimos: list[Emprestimo] = []
        for item in itens or []:
            self.adicionar_item(item)

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def emprestimos_ativos(self) -> list[Emprestimo]:
        return [e for e in self._emprestimos if e.ativo]

    def adicionar_item(self, item: ItemAcervo) -> None:
        if not isinstance(item, ItemAcervo):
            raise TypeError("Somente ItemAcervo pode ser adicionado ao acervo.")
        if item in self._itens:
            raise ValueError(f"Item já cadastrado: {item.titulo}")
        self._itens.append(item)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        if not isinstance(usuario, Usuario):
            raise TypeError("Somente Usuario pode ser cadastrado.")
        if usuario in self._usuarios:
            raise ValueError(f"E-mail já cadastrado: {usuario.email}")
        self._usuarios.append(usuario)

    def buscar_por_titulo(self, trecho: str) -> list[ItemAcervo]:
        return sorted(i for i in self._itens if trecho.lower() in i.titulo.lower())

    def emprestar(self, usuario: Usuario, item: ItemAcervo, data: date | None = None) -> Emprestimo:
        if usuario not in self._usuarios:
            raise UsuarioNaoCadastradoError(f"{usuario.nome} não está cadastrado.")
        item.emprestar()  # pode lançar ItemIndisponivelError
        emprestimo = Emprestimo(usuario, item, data)
        self._emprestimos.append(emprestimo)
        return emprestimo

    def devolver(self, emprestimo: Emprestimo, data: date | None = None) -> float:
        """Registra a devolução e retorna a multa devida (R$)."""
        emprestimo.registrar_devolucao(data)
        emprestimo.item.devolver()
        return emprestimo.calcular_multa()

    def __len__(self) -> int:
        return len(self._itens)

    def __iter__(self):
        return iter(self._itens)

    def __str__(self) -> str:
        return (f"Biblioteca '{self.nome}': {len(self._itens)} itens, "
                f"{len(self._usuarios)} usuários, {len(self.emprestimos_ativos)} empréstimos ativos")

    def __repr__(self) -> str:
        return f"Biblioteca(nome={self.nome!r}, itens={len(self._itens)})"
