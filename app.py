from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import requests

app = Flask(__name__)
app.secret_key = "nutriapp2025"

API_KEY = "GtT9BVfZt3IAs6emnD24WO6ITAE7gzi4Grxq8VvO"

def buscar_alimento(api_key, nombre):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"api_key": api_key, "query": nombre, "pageSize": 1}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    data = r.json()
    if "foods" not in data or len(data["foods"]) == 0:
        return None
    food = data["foods"][0]
    nutrients = {n["nutrientName"]: n["value"] for n in food["foodNutrients"]}
    return {
        "proteins": nutrients.get("Protein", 0),
        "carbs": nutrients.get("Carbohydrate, by difference", 0),
        "fats": nutrients.get("Total lipid (fat)", 0)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrado', methods=['GET', 'POST'])
def registrado():
    if request.method == 'POST':
        campos = [
            'nombre', 'apellidos', 'edad', 'sexo', 'peso', 'altura', 'actividad',
            'email', 'password', 'objetivo', 'alergias', 'intolerancias',
            'dieta', 'no_gusta', 'experiencia'
        ]
        for campo in campos:
            session[campo] = request.form.get(campo, "")
        return redirect(url_for('index'))
    return render_template('registrado.html')

@app.route('/perfil')
def perfil():
    if 'nombre' in session:
        return render_template('perfil.html')
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
    info = None

    if request.method == 'POST' and 'nombre' in session:
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura']) / 100
            imc = peso / (altura ** 2)
            resultado = f"Tu IMC es {imc:.2f}"

            if imc < 18.5:
                info = "Bajo peso: podrías necesitar aumentar masa muscular."
            elif 18.5 <= imc < 24.9:
                info = "Peso normal: ¡Excelente! Mantén tus buenos hábitos."
            elif 25 <= imc < 29.9:
                info = "Sobrepeso: podrías beneficiarte de una dieta equilibrada."
            else:
                info = "Obesidad: considera buscar apoyo nutricional."
        except:
            resultado = "Por favor llena todos los campos correctamente."

    return render_template('calculadora_IMC.html', resultado=resultado, info=info)

@app.route('/calculadora/tmb', methods=['GET', 'POST'])
def calculadora_tmb():
    resultado = None
    info = None

    if request.method == 'POST' and 'nombre' in session:
        try:
            edad = int(request.form['edad'])
            sexo = request.form['sexo']
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])

            if sexo == "hombre":
                tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
            else:
                tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

            resultado = f"Tu TMB es {tmb:.2f} calorías/día"
            info = "Este valor representa cuántas calorías quemas en reposo."
        except:
            resultado = "Completa correctamente todos los campos."

    return render_template('calculadora_TMB.html', resultado=resultado, info=info)

@app.route('/calculadora/gct', methods=['GET', 'POST'])
def calculadora_gct():
    resultado = None
    info = None

    if request.method == 'POST' and 'nombre' in session:
        try:
            tmb = float(request.form['tmb'])
            actividad = float(request.form['actividad'])
            gct = tmb * actividad
            resultado = f"Tu gasto calórico total es {gct:.2f} calorías/día"
            info = "Estas son las calorías que quemas en un día normal."
        except:
            resultado = "Completa los datos correctamente."

    return render_template('calculadora_GCT.html', resultado=resultado, info=info)

@app.route('/calculadora/pesoideal', methods=['GET', 'POST'])
def calculadora_pesoideal():
    resultado = None
    info = None

    if request.method == 'POST' and 'nombre' in session:
        try:
            altura = float(request.form['altura'])
            sexo = request.form['sexo']
            altura_m = altura / 2.54

            if sexo == "hombre":
                ideal = 50 + 2.3 * (altura_m - 60)
            else:
                ideal = 45.5 + 2.3 * (altura_m - 60)

            resultado = f"Tu peso ideal aproximado es {ideal:.2f} kg"
            info = "El peso ideal es solo una referencia, cada cuerpo es diferente."
        except:
            resultado = "Llena los campos correctamente."

    return render_template('calculadora_pesoideal.html', resultado=resultado, info=info)

@app.route('/calculadora/macronutrientes', methods=['GET', 'POST'])
def calculadora_macronutrientes():
    resultado = None
    info = None

    if request.method == 'POST' and 'nombre' in session:
        try:
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
            info = "Estos valores son ideales según tu objetivo."
        except:
            resultado = "Ingresa un número válido."

    return render_template('calculadora_macronutrientes.html', resultado=resultado, info=info)

@app.route("/rutinas")
def rutinas():
    return render_template("rutinas.html")

@app.route('/rutinas/hombre')
def rutinas_hombre_pdf():
    if 'nombre' not in session or session['nombre'] == "":
        return render_template("login_requerido.html")
    return send_from_directory('static/pdf', 'rutinas_hombre.pdf', as_attachment=True)

@app.route('/rutinas/mujer')
def rutinas_mujer_pdf():
    if 'nombre' not in session or session['nombre'] == "":
        return render_template("login_requerido.html")
    return send_from_directory('static/pdf', 'rutinas_mujer.pdf', as_attachment=True)


@app.route('/analizador_recetas', methods=['GET', 'POST'])
def analizador_recetas():
    if 'nombre' not in session:
        return redirect(url_for('registrado'))

    food_data = {
        "Carne de Res": {"proteins": 26, "carbs": 0, "fats": 20},
        "Tocino": {"proteins": 12, "carbs": 1, "fats": 35},
        "Papas": {"proteins": 2, "carbs": 17, "fats": 0.1},
        "Zanahorias": {"proteins": 0.9, "carbs": 10, "fats": 0.2},
        "Cebolla": {"proteins": 1.1, "carbs": 9, "fats": 0.1},
        "Pimientos": {"proteins": 1, "carbs": 6, "fats": 0.2},
        "Tomate": {"proteins": 1.2, "carbs": 4, "fats": 0.2},
        "Aceite de Oliva": {"proteins": 0, "carbs": 0, "fats": 100},
        "Tortillas": {"proteins": 7, "carbs": 46, "fats": 3},
        "Cilantro": {"proteins": 2.1, "carbs": 3.7, "fats": 0.5},
        "Limón": {"proteins": 0.6, "carbs": 5.4, "fats": 0.1},
        "Lechuga": {"proteins": 1.4, "carbs": 3.2, "fats": 0.2},
        "Pepino": {"proteins": 0.7, "carbs": 3.6, "fats": 0.1},
        "Pollo": {"proteins": 31, "carbs": 0, "fats": 3.6},
        "Ajo": {"proteins": 1.6, "carbs": 33, "fats": 0.1},
        "Perejil": {"proteins": 3, "carbs": 6, "fats": 0.8},
        "Carne molida de res": {"proteins": 22, "carbs": 0, "fats": 15},
        "Pan rallado": {"proteins": 7, "carbs": 55, "fats": 1},
        "Huevo": {"proteins": 6.3, "carbs": 0.4, "fats": 5},
        "Pescado": {"proteins": 20, "carbs": 0, "fats": 5},
    }

    recipes = {
        "Discada": ["Carne de Res", "Tocino", "Papas", "Zanahorias",
                    "Cebolla", "Pimientos", "Tomate", "Aceite de Oliva"],
        "Ensalada": ["Lechuga", "Tomate", "Pepino", "Zanahorias", "Aceite de Oliva"],
        "Tacos": ["Tortillas", "Carne de Res", "Cebolla", "Cilantro", "Limón"],
        "Albóndigas": ["Carne molida de res", "Ajo", "Pan rallado", "Huevo",
                       "Tomate", "Cebolla", "Aceite de Oliva"],
        "Pescado": ["Pescado", "Limón", "Aceite de Oliva", "Ajo", "Perejil"]
    }

    total_proteins = total_carbs = total_fats = 0
    ingredient_data = []
    health_status = ""
    recipe_name = None

    if request.method == 'POST':
        recipe_name = request.form.get('recipe')

        if not recipe_name or recipe_name not in recipes:
            return render_template('analizador_recetas.html', recipes=recipes, error="Debes seleccionar una receta válida.")

        quantities = request.form.getlist('quantities')
        ingredients = recipes[recipe_name]

        if len(quantities) != len(ingredients):
            return render_template('analizador_recetas.html', recipes=recipes, recipe_name=recipe_name, error="Debes ingresar todas las cantidades.")

        for ingredient, quantity in zip(ingredients, quantities):
            try:
                quantity = float(quantity)
            except:
                quantity = 0

            data = food_data.get(ingredient, {"proteins":0,"carbs":0,"fats":0})
            protein = (data['proteins'] * quantity) / 100
            carbs = (data['carbs'] * quantity) / 100
            fats = (data['fats'] * quantity) / 100

            ingredient_data.append({
                'ingredient': ingredient,
                'quantity': quantity,
                'protein': round(protein, 2),
                'carbs': round(carbs, 2),
                'fats': round(fats, 2)
            })

            total_proteins += protein
            total_carbs += carbs
            total_fats += fats

        try:
            health_score = total_proteins / (total_carbs + total_fats)
        except:
            health_score = 0

        if health_score > 0.4:
            health_status = "¡Receta saludable!"
        elif health_score > 0.2:
            health_status = "Receta balanceada."
        else:
            health_status = "Receta alta en carbohidratos o grasas."

        return render_template(
            'analizador_recetas.html',
            ingredient_data=ingredient_data,
            total_proteins=round(total_proteins, 2),
            total_carbs=round(total_carbs, 2),
            total_fats=round(total_fats, 2),
            health_status=health_status,
            recipe_name=recipe_name,
            recipes=recipes
        )

    return render_template('analizador_recetas.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
