from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Vi är f*n bäst!'


if __name__ == '__main__':
    app.run(debug=True)
