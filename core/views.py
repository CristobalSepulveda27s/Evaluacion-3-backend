from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Bienvenido a la API de Productos",
        "version": "1.0",
        "endpoints": {
            "auth": {
                "registro": "POST /api/auth/register/",
                "login": "POST /api/auth/login/",
                "refresh": "POST /api/auth/refresh/",
                "perfil": "GET /api/auth/profile/"
            },
            "productos": {
                "listar": "GET /api/productos/",
                "crear": "POST /api/productos/",
                "detalle": "GET /api/productos/{id}/",
                "actualizar": "PUT/PATCH /api/productos/{id}/",
                "eliminar": "DELETE /api/productos/{id}/"
            }
        }
    })