from flask_app.models.registro_login import Proyecto
from flask_bcrypt import Bcrypt   
from flask_app import app
bcrypt = Bcrypt(app) 
from flask_app import app
from flask import render_template,redirect,request,session,flash



@app.route('/main', methods=['GET'])
def inicio_sesion_registro():
    return render_template('register_login.html')

@app.route('/dashboard', methods=['GET'])
def ingresado_exitosamente():
    if 'id' not in session:
        return redirect('/main')
    data = {
        "id": session['id']
    }
    return render_template('music_dashboard.html')

@app.route('/listen')
def listen_music():
    return render_template('listen_download.html')

@app.route('/contribute')
def contributing():
    return render_template('contribute_music.html')

@app.route('/view_user')
def view_user():
    return render_template('view_user_music.html')


@app.route('/registrarse', methods=['POST'])
def registro():
    if request.method == 'POST':
        print(request.form, "/?/"*20)
        if not Proyecto.validar_registro(request.form):
            flash("Registro invalido")
            return redirect('/main')
        data = {
            "name" : request.form['name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : bcrypt.generate_password_hash(request.form['password']),
            "confirm_password" : request.form['confirm_password'],
            "date" : request.form['date']
        }
        print(data, "/*-"*20)
        usuario_id = Proyecto.save(data)
        print(data)
        session["id"] = usuario_id 
        return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        usuario = Proyecto.getEmail(request.form)
        if not usuario:
            flash("Este dato esta erroneo")
            return redirect("/main")
        if usuario == False or not bcrypt.check_password_hash(usuario.password, request.form['password']):
            flash("Contraseña erronea")
            return redirect("/main")
        session["id"] = usuario.id
        print(usuario)
        return redirect('/dashboard')

@app.route('/destroy')
def destroy():
    session.clear()
    return redirect('/main')

@app.route('/user/<int:id>', methods=['GET'])
def view(id):
    data = {
        "id": id
    }
    view_all = Proyecto.get_one(data)
    return render_template('view_user_music.html', view_all=view_all)