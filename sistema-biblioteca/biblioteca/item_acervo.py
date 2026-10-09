"""Classe abstrata ItemAcervo e suas especializações (Livro, Revista, DVD)."""
from abc import ABC, abstractmethod
from datetime import date

from .excecoes import ItemIndisponivelError


class ItemAcervo(ABC):
    """Contrato comum a qualquer item emprestável do acervo.

    Subclasses DEVEM implementar `prazo_emprestimo_dias` e `calcular_multa`.
    """

    ANO_MINIMO = 1450  # invenção da prensa de tipos móveis

    def __init__(self, titulo: str, ano_publicacao: int, exemplares: int = 1):
        self._titulo = self._validar_titulo(titulo)
        self._ano_publicacao = self._validar_ano(ano_publicacao)
        self._exemplares_total = self._validar_inteiro_positivo(exemplares, "exemplares")
        self._exemplares_disponiveis = self._exemplares_total

    # ---------- validações reutilizáveis ----------
    @staticmethod
    def _validar_texto(valor, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} deve ser um texto não vazio.")
        return valor.strip()

    @classmethod
    def _validar_titulo(cls, titulo) -> str:
        return cls._validar_texto(titulo, "Título")

    @classmethod
    def _validar_ano(cls, ano) -> int:
        if not isinstance(ano, int) or isinstance(ano, bool):
            raise TypeError("Ano de publicação deve ser um inteiro.")
        if not cls.ANO_MINIMO <= ano <= date.today().year:
            raise ValueError(
                f"Ano de publicação deve estar entre {cls.ANO_MINIMO} e {date.today().year}."
            )
        return ano

    @staticmethod
    def _validar_inteiro_positivo(valor, campo: str) -> int:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(f"{campo} deve ser um inteiro.")
        if valor <= 0:
            raise ValueError(f"{campo} deve ser maior que zero.")
        return valor

    @staticmethod
    def _validar_dias(dias) -> int:
        if not isinstance(dias, int) or isinstance(dias, bool):
            raise TypeError("Dias de atraso deve ser um inteiro.")
        if dias < 0:
            raise ValueError("Dias de atraso não pode ser negativo.")
        return dias

    # ---------- propriedades (encapsulamento) ----------
    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = self._validar_titulo(valor)

    @property
    def ano_publicacao(self) -> int:
        return self._ano_publicacao

    @ano_publicacao.setter
    def ano_publicacao(self, valor: int) -> None:
        self._ano_publicacao = self._validar_ano(valor)

    @property
    def exemplares_total(self) -> int:
        """Somente leitura: o total de exemplares é definido na criação."""
        return self._exemplares_total

    @property
    def exemplares_disponiveis(self) -> int:
        return self._exemplares_disponiveis

    @exemplares_disponiveis.setter
    def exemplares_disponiveis(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("Exemplares disponíveis deve ser um inteiro.")
        if not 0 <= valor <= self._exemplares_total:
            raise ValueError(
                f"Exemplares disponíveis deve estar entre 0 e {self._exemplares_total}."
            )
        self._exemplares_disponiveis = valor

    @property
    def tipo(self) -> str:
        return type(self).__name__

    # ---------- contrato abstrato (polimorfismo) ----------
    @property
    @abstractmethod
    def prazo_emprestimo_dias(self) -> int:
        """Quantidade de dias de empréstimo para este tipo de item."""

    @abstractmethod
    def calcular_multa(self, dias_atraso: int) -> float:
        """Valor da multa (R$) para a quantidade de dias de atraso."""

    # ---------- comportamentos comuns ----------
    def emprestar(self) -> None:
        if self._exemplares_disponiveis == 0:
            raise ItemIndisponivelError(f"Sem exemplares disponíveis de '{self.titulo}'.")
        self.exemplares_disponiveis = self._exemplares_disponiveis - 1

    def devolver(self) -> None:
        self.exemplares_disponiveis = self._exemplares_disponiveis + 1

    # ---------- métodos especiais ----------
    def __str__(self) -> str:
        return (f"{self.tipo}: '{self.titulo}' ({self.ano_publicacao}) - "
                f"{self.exemplares_disponiveis}/{self.exemplares_total} disponíveis")

    def __repr__(self) -> str:
        return (f"{self.tipo}(titulo={self.titulo!r}, ano_publicacao={self.ano_publicacao!r}, "
                f"exemplares={self.exemplares_total!r})")

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, ItemAcervo) or type(self) is not type(outro):
            return NotImplemented
        return (self.titulo.lower(), self.ano_publicacao) == (outro.titulo.lower(), outro.ano_publicacao)

    def __lt__(self, outro) -> bool:
        if not isinstance(outro, ItemAcervo):
            return NotImplemented
        return self.titulo.lower() < outro.titulo.lower()

    def __hash__(self) -> int:
        return hash((self.tipo, self.titulo.lower(), self.ano_publicacao))


