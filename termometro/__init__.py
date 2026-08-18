import logging
import os

from flask import Flask

# Raiz do projeto (um nível acima do pacote), onde templates/ e static/
# já vivem desde a versão original — mantém os dois sem precisar movê-los.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static'),
    )

    from .routes import bp
    app.register_blueprint(bp)

    return app
