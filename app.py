from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = conectar()
    usuarios = conn.execute(
        "SELECT * FROM usuarios ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", usuarios=usuarios)


@app.route("/criar", methods=["POST"])
def criar():
    nome = request.form["nome"]
    email = request.form["email"]

    conn = conectar()
    conn.execute(
        "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
        (nome, email)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    nome = request.form["nome"]
    email = request.form["email"]

    conn = conectar()
    conn.execute(
        "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
        (nome, email, id)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/excluir/<int:id>")
def excluir(id):
    conn = conectar()
    conn.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
