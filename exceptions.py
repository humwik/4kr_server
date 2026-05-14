from fastapi import Request
from fastapi.responses import JSONResponse

# Классы ошибок
class CustomExceptionA(Exception):
    def __init__(self, message: str):
        self.message = message

class CustomExceptionB(Exception):
    def __init__(self, message: str):
        self.message = message

# Функция регистрации
def register_custom_exceptions(app):
    @app.exception_handler(CustomExceptionA)
    async def handler_a(request: Request, exc: CustomExceptionA):
        return JSONResponse(status_code=400, content={"error_type": "CustomA", "message": exc.message})

    @app.exception_handler(CustomExceptionB)
    async def handler_b(request: Request, exc: CustomExceptionB):
        return JSONResponse(status_code=404, content={"error_type": "CustomB", "message": exc.message})