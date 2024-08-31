


from flask import Flask, render_template, redirect, request, flash
import json
import ast
import os
import mysql.connector

app = Flask(__name__)
app.config['LULUEFRAN'] = 'FRANCPAES'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        conectBD = mysql.connector.connect(host='localhost', database='usuarios', user = 'root', password = 'admin')
        
        if conectBD.is_connected():  
                print('conectado')
                cursur = conectBD.cursor()
                cursur.execute('select*from usuario;')
                usuarios = cursur.fetchall()

        return render_template("administrador.html",usuarios=usuarios)
    if logado == False:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user = 'root', password = 'admin')
    cont = 0
    if conectBD.is_connected():  
        print('conectado')
        cursur = conectBD.cursor()
        cursur.execute('select*from usuario;')
        
        usuariosBD = cursur.fetchall()
        
        for usuario in usuariosBD:
            cont += 1
            usuarioNome = str(usuario[1])
            usuarioSenha = str(usuario[2])
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')

            if usuarioNome == nome and usuarioSenha == senha:
                return render_template("usuarios.html")

            if cont >= len(usuariosBD):
                flash('USUARIO INVALIDO')
                return redirect("/")
    else: 
        return redirect('/')

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user = 'root', password = 'admin')
    if conectBD.is_connected():  
       
        cursur = conectBD.cursor()
        cursur.execute(f"insert into usuario values (default,'{nome}','{senha}');")

    if conectBD.is_connected():  
        cursur.close()
        conectBD.close()
  
    logado = True
    flash(F'{nome} CADASTRADO!!')
    return redirect('/adm')


@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    nome = request.form.get('nome')
    
    usuarioID = request.form.get('usuarioPexcluir')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user = 'root', password = 'admin')
    if conectBD.is_connected():  
       
        cursur = conectBD.cursor()
        cursur.execute(f" delete from usuario where id = '{usuarioID}'; ")

    if conectBD.is_connected():  
        cursur.close()
        conectBD.close()
    
    flash(F'{nome} EXCLUIDO')
    return redirect('/adm')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ","-")
    arquivo.save(os.path.join('../001/static/css/arquivos/', nome_arquivo))

    flash('Arquivo salvo')
    return redirect('/adm')





if __name__ in "__main__":
    app.run(debug=True)    