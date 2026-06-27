# bda-bibliotecavirtual

para validar a análise comparativa de desempenho das estruturas de indexação no sistema MongoDBpara o nosso artigo de pesquisa, desenvolvemos uma aplicação experimental utilizando a linguagem Python 3.14 e o driver PyMongo, utilizando o VScode.

a arquitetura da aplicação foi projetada de forma modular, dividindo a conexão, persistência, indexação e busca em arquivos distintos.

a massa de dados utilizada provém de um acervo governamental real de bibliotecas (exemplares-acervo.csv), contendo registros detalhados de publicações.

# TUTORIAL

No MongoDB Compass adicione a conexão "mongodb://localhost:27017", crie um database com o nome "biblioteca_virtual" com o nome de coleção "livros". Dentro de livros, importe o arquivo "exemplares-acervos.txt".

Abra a pasta bda-bibliotecavirtual-front no vscode e instale os requisitos "pip install -r requirements.txt" pelo terminal. No terminal rode o app.py "python app.py" (ou "py app.py").

Abra "http://127.0.0.1:5000/".
