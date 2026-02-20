"""
Script para probar la conexión a MongoDB Atlas
"""
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Cargar variables de entorno
load_dotenv()

# Obtener la URI desde el .env
uri = os.getenv("MONGODB_URL")

if not uri:
    print("Error: No se encontró MONGODB_URL en el archivo .env")
    exit(1)

print(f"Conectando a MongoDB...")
print(f"URI: {uri.split('@')[1] if '@' in uri else 'URI no válida'}")  # Ocultar credenciales

try:
    # Crear cliente con timeout de 5 segundos
    client = MongoClient(
        uri, 
        server_api=ServerApi('1'),
        serverSelectionTimeoutMS=5000,  # 5 segundos de timeout
        connectTimeoutMS=5000
    )
    
    # Enviar ping para confirmar conexión exitosa
    print("Enviando ping...")
    client.admin.command('ping')
    
    print("¡Conexión exitosa! Estás conectado a MongoDB Atlas.")
    
    # Información adicional
    db_list = client.list_database_names()
    print(f"\nBases de datos disponibles: {db_list}")
    
except Exception as e:
    print(f"\nError al conectar: {type(e).__name__}")
    print(f"Detalles: {e}")
    print("\nPosibles causas:")
    print("  1. Tu IP no está en la lista blanca de MongoDB Atlas")
    print("  2. Las credenciales son incorrectas")
    print("  3. Hay un firewall bloqueando la conexión")
    print("\nSolución para IP whitelist:")
    print("  - Ve a MongoDB Atlas → Network Access")
    print("  - Añade tu IP actual o usa 0.0.0.0/0 para permitir todas (solo desarrollo)")
    
finally:
    if 'client' in locals():
        client.close()
        print("\nConexión cerrada.")
