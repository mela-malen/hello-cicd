from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Vad roligt det är när det lyckas!'


if __name__ == '__main__':
    app.run(debug=True)
