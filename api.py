from flask import Flask, request, jsonify
import mysql.connector
from uuid import uuid4


app = Flask(__name__)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password = '',
    database='database_usuarios'
)


@app.route('/',methods=['GET'])
def obter_usuarios():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM usuarios')
    usuarios = my_cursor.fetchall()

    usuario_list = list()

    for usuario in usuarios:
        usuario_list.append({
            'id':usuario[0],
            'nome':usuario[1],
            'e-mail':usuario[2],
            'senha':usuario[3],
            'idade': usuario[4],
            'Data_de_nascimento': usuario[5]
        })
    return jsonify({
        'Usuarios': usuario_list
    })


@app.route('/<id>', methods=['GET'])
def obter_usuario_por_id(id):

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM usuarios')
    usuarios = my_cursor.fetchall()

    usuario_list = list()

    for usuario in usuarios:
        usuario_list.append({
            'id':usuario[0],
            'nome':usuario[1],
            'email':usuario[2],
            'senha':usuario[3],
            'idade': usuario[4],
            'data_nascimento': usuario[5]
        })
    
    for UsuarioId in usuario_list:
        if UsuarioId.get('id') == id:
            return(UsuarioId)
        
@app.route('/criar', methods=['POST'])
def criar_usuario():

    usuario = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO usuarios (id,nome,email,senha,idade,data_nascimento) VALUES ( '{uuid4()}','{usuario['nome']}','{usuario['email']}','{usuario['senha']}',{usuario['idade']}, '{usuario['data_nascimento']}')"

    my_cursor.execute(sql)

    mydb.commit()

    return jsonify(usuario)

# UPDATE
@app.route('/u/<id>', methods=['PUT'])
def editar_perfil(id):
    usuario_alterado = request.get_json() 

    my_cursor = mydb.cursor()

    sql = f"UPDATE usuarios SET nome = '{usuario_alterado['nome']}', email = '{usuario_alterado['email']}', senha = '{usuario_alterado['senha']}', idade = '{usuario_alterado['idade']}', data_nascimento = '{usuario_alterado['data_nascimento']}' WHERE id = '{id}' "
    
    my_cursor.execute(sql)

    mydb.commit()

    return jsonify(usuario_alterado)

# DELETE

@app.route('/d/<id>', methods = ['DELETE'])
def deletar_usuario(id):

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM usuarios WHERE id = '{id}' "

    my_cursor.execute(sql)

    mydb.commit()

    return jsonify('Usuario removido com sucesso! ')

app.run(port=5000,host='localhost',debug=True)