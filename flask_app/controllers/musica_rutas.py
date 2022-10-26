import os
from fileinput import filename
from flask_app.models.registro_login import Proyecto
from flask_app.models.datos_musica import Musica
from flask_bcrypt import Bcrypt   
from flask_app import app
bcrypt = Bcrypt(app) 
from flask_app import app
from werkzeug.utils import secure_filename
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
    Usuario_all = Proyecto.get_one(data)
    return render_template('music_dashboard.html', Usuario_all=Usuario_all)

@app.route('/listen', methods=['POST', 'GET'])
def listen_music():
    if 'id' not in session:
        return redirect('/main')
    toda_music_data = Musica.get_all()
    if request.method == 'POST':
        f = request.files['music']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
            "name_music":{filename},
            "music": f"{filename}",
            "registro_login_join": session['id']
        }
        guardar_track = Musica.save(data)
        return redirect('/listen')
    # music_data = data['music']
    # data = {
    #     "name_music" : name_music_data,
    #     "music" : str(music_data)
    # }
    # llamar_musica = Musica.get_all(data)

    return render_template('listen_download.html', toda_music_data=toda_music_data)

@app.route('/contribute', methods=['POST' , 'GET'] )
def contributing():
    if request.method == 'POST':
        # data = {
        #     "music": str(music)
        # }
        music_data = Musica.save(request.form)
        return music_data
    return render_template('contribute_music.html')

@app.route('/view_user')
def view_user(id):
    data ={
        "id" : id
    }
    view_all = Proyecto.get_one(data)
    return redirect('/user/<int:id>')


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
            "mail" : request.form['mail'],
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
        print(request.form['mail'])
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
    musica_all = Musica.get_one(data)
    return render_template('view_user_music.html', view_all=view_all, musica_all=musica_all)