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

        return redirect(url_for('index'))
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

@app.route('/calculadora/imc', methods=['GET', 'POST'])
def calculadora_imc():
    resultado = None
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura']) / 100
        imc = peso / (altura ** 2)
        resultado = f"Tu IMC es {imc:.2f}"

    return render_template('calculadora_IMC.html', resultado=resultado)

@app.route('/calculadora/tmb', methods=['GET', 'POST'])
def calculadora_tmb():
    resultado = None
    if request.method == 'POST':
        edad = int(request.form['edad'])
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])

        if sexo == "hombre":
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = f"Tu TMB es {tmb:.2f} calorías/día"

    return render_template('calculadora_TMB.html', resultado=resultado)

@app.route('/calculadora/gct', methods=['GET', 'POST'])
def calculadora_gct():
    resultado = None
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        actividad = float(request.form['actividad'])
        gct = tmb * actividad
        resultado = f"Tu gasto calórico total es {gct:.2f} calorías/día"

    return render_template('calculadora_GCT.html', resultado=resultado)

@app.route('/calculadora/pesoideal', methods=['GET', 'POST'])
def calculadora_pesoideal():
    resultado = None
    if request.method == 'POST':
        altura = float(request.form['altura'])
        sexo = request.form['sexo']

        altura_m = altura / 2.54 

        if sexo == "hombre":
            ideal = 50 + 2.3 * (altura_m - 60)
        else:
            ideal = 45.5 + 2.3 * (altura_m - 60)

        resultado = f"Tu peso ideal aproximado es {ideal:.2f} kg"

    return render_template('calculadora_pesoideal.html', resultado=resultado)

@app.route('/calculadora/macronutrientes', methods=['GET', 'POST'])
def calculadora_macronutrientes():
    resultado = None

    if request.method == 'POST':
        calorias = float(request.form['calorias'])
        objetivo = request.form['objetivo']

        if objetivo == "perder":
            p, g, c = 0.40, 0.30, 0.30
        elif objetivo == "mantener":
            p, g, c = 0.30, 0.30, 0.40
        else:
            p, g, c = 0.30, 0.25, 0.45

        prot = calorias * p / 4
        gras = calorias * g / 9
        carb = calorias * c / 4

        resultado = f"Proteínas: {prot:.0f} g | Grasas: {gras:.0f} g | Carbohidratos: {carb:.0f} g"

    return render_template('calculadora_macronutrientes.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)