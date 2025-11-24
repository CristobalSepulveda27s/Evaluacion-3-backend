import requests

def iniciar_sesion():
    print("\n🔐 INICIAR SESIÓN")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    try:
        resp = requests.post("https://evaluacion-3-backend.onrender.com/api/token/",
                           json={"username": username, "password": password})
        print(resp)
        if resp.status_code == 200:
            data = resp.json()
            print("✅ Login exitoso!")
            return data['access']
        else:
            print("❌ Credenciales incorrectas")
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None

def main():
    token = None
    
    while not token:
        print("\n🚀 CLIENTE JWT")
        print("1. Iniciar sesión")
        opcion = input("Opción: ")
        
        if opcion == "1":
            token = iniciar_sesion()
        else:
            print("❌ Opción inválida")
    
    # Menú principal
    while True:
        print("\n🏪 MENÚ PRODUCTOS")
        print("1. Ver productos")
        print("2. Crear producto")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        opcion = input("Opción: ")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        if opcion == "1":
            try:
                resp = requests.get("https://evaluacion-3-backend.onrender.com/api/productos/", headers=headers)
                if resp.status_code == 200:
                    productos = resp.json()
                    if productos:
                        print(f"\n📦 Total de productos: {len(productos)}")
                        for p in productos:
                            print(f"  {p['id']}: {p['nombre']} - ${p['precio']} - Stock: {p['stock']}")
                    else:
                        print(" No hay productos registrados")
                else:
                    print("❌ Error al obtener productos:", resp.text)
            except Exception as e:
                print("❌ Error de conexión:", e)
        
        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            descripcion = input("Descripción (opcional): ") or ""
            
            try:
                resp = requests.post("https://evaluacion-3-backend.onrender.com/api/productos/", 
                                   json={
                                       "nombre": nombre, 
                                       "precio": precio, 
                                       "stock": stock,
                                       "descripcion": descripcion
                                   },
                                   headers=headers)
                if resp.status_code == 201:
                    print("✅ Producto creado exitosamente!")
                else:
                    print("❌ Error al crear producto:", resp.text)
            except Exception as e:
                print("❌ Error de conexión:", e)
        
        elif opcion == "3":
            id_producto = input("ID del producto a editar: ")
            print("Deja en blanco los campos que no quieras cambiar:")
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_precio = input("Nuevo precio: ")
            nuevo_stock = input("Nuevo stock: ")
            nueva_descripcion = input("Nueva descripción: ")
            
            data = {}
            if nuevo_nombre: data["nombre"] = nuevo_nombre
            if nuevo_precio: data["precio"] = float(nuevo_precio)
            if nuevo_stock: data["stock"] = int(nuevo_stock)
            if nueva_descripcion: data["descripcion"] = nueva_descripcion
            
            try:
                resp = requests.patch(f"https://evaluacion-3-backend.onrender.com/api/productos/{id_producto}/", 
                                    json=data,
                                    headers=headers)
                if resp.status_code == 200:
                    print("✅ Producto editado exitosamente!")
                else:
                    print("❌ Error al editar producto:", resp.text)
            except Exception as e:
                print("❌ Error de conexión:", e)
        
        elif opcion == "4":
            id_producto = input("ID del producto a eliminar: ")
            
            try:
                resp = requests.delete(f"https://evaluacion-3-backend.onrender.com/api/productos/{id_producto}/", 
                                     headers=headers)
                if resp.status_code == 204:
                    print("✅ Producto eliminado exitosamente!")
                else:
                    print("❌ Error al eliminar producto:", resp.text)
            except Exception as e:
                print("❌ Error de conexión:", e)
        
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()