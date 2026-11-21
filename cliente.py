"""Módulo que define a classe Cliente."""


class Cliente:
    """Representa um cliente titular de contas bancárias."""

    def __init__(self, nome: str, email: str, cpf: str) -> None:
        """Inicializa um cliente validando nome, e-mail e CPF."""
        self.nome = nome
        self.email = email
        self.cpf = cpf

    @property
    def nome(self) -> str:
        """Retorna o nome completo do cliente."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        """Valida e define o nome do cliente."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValueError("O nome do cliente deve ter pelo menos 3 caracteres.")
        self._nome = valor.strip()

    @property
    def email(self) -> str:
        """Retorna o e-mail do cliente."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Valida o formato básico do e-mail e define o atributo."""
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError(f"E-mail inválido: '{valor}'. Informe um e-mail válido.")
        self._email = valor.strip().lower()

    @property
    def cpf(self) -> str:
        """Retorna o CPF do cliente."""
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        """Valida que o CPF possui 11 dígitos numéricos."""
        digitos = "".join(ch for ch in str(valor) if ch.isdigit())
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        self._cpf = digitos

    def __str__(self) -> str:
        """Retorna representação amigável do cliente."""
        return f"Cliente: {self.nome} ({self.email})"

    def __repr__(self) -> str:
        """Retorna representação técnica do cliente."""
        return f"Cliente(nome={self.nome!r}, email={self.email!r}, cpf={self.cpf!r})"

    def __eq__(self, outro: object) -> bool:
        """Compara dois clientes pelo CPF."""
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self.cpf == outro.cpf
