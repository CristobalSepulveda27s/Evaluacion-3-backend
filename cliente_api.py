import requests
import json

# ===============================
# FUNCIONES DE AUTENTICACIÓN JWT
# ===============================

def obtener_token_registro(username, password, email="", first_name="", last_name=""):
    """
    Obtiene token JWT registrando un nuevo usuario
    """
    url = "http://127.0.0.1:8000/api/auth/register/"
    
    data = {
        "username": username,
        "password": password,
        "password_confirm": password,
    }
    
    if email:
        data["email"] = email
    if first_name:
        data["first_name"] = first_name
    if last_name:
        data["last_name"] = last_name
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 201:
            token_data = response.json()
            return token_data['access']  # Devuelve el token de acceso
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def obtener_token_login(username, password):
    """
    Obtiene token JWT iniciando sesión
    """
    url = "http://127.0.0.1:8000/api/auth/login/"
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data['access']  # Devuelve el token de acceso
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def verificar_token(token):
    """
    Verifica si un token es válido
    """
    url = "http://127.0.0.1:8000/api/productos/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def refrescar_token(refresh_token):
    """
    Obtiene un nuevo token usando el refresh token
    """
    url = "http://127.0.0.1:8000/api/auth/refresh/"
    
    data = {
        "refresh": refresh_token
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data['access']  # Nuevo token de acceso
        else:
            print(f"❌ Error refrescando token: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

# ===============================
# FUNCIONES PARA PRODUCTOS (CON AUTORIZACIÓN)
# ===============================

def obtener_productos(token):
    """
    Obtiene todos los productos (requiere autorización)
    """
    url = "http://127.0.0.1:8000/api/productos/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()  # Lista de productos
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def crear_producto(token, nombre, precio, stock, descripcion="", disponible=True):
    """
    Crea un nuevo producto (requiere autorización)
    """
    url = "http://127.0.0.1:8000/api/productos/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "disponible": disponible
    }
    
    if descripcion:
        data["descripcion"] = descripcion
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            print("✅ Producto creado exitosamente")
            return response.json()
        else:
            print(f"❌ Error creando producto: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def actualizar_producto(token, producto_id, datos_actualizados):
    """
    Actualiza un producto existente (requiere autorización)
    """
    url = f"http://127.0.0.1:8000/api/productos/{producto_id}/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.patch(url, json=datos_actualizados, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Producto actualizado exitosamente")
            return response.json()
        else:
            print(f"❌ Error actualizando producto: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def eliminar_producto(token, producto_id):
    """
    Elimina un producto (requiere autorización)
    """
    url = f"http://127.0.0.1:8000/api/productos/{producto_id}/"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        
        if response.status_code == 204:
            print("✅ Producto eliminado exitosamente")
            return True
        else:
            print(f"❌ Error eliminando producto: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

# ===============================
# EJEMPLO DE USO COMPLETO
# ===============================

def ejemplo_uso_completo():
    """
    Ejemplo de cómo usar todas las funciones de autorización
    """
    print("🔐 EJEMPLO DE AUTORIZACIÓN JWT")
    
    # 1. Obtener token (registro o login)
    token = obtener_token_registro(
        username="usuario_ejemplo",
        password="clave123",
        email="ejemplo@test.com"
    )
    
    if not token:
        # Intentar con login si el registro falla
        token = obtener_token_login("usuario_ejemplo", "clave123")
    
    if not token:
        print("❌ No se pudo obtener token de autorización")
        return
    
    print(f"✅ Token obtenido: {token[:50]}...")
    
    # 2. Verificar que el token funciona
    if verificar_token(token):
        print("✅ Token válido")
    else:
        print("❌ Token inválido")
        return
    
    # 3. Obtener productos (requiere autorización)
    print("\n📦 Obteniendo productos...")
    productos = obtener_productos(token)
    
    if productos:
        print(f"✅ Se encontraron {len(productos)} productos")
        for producto in productos:
            print(f"   - {producto['nombre']}: ${producto['precio']}")
    
    # 4. Crear un nuevo producto (requiere autorización)
    print("\n🆕 Creando nuevo producto...")
    nuevo_producto = crear_producto(
        token=token,
        nombre="Producto de Ejemplo",
        precio=29.99,
        stock=15,
        descripcion="Este es un producto de ejemplo"
    )
    
    if nuevo_producto:
        print(f"✅ Producto creado con ID: {nuevo_producto['id']}")

# ===============================
# CLIENTE INTERACTIVO MEJORADO
# ===============================

def cliente_interactivo():
    """
    Cliente interactivo con manejo completo de autorización
    """
    token = None
    
    while True:
        print("\n" + "="*50)
        print("🔐 SISTEMA DE AUTORIZACIÓN JWT")
        print("="*50)
        
        if token:
            print(f"✅ Token activo: {token[:30]}...")
            print("1. Ver productos")
            print("2. Crear producto")
            print("3. Actualizar producto")
            print("4. Eliminar producto")
            print("5. Verificar token")
            print("6. Cerrar sesión")
            print("7. Salir")
        else:
            print("❌ No autenticado")
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if not token:
            # Usuario no autenticado
            if opcion == "1":
                print("\n📝 REGISTRO DE USUARIO")
                username = input("Usuario: ")
                password = input("Contraseña: ")
                email = input("Email (opcional): ")
                
                token = obtener_token_registro(username, password, email)
                if token:
                    print("✅ Registro exitoso y token obtenido")
            
            elif opcion == "2":
                print("\n🔐 INICIO DE SESIÓN")
                username = input("Usuario: ")
                password = input("Contraseña: ")
                
                token = obtener_token_login(username, password)
                if token:
                    print("✅ Inicio de sesión exitoso")
                else:
                    print("❌ Credenciales incorrectas")
            
            elif opcion == "3":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")
        
        else:
            # Usuario autenticado
            if opcion == "1":
                productos = obtener_productos(token)
                if productos:
                    print("\n📦 LISTA DE PRODUCTOS:")
                    for p in productos:
                        disp = "✅" if p.get('disponible', True) else "❌"
                        print(f"   {p['id']}: {p['nombre']} - ${p['precio']} - Stock: {p['stock']} {disp}")
            
            elif opcion == "2":
                print("\n🆕 CREAR PRODUCTO")
                nombre = input("Nombre: ")
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                descripcion = input("Descripción (opcional): ")
                disponible = input("¿Disponible? (s/n): ").lower() == 's'
                
                crear_producto(token, nombre, precio, stock, descripcion, disponible)
            
            elif opcion == "3":
                productos = obtener_productos(token)
                if productos:
                    print("\n📦 PRODUCTOS DISPONIBLES:")
                    for p in productos:
                        print(f"   {p['id']}: {p['nombre']}")
                    
                    producto_id = input("\nID del producto a actualizar: ")
                    print("Deja vacío los campos que no quieras cambiar:")
                    
                    datos = {}
                    nuevo_nombre = input("Nuevo nombre: ")
                    if nuevo_nombre: datos["nombre"] = nuevo_nombre
                    
                    nuevo_precio = input("Nuevo precio: ")
                    if nuevo_precio: datos["precio"] = float(nuevo_precio)
                    
                    nuevo_stock = input("Nuevo stock: ")
                    if nuevo_stock: datos["stock"] = int(nuevo_stock)
                    
                    if datos:
                        actualizar_producto(token, producto_id, datos)
                    else:
                        print("❌ No se ingresaron cambios")
            
            elif opcion == "4":
                productos = obtener_productos(token)
                if productos:
                    print("\n📦 PRODUCTOS DISPONIBLES:")
                    for p in productos:
                        print(f"   {p['id']}: {p['nombre']}")
                    
                    producto_id = input("\nID del producto a eliminar: ")
                    confirmar = input("¿Estás seguro? (s/n): ").lower()
                    
                    if confirmar == 's':
                        eliminar_producto(token, producto_id)
            
            elif opcion == "5":
                if verificar_token(token):
                    print("✅ Token válido y activo")
                else:
                    print("❌ Token inválido o expirado")
                    token = None
            
            elif opcion == "6":
                token = None
                print("🔒 Sesión cerrada")
            
            elif opcion == "7":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")

if __name__ == "__main__":
    # Ejecutar el ejemplo completo
    # ejemplo_uso_completo()
    
    # O ejecutar el cliente interactivo
    cliente_interactivo()