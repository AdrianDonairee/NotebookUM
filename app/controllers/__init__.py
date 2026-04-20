from .example_controller import router as example_router
from .ai_controller import router as ai_router
from .file_controller import router as file_router
from .functionality_controller import router as functionality_router


def register_blueprints(app):
    app.include_router(example_router)
    app.include_router(ai_router)
    app.include_router(file_router)
    app.include_router(functionality_router)
