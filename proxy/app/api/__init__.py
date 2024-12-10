from flask import Flask

app = Flask(__name__)

from engine.blueprint import engine_bp

app.register_blueprint(engine_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)