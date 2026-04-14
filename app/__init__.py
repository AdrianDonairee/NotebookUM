from fastapi import FastAPI
from .controllers import register_blueprints


def create_app(config_class=None):
    app = FastAPI(title="NotebookUM API")

    # Keep parameter for backward compatibility with existing tests.
    _ = config_class

    # Register API routers
    register_blueprints(app)

    return app