from .example_controller import example_bp

def register_blueprints(app):
    app.register_blueprint(example_bp, url_prefix='/api/example')