import numpy as np
import os
from flask import Flask, request, render_template, make_response
import joblib
import datetime


app = Flask(__name__, static_url_path='/static')
model = joblib.load('model/model.pkl')


@app.route('/')
def display_gui():
    return render_template('index.html')

@app.route('/previsao', methods=['POST'])
def previsao():
	rooms = request.form['rooms']
	view = request.form['viewQuantity']
	sqft_living = request.form['sqft_living']
	floors = request.form['floors']
	condition = request.form['condition']
	yr_renovated = int(request.form['yr_renovated'])
	yr_built = request.form['yr_built']
	sqft_basement = request.form['sqft_basement']

	actual_year = datetime.date.today().year
	age = actual_year - yr_renovated
	
	if view == '':
		view = 0
	if sqft_basement == '':
		sqft_basement = 0

	print(":::::: Dados ::::::")
	print("view: {}".format(view))
	print("rooms: {}".format(rooms))
	print("sqft_living: {}".format(sqft_living))
	print("floors: {}".format(floors))
	print("condition: {}".format(condition))
	print("age: {}".format(age))
	print("yr_built: {}".format(yr_built))
	print("sqft_basement: {}".format(sqft_basement))
	print("\n")

	dados_previsao = np.array([[rooms, view, sqft_living,floors, condition, age, yr_built, sqft_basement]])
	dados_previsao = dados_previsao.astype(np.float64)

	valor = model.predict(dados_previsao)[0][0]
	valor = round(valor, 2)
	print("Preço predito: {}".format(str(valor)))

	return render_template('index.html',valor=str(valor),rooms =rooms, view=view, sqft_living=sqft_living,
	floors=floors, condition=condition, age=age, yr_built=yr_built, sqft_basement=sqft_basement)

if __name__ == "__main__":
        port = int(os.environ.get('PORT', 8080))
        app.run(host='localhost', port=port)
