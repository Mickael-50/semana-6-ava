"""Classe Usuario."""
import re

_PADRAO_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Usuario:
    """Pessoa cadastrada que pode pegar itens emprestados."""

    def __init__(self, nome: str, email: str):
        self._nome = self._validar_nome(nome)
        self._email = self._validar_email(email)

    @staticmethod
    def _validar_nome(nome) -> str:
        if not isinstance(nome, str) or len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres.")
        return nome.strip()

    @staticmethod
    def _validar_email(email) -> str:
        if not isinstance(email, str) or not _PADRAO_EMAIL.match(email.strip()):
            raise ValueError(f"E-mail inválido: {email!r}")
        return email.strip().lower()

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = self._validar_nome(valor)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = self._validar_email(valor)

    def __str__(self) -> str:
        return f"{self.nome} <{self.email}>"

    def __repr__(self) -> str:
        return f"Usuario(nome={self.nome!r}, email={self.email!r})"

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Usuario):
            return NotImplemented
        return self.email == outro.email

    def __lt__(self, outro) -> bool:
        if not isinstance(outro, Usuario):
            return NotImplemented
        return self.nome.lower() < outro.nome.lower()

    def __hash__(self) -> int:
        return hash(self.email)
