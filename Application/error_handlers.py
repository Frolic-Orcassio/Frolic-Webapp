from werkzeug import exceptions
from typing import cast

def jsonify_default_errors(e: exceptions.HTTPException) -> tuple[dict, int]:
        code: int
        description: str | list
        
        if issubclass(type(e), exceptions.InternalServerError):
            UnhandledException = cast(exceptions.InternalServerError, e)
            if UnhandledException.original_exception is not None and any(args:=UnhandledException.original_exception.args):
                description = args[0] if len(args)==1 else list(args)
            else:
                description = UnhandledException.description
            
            code = UnhandledException.code
        else:
            description = e.description # type: ignore
            code = e.code # type: ignore
                    
        data = dict(description=description)
        return data, code

# def handle_notfound_errors(e: exceptions.NotFound):
#     res = requests.get('https://smit1199.pythonanywhere.com'+request.path)
#     return res.text