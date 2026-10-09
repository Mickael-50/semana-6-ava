"""Demonstração do sistema de biblioteca."""
from datetime import date

from biblioteca import (DVD, Biblioteca, ItemAcervo, ItemIndisponivelError, Livro,
                        Revista, Usuario, UsuarioNaoCadastradoError)


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def main() -> None:
    titulo("1. Criando objetos (10+ instâncias)")
    livros = [
        Livro("Dom Casmurro", 1899, "Machado de Assis", 256, exemplares=2),
        Livro("Grande Sertão: Veredas", 1956, "Guimarães Rosa", 624),
        Livro("Clean Code", 2008, "Robert C. Martin", 464),
    ]
    revistas = [Revista("Superinteressante", 2024, 450), Revista("Nature Brasil", 2023, 12)]
    dvds = [DVD("Cidade de Deus", 2002, 130), DVD("O Auto da Compadecida", 2000, 104)]
    ana = Usuario("Ana Souza", "ana@email.com")
    bruno = Usuario("Bruno Lima", "Bruno.Lima@Email.com")
    biblioteca = Biblioteca("Biblioteca Central", itens=[*livros, *revistas])
    for dvd in dvds:
        biblioteca.adicionar_item(dvd)
    biblioteca.cadastrar_usuario(ana)
    biblioteca.cadastrar_usuario(bruno)
    print(biblioteca)
    print(repr(livros[0]))

    titulo("2. Polimorfismo: mesma chamada, comportamentos diferentes")
    acervo: list[ItemAcervo] = [livros[0], revistas[0], dvds[0]]
    for item in acervo:
        print(f"{item.tipo:8} prazo={item.prazo_emprestimo_dias:2}d | "
              f"multa 5 dias=R$ {item.calcular_multa(5):6.2f} | "
              f"multa 20 dias=R$ {item.calcular_multa(20):6.2f}")

    titulo("3. Empréstimos e devolução com atraso")
    e1 = biblioteca.emprestar(ana, livros[0], date(2026, 9, 1))
    e2 = biblioteca.emprestar(bruno, dvds[0], date(2026, 9, 1))
    print(e1)
    print(e2)
    print(f"Multa Ana (devolveu 10 dias após o prazo): R$ {biblioteca.devolver(e1, date(2026, 9, 25)):.2f}")
    print(f"Multa Bruno (devolveu 20 dias após o prazo): R$ {biblioteca.devolver(e2, date(2026, 9, 24)):.2f}")

    titulo("4. Dunder methods: ordenação, igualdade, busca")
    for item in sorted(biblioteca):
        print(" -", item)
    print("Dois 'Clean Code' são iguais?", Livro("Clean Code", 2008, "Outro", 10) == livros[2])
    print("Busca por 'cl':", biblioteca.buscar_por_titulo("cl"))
    print("Usuários ordenados:", sorted([bruno, ana]))

    titulo("5. Tratamento de exceções (entradas inválidas)")
    testes = {
        "E-mail inválido": lambda: Usuario("Carlos", "carlos@"),
        "Ano futuro": lambda: Livro("Futuro", 2999, "X", 100),
        "Páginas negativas": lambda: Livro("Ruim", 2000, "X", -5),
        "Título vazio": lambda: Revista("   ", 2020, 1),
        "Tipo errado em duração": lambda: DVD("Filme", 2020, "longo"),
        "Instanciar classe abstrata": lambda: ItemAcervo("X", 2000),
        "Disponíveis acima do total": lambda: setattr(livros[1], "exemplares_disponiveis", 99),
        "Multa com dias negativos": lambda: dvds[1].calcular_multa(-1),
        "Usuário não cadastrado": lambda: biblioteca.emprestar(Usuario("Dani", "dani@email.com"), livros[1]),
        "Devolver duas vezes": lambda: biblioteca.devolver(e1),
    }
    for descricao, acao in testes.items():
        try:
            acao()
            print(f"[FALHOU] {descricao}: deveria ter lançado exceção")
        except (ValueError, TypeError, ItemIndisponivelError, UsuarioNaoCadastradoError) as erro:
            print(f"[OK] {descricao}: {type(erro).__name__} - {erro}")

    titulo("6. Item sem exemplares")
    biblioteca.emprestar(ana, livros[1])
    try:
        biblioteca.emprestar(bruno, livros[1])
    except ItemIndisponivelError as erro:
        print("[OK]", erro)
    print(biblioteca)


if __name__ == "__main__":
    main()
