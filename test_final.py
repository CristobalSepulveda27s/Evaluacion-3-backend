import requests
import json

def test_completo():
    print("🧪 TEST COMPLETO DEL SISTEMA")
    
    # 1. Registrar usuario
    print("\n1. 📝 Registrando usuario...")
    resp = requests.post(
        "http://127.0.0.1:8000/api/auth/register/",
        json={
            "username": "usuariofinal",
            "password": "clave123",
            "password_confirm": "clave123"
        }
    )
    
    if resp.status_code == 201:
        token = resp.json()['access']
        print("✅ Usuario registrado y token obtenido")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Crear producto
        print("\n2. 🆕 Creando producto...")
        resp = requests.post(
            "http://127.0.0.1:8000/api/productos/",
            json={
                "nombre": "Producto de Prueba",
                "precio": 99.99,
                "stock": 50,
                "disponible": True
            },
            headers=headers
        )
        
        if resp.status_code == 201:
            print("✅ Producto creado exitosamente")
            
            # 3. Listar productos
            print("\n3. 📦 Listando productos...")
            resp = requests.get("http://127.0.0.1:8000/api/productos/", headers=headers)
            
            if resp.status_code == 200:
                productos = resp.json()
                print(f"✅ Productos obtenidos: {len(productos)}")
                for p in productos:
                    print(f"   - {p['nombre']}: ${p['precio']} (Stock: {p['stock']})")
                
                print("\n🎉 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")
                return True
    
    print("❌ Algo salió mal")
    return False

if __name__ == "__main__":
    test_completo()
