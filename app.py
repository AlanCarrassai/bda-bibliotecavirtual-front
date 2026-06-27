from flask import Flask, render_template, request
from conexao import db
import re

app = Flask(__name__)
livros_collection = db["livros"]


def build_filter(args):
    filtro = {}

    titulo = args.get("titulo", "").strip()
    autor = args.get("autor", "").strip()
    editora = args.get("editora", "").strip()
    ano = args.get("ano", "").strip()
    assunto = args.get("assunto", "").strip()

    if titulo:
        filtro["titulo"] = {"$regex": re.compile(re.escape(titulo), re.IGNORECASE)}

    if autor:
        filtro["autor"] = {"$regex": re.compile(re.escape(autor), re.IGNORECASE)}

    if editora:
        filtro["editora"] = {"$regex": re.compile(re.escape(editora), re.IGNORECASE)}

    if ano:
        if ano.isdigit():
            filtro["ano"] = int(ano)

    if assunto:
        filtro["assunto"] = {"$regex": re.compile(re.escape(assunto), re.IGNORECASE)}

    return filtro


@app.route("/", methods=["GET"])
def index():
    filtro = build_filter(request.args)
    has_query = any(value.strip() for value in request.args.values())
    limite = 100 if not has_query else 200

    livros_cursor = livros_collection.find(filtro).sort("titulo", 1).limit(limite)
    livros = list(livros_cursor)
    total = livros_collection.count_documents(filtro)

    return render_template(
        "index.html",
        livros=livros,
        total=total,
        limite=limite,
        params=request.args,
        has_query=has_query,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
