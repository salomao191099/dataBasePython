import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

# Verificar se o banco de dados já existe
nome_banco = 'database.db'

if not os.path.exists(nome_banco):
    # Se não existir, criar o banco de dados
    conexao_temporaria = sqlite3.connect(nome_banco)
    conexao_temporaria.close()

# Conectar ao banco de dados
banco = sqlite3.connect(nome_banco, check_same_thread=False)
cursor = banco.cursor()


# Criação da tabela se não existir
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS formulario (nome TEXT)")
banco.commit()

# Rota para receber dados do formulário
@app.route('/receber-dados', methods=['GET'])
def receber_dados():
    nome = request.args.get('nome')

    if nome:
        # Apagar dados
        cursor.execute("DELETE FROM formulario")
        banco.commit()
        # Insere os dados no banco de dados
        cursor.execute("INSERT INTO formulario (nome) VALUES (?)", (nome,))
        banco.commit()
        # Visualização dos dados da tabela
        cursor.execute("SELECT * FROM formulario")
        print(cursor.fetchall())
        return 'Dados recebidos com sucesso'
    else:
        return 'Por favor, insira um nome antes de enviar.', 400

# Rota para obter todos os dados da tabela
@app.route('/obter-dados', methods=['GET'])
def obter_dados():
    cursor.execute("SELECT * FROM formulario")
    dados = cursor.fetchall()
    return jsonify(dados)

# Rota para obter a última informação do banco de dados
@app.route('/obter-ultima-informacao', methods=['GET'])
def obter_ultima_informacao():
    cursor.execute("SELECT * FROM formulario ORDER BY ROWID DESC LIMIT 1")
    ultima_informacao = cursor.fetchone()
    return jsonify(ultima_informacao)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
