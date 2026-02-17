from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
URL = "http://localhost:5000/v1/usuarios/"

@app.route('/')
def home():
    # Pedimos la lista a la API y la mostramos en el indes
    res = requests.get(URL).json()
    return render_template('index.html', usuarios=res['usuarios'])

@app.route('/enviar', methods=['POST'])
def enviar():
    nuevo_usuario = {
        "id": int(request.form['id']),
        "nombre": request.form['nombre'],
        "edad": int(request.form['edad'])
    }
    requests.post(URL, json=nuevo_usuario)
    return redirect('/')

@app.route('/borrar/<int:id>')
def borrar(id):
    requests.delete(f"{URL}{id}")
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)