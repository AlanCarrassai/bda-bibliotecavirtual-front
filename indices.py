from conexao import db

def executar():
    livros_collection = db["livros"] 
    
    print("\nCriando índices no MongoDB")
    
    print("Criando índice B-tree para 'ano_publicacao'...")
    livros_collection.create_index([("ano_publicacao", 1)])
    
    print("Criando índice de Texto para 'sinopse'...")
    livros_collection.create_index([("sinopse", "text")])
    
    print("Todos os índices foram criados com sucesso!")

if __name__ == "__main__":
    executar()
