from flask import Flask, render_template
from werkzeug import exceptions
from instance import IApplicationConfiguration

def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    import Application.error_handlers as errhndl
    # app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    # app.register_error_handler(exceptions.NotFound, errhndl.handle_notfound_errors)
    
    @app.get('/')
    def home():
        return render_template('index.html')
            
    return app