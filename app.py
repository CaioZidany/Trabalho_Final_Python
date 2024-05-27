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


# Exemplo de rota para a página sobre
@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')


# Exemplo de rota para a página de glossário
@app.route('/cursos')
def cursos():

    curso_de_lista = []

    with open(
            'bd_cursos.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            curso_de_lista.append(l)

    return render_template('cursos.html',
                           cursos=gcurso_de_lista)


@app.route('/novo_curso')
def novo_termo():
    return render_template('adicionar_curso.html')


@app.route('/criar_curso', methods=['POST', ])
def criar_curso():
    termo = request.form['curso']
    definicao = request.form['definicao']

    with open(
            'bd_cursos.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([curso, definicao])

    return redirect(url_for('cursos'))


@app.route('/excluir_cursos/<int:termo_id>', methods=['POST'])
def excluir_cursos(termo_id):

    with open('bd_cursos.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_cursos.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('cursos'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)
