# Prueba-backend3

DATABASES = {
    "default": {
       "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("dbname"),
        "USER": os.getenv("user"),
        "PASSWORD": os.getenv("password"),
        "HOST": os.getenv("host"),
        "PORT": os.getenv("port"),
    }
}
    'onrender.com',
    'evaluacion-3-backend.onrender.com',
    '127.0.0.1'
    http://localhost:8000/api/auth/register/