from conexao import client, db
import csv
import os

def executar():
    try:
        client.server_info()
        print("Conexão com o Localhost confirmada.")
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return
        
    colecao = db["livros"]
    nome_arquivo_csv = "exemplares-acervo.csv"
    
    if not os.path.exists(nome_arquivo_csv):
        print(f"\n[ERRO] O arquivo '{nome_arquivo_csv}' não foi encontrado!")
        return

    print("Limpando registros antigos do banco...")
    colecao.delete_many({})

    lista_livros = []
    
    print(f"Processando '{nome_arquivo_csv}' com separador ';' e codificação UTF-8...")
    
    with open(nome_arquivo_csv, mode='r', encoding='utf-8-sig') as arquivo:
        leitor_csv = csv.DictReader(arquivo, delimiter=';', skipinitialspace=True)
        
        for linha in leitor_csv:
            linha_limpa = {str(k).replace('"', '').strip().lower(): str(v).replace('"', '').strip() for k, v in linha.items() if k is not None}
            
            titulo = linha_limpa.get("titulo")
            autor = linha_limpa.get("autor")
            ano_bruto = linha_limpa.get("ano")
            editora = linha_limpa.get("editora")
            assunto = linha_limpa.get("assunto")
            sub_titulo = linha_limpa.get("sub_titulo")

            ano_final = 2020
            if ano_bruto:
                ano_limpo = str(ano_bruto).split('.')[0].strip()
                if ano_limpo.isdigit():
                    ano_final = int(ano_limpo)

            titulo_completo = titulo if titulo else "Título Desconhecido"
            if sub_titulo and sub_titulo.lower() != "null" and sub_titulo.strip() != "":
                titulo_completo = f"{titulo_completo} - {sub_titulo}"

            if titulo and titulo.lower() != "null":
                livro = {
                    "titulo": titulo_completo,
                    "autor": autor if (autor and autor.lower() != "null") else "Autor Não Informado",
                    "ano_publicacao": ano_final,
                    "editora": editora if (editora and editora.lower() != "null") else "Editora Não Informada",
                    "sinopse": assunto if (assunto and assunto.lower() != "null") else "Sem descrição disponível no acervo real."
                }
                lista_livros.append(livro)
            
            if len(lista_livros) >= 10000:
                break
                
    if lista_livros:
        print(f"Realizado, {len(lista_livros)} livros extraídos da planilha para o MongoDB.")
        colecao.insert_many(lista_livros)
        print("Dados carregados com sucesso!")
    else:
        print("Não foi possível extrair os dados. Verifique se o arquivo contém linhas preenchidas.")

if __name__ == "__main__":
    executar()
