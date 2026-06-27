from conexao import db

livros_collection = db["livros"]


def garantir_indice_texto():
    indices_existentes = livros_collection.index_information()

    tem_indice_texto = any(
        any(tipo == "text" for _campo, tipo in detalhes.get("key", []))
        for detalhes in indices_existentes.values()
    )

    if not tem_indice_texto:
        print("Índice de texto não encontrado. Criando em titulo, autor e sinopse...")
        livros_collection.create_index(
            [("titulo", "text"), ("autor", "text"), ("sinopse", "text")],
            name="idx_busca_textual",
        )
        print("Índice de texto criado com sucesso.")


def executar():
    print("\nIniciando testes")

    # Teste 1: Ranges
    print("\nExecutando Busca por Intervalo:")
    query_range = {"ano": {"$gte": 2000, "$lte": 2010}}

    comando_range = {
        "explain": {
            "find": "livros",
            "filter": query_range
        },
        "verbosity": "executionStats"
    }

    resultado_range = db.command(comando_range)
    stats_range = resultado_range['executionStats']

    print(f"Tempo de execucao: {stats_range['executionTimeMillis']} ms")
    print(f"Documentos examinados: {stats_range['totalDocsExamined']}")
    print(f"Documentos retornados: {stats_range['nReturned']}")

    # Teste 2: Expressões Regulares
    print("\nExecutando Busca por Regex:")
    query_regex = {"titulo": {"$regex": "^O Mistério"}}

    comando_regex = {
        "explain": {
            "find": "livros",
            "filter": query_regex
        },
        "verbosity": "executionStats"
    }

    resultado_regex = db.command(comando_regex)
    stats_regex = resultado_regex['executionStats']

    print(f"Tempo de execucao: {stats_regex['executionTimeMillis']} ms")
    print(f"Documentos examinados: {stats_regex['totalDocsExamined']}")

    # Teste 3: Busca Textual
    print("\nExecutando Busca Textual:")
    garantir_indice_texto()

    query_texto = {"$text": {"$search": "aventura história"}}

    comando_texto = {
        "explain": {
            "find": "livros",
            "filter": query_texto
        },
        "verbosity": "executionStats"
    }

    resultado_texto = db.command(comando_texto)
    stats_texto = resultado_texto['executionStats']

    print(f"Tempo de execucao: {stats_texto['executionTimeMillis']} ms")
    print(f"Documentos examinados: {stats_texto['totalDocsExamined']}")


if __name__ == "__main__":
    executar()