class Livro(ItemAcervo):
    """Livro: 14 dias de prazo e multa de R$ 1,00 por dia."""

    MULTA_DIARIA = 1.00

    def __init__(self, titulo: str, ano_publicacao: int, autor: str, paginas: int, exemplares: int = 1):
        super().__init__(titulo, ano_publicacao, exemplares)
        self._autor = self._validar_texto(autor, "Autor")
        self._paginas = self._validar_inteiro_positivo(paginas, "Páginas")

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = self._validar_texto(valor, "Autor")

    @property
    def paginas(self) -> int:
        return self._paginas

    @paginas.setter
    def paginas(self, valor: int) -> None:
        self._paginas = self._validar_inteiro_positivo(valor, "Páginas")

    @property
    def prazo_emprestimo_dias(self) -> int:
        return 14

    def calcular_multa(self, dias_atraso: int) -> float:
        return self._validar_dias(dias_atraso) * self.MULTA_DIARIA

    def __str__(self) -> str:
        return f"{super().__str__()} | Autor: {self.autor}, {self.paginas} páginas"

    def __repr__(self) -> str:
        return (f"Livro(titulo={self.titulo!r}, ano_publicacao={self.ano_publicacao!r}, "
                f"autor={self.autor!r}, paginas={self.paginas!r}, exemplares={self.exemplares_total!r})")


class Revista(ItemAcervo):
    """Revista: 7 dias de prazo e multa de R$ 0,50 por dia."""

    MULTA_DIARIA = 0.50

    def __init__(self, titulo: str, ano_publicacao: int, edicao: int, exemplares: int = 1):
        super().__init__(titulo, ano_publicacao, exemplares)
        self._edicao = self._validar_inteiro_positivo(edicao, "Edição")

    @property
    def edicao(self) -> int:
        return self._edicao

    @edicao.setter
    def edicao(self, valor: int) -> None:
        self._edicao = self._validar_inteiro_positivo(valor, "Edição")

    @property
    def prazo_emprestimo_dias(self) -> int:
        return 7

    def calcular_multa(self, dias_atraso: int) -> float:
        return self._validar_dias(dias_atraso) * self.MULTA_DIARIA

    def __str__(self) -> str:
        return f"{super().__str__()} | Edição nº {self.edicao}"

    def __repr__(self) -> str:
        return (f"Revista(titulo={self.titulo!r}, ano_publicacao={self.ano_publicacao!r}, "
                f"edicao={self.edicao!r}, exemplares={self.exemplares_total!r})")


class DVD(ItemAcervo):
    """DVD: 3 dias de prazo, multa de R$ 3,00 por dia limitada a R$ 30,00."""

    MULTA_DIARIA = 3.00
    MULTA_MAXIMA = 30.00

    def __init__(self, titulo: str, ano_publicacao: int, duracao_minutos: int, exemplares: int = 1):
        super().__init__(titulo, ano_publicacao, exemplares)
        self._duracao_minutos = self._validar_inteiro_positivo(duracao_minutos, "Duração")

    @property
    def duracao_minutos(self) -> int:
        return self._duracao_minutos

    @duracao_minutos.setter
    def duracao_minutos(self, valor: int) -> None:
        self._duracao_minutos = self._validar_inteiro_positivo(valor, "Duração")

    @property
    def prazo_emprestimo_dias(self) -> int:
        return 3

    def calcular_multa(self, dias_atraso: int) -> float:
        return min(self._validar_dias(dias_atraso) * self.MULTA_DIARIA, self.MULTA_MAXIMA)

    def __str__(self) -> str:
        return f"{super().__str__()} | {self.duracao_minutos} min"

    def __repr__(self) -> str:
        return (f"DVD(titulo={self.titulo!r}, ano_publicacao={self.ano_publicacao!r}, "
                f"duracao_minutos={self.duracao_minutos!r}, exemplares={self.exemplares_total!r})")
