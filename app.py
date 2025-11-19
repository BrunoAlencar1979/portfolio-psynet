from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Aqui você pode passar variáveis para o HTML se precisar no futuro
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)