from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "nutriapp2025"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrado', methods=['GET', 'POST'])
def registrado():
    if request.method == 'POST':
        session['nombre'] = request.form['nombre']
        session['apellidos'] = request.form['apellidos']
        session['edad'] = request.form['edad']
        session['sexo'] = request.form['sexo']
        session['peso'] = request.form['peso']
        session['altura'] = request.form['altura']
        session['actividad'] = request.form['actividad']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        session['objetivo'] = request.form['objetivo']
        session['alergias'] = request.form['alergias']
        session['intolerancias'] = request.form['intolerancias']
        session['dieta'] = request.form['dieta']
        session['no_gusta'] = request.form['no_gusta']
        session['experiencia'] = request.form['experiencia']

        return redirect(url_for('perfil'))
    return render_template('registrado.html')

@app.route('/perfil')
def perfil():
    if 'nombre' in session:
        return render_template('perfil.html')
    else:
        return redirect(url_for('registrado'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/datos-nutricionales')
def datos_nutricionales():
    return render_template('datos_nutricionales.html')

if __name__ == '__main__':
    app.run(debug=True)