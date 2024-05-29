import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente para modo de desenvolvimento debug
os.environ['FLASK_DEBUG'] = 'True'
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def pagina_home():
    return render_template('index.html')

@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')

@app.route('/cursos')
def cursos():
    listar_curso = []
    try:
        with open('bd_cursos.csv', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for l in reader:
                listar_curso.append(l)
    except FileNotFoundError:
        listar_curso = []

    return render_template('cursos.html', listar_curso=listar_curso)

@app.route('/novo_curso')
def novo_curso():
    return render_template('adicionar_curso.html')

@app.route('/criar_curso', methods=['POST'])
def criar_curso():
    curso = request.form['curso']
    definicao = request.form['definicao']

    with open('bd_cursos.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([curso, definicao])

    return redirect(url_for('cursos'))

@app.route('/excluir_cursos/<int:curso_id>', methods=['POST'])
def excluir_cursos(curso_id):
    with open('bd_cursos.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    if 0 <= curso_id < len(linhas):
        del linhas[curso_id]

    with open('bd_cursos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)

    return redirect(url_for('cursos'))

@app.route('/agenda')
def agenda():
    eventos = []
    try:
        with open('bd_eventos.csv', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for l in reader:
                eventos.append(l)
    except FileNotFoundError:
        eventos = []

    return render_template('agenda.html', eventos=eventos)

@app.route('/novo_evento')
def novo_evento():
    return render_template('adicionar_evento.html')

@app.route('/criar_evento', methods=['POST'])
def criar_evento():
    data = request.form['data']
    descricao = request.form['descricao']
    tipo = request.form['tipo']

    with open('bd_eventos.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([data, descricao, tipo])

    return redirect(url_for('agenda'))

@app.route('/excluir_evento/<int:evento_id>', methods=['POST'])
def excluir_evento(evento_id):
    with open('bd_eventos.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    if 0 <= evento_id < len(linhas):
        del linhas[evento_id]

    with open('bd_eventos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)

    return redirect(url_for('agenda'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)
