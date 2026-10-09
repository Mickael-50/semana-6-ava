"""Exceções específicas do domínio da biblioteca."""


class BibliotecaError(Exception):
    """Erro base para regras de negócio da biblioteca."""


class ItemIndisponivelError(BibliotecaError):
    """Lançada quando não há exemplares disponíveis para empréstimo."""


class UsuarioNaoCadastradoError(BibliotecaError):
    """Lançada quando um usuário não cadastrado tenta realizar uma operação."""
