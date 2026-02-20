"""
Script para generar usuarios fake y poblar la base de datos MongoDB
"""
import os
import sys
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

# Añadir el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.user import User, MaritalStatus, EducationLevel, EmploymentStatus

# Cargar variables de entorno
load_dotenv()

# Configurar Faker con localización española
fake = Faker('es_ES')
Faker.seed(42)  # Para reproducibilidad


def generate_dni():
    """Genera un DNI español válido"""
    numero = random.randint(10000000, 99999999)
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letra = letras[numero % 23]
    return f"{numero}{letra}"


def generate_phone():
    """Genera un teléfono móvil español"""
    return f"+346{random.randint(10000000, 99999999)}"


def generate_user() -> dict:
    """Genera un usuario fake con datos realistas"""
    
    # Determinar edad realista para tener tarjetas (18-75 años)
    edad = random.randint(18, 75)
    fecha_nacimiento = datetime.now() - timedelta(days=edad * 365 + random.randint(0, 365))
    
    # Situación laboral según edad
    if edad < 25:
        situacion_laboral = random.choice([
            EmploymentStatus.STUDENT,
            EmploymentStatus.EMPLOYED,
            EmploymentStatus.UNEMPLOYED
        ])
    elif edad > 65:
        situacion_laboral = random.choice([
            EmploymentStatus.RETIRED,
            EmploymentStatus.SELF_EMPLOYED
        ])
    else:
        situacion_laboral = random.choice([
            EmploymentStatus.EMPLOYED,
            EmploymentStatus.SELF_EMPLOYED,
            EmploymentStatus.UNEMPLOYED
        ])
    
    # Ingresos según situación laboral y edad
    if situacion_laboral == EmploymentStatus.STUDENT:
        ingresos = random.uniform(0, 12000)
    elif situacion_laboral == EmploymentStatus.UNEMPLOYED:
        ingresos = random.uniform(0, 15000)
    elif situacion_laboral == EmploymentStatus.RETIRED:
        ingresos = random.uniform(15000, 35000)
    elif situacion_laboral == EmploymentStatus.SELF_EMPLOYED:
        ingresos = random.uniform(20000, 80000)
    else:  # EMPLOYED
        ingresos = random.uniform(18000, 70000)
    
    # Nivel de estudios según edad
    if edad < 25:
        nivel_estudios = random.choice([
            EducationLevel.HIGH_SCHOOL,
            EducationLevel.VOCATIONAL,
            EducationLevel.UNIVERSITY
        ])
    else:
        nivel_estudios = random.choice(list(EducationLevel))
    
    # Estado civil según edad
    if edad < 25:
        estado_civil = random.choice([MaritalStatus.SINGLE, MaritalStatus.MARRIED])
    else:
        estado_civil = random.choice(list(MaritalStatus))
    
    # Dependientes según edad y estado civil
    if estado_civil == MaritalStatus.MARRIED and edad > 25:
        num_dependientes = random.choices([0, 1, 2, 3], weights=[0.2, 0.3, 0.3, 0.2])[0]
    else:
        num_dependientes = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]
    
    # Antiguedad como cliente (0-15 años)
    antiguedad_cliente_meses = random.randint(0, 180)
    
    # Productos bancarios contratados
    productos_disponibles = [
        "cuenta_corriente",
        "cuenta_ahorro",
        "cuenta_nomina",
        "deposito",
        "fondo_inversion",
        "prestamo_personal",
        "prestamo_hipoteca",
        "seguro_vida",
        "seguro_hogar",
        "plan_pensiones"
    ]
    num_productos = random.randint(1, 5)
    productos_contratados = random.sample(productos_disponibles, num_productos)
    
    # Saldo promedio según ingresos
    saldo_promedio = random.uniform(ingresos * 0.05, ingresos * 0.3)
    
    # Score crediticio (correlacionado con ingresos y edad)
    base_score = 600
    score_por_ingresos = min(100, ingresos / 1000)
    score_por_edad = min(50, edad - 18)
    score_aleatorio = random.randint(-50, 100)
    score_crediticio = int(base_score + score_por_ingresos + score_por_edad + score_aleatorio)
    score_crediticio = max(300, min(850, score_crediticio))
    
    # Deudas (más probable si score bajo)
    tiene_deudas = score_crediticio < 650 and random.random() < 0.6
    importe_deudas = random.uniform(5000, 50000) if tiene_deudas else 0.0
    
    # Fecha de registro (entre 1 mes y la antigüedad como cliente)
    if antiguedad_cliente_meses > 0:
        dias_registro = min(antiguedad_cliente_meses * 30, antiguedad_cliente_meses * 30 - random.randint(0, 30))
        fecha_registro = datetime.now() - timedelta(days=dias_registro)
    else:
        fecha_registro = datetime.now() - timedelta(days=random.randint(1, 30))
    
    user = User(
        national_id=generate_dni(),
        first_name=fake.first_name(),
        last_name=f"{fake.last_name()} {fake.last_name()}",
        email=fake.email(),
        phone=generate_phone(),
        birth_date=fecha_nacimiento,
        address=fake.street_address(),
        city=fake.city(),
        postal_code=fake.postcode(),
        province=fake.state(),
        annual_income=round(ingresos, 2),
        employment_status=situacion_laboral,
        education_level=nivel_estudios,
        marital_status=estado_civil,
        num_dependents=num_dependientes,
        customer_tenure_months=antiguedad_cliente_meses,
        contracted_products=productos_contratados,
        average_balance=round(saldo_promedio, 2),
        credit_score=score_crediticio,
        has_debts=tiene_deudas,
        debt_amount=round(importe_deudas, 2),
        registration_date=fecha_registro,
        active=True
    )
    
    return user.model_dump()


def seed_database(num_users: int = 100):
    """
    Genera usuarios fake e inserta en MongoDB
    
    Args:
        num_users: Número de usuarios a generar
    """
    # Obtener URI de MongoDB
    uri = os.getenv("MONGODB_URL")
    
    if not uri:
        print("Error: No se encontró MONGODB_URL en el archivo .env")
        return
    
    print(f"🔗 Conectando a MongoDB...")
    
    try:
        # Conectar a MongoDB
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000
        )
        
        # Seleccionar base de datos y colección
        db = client['caixabank_cards']
        users_collection = db['users']
        
        print(f"Conectado a MongoDB")
        print(f"Generando {num_users} usuarios...")
        
        # Generar usuarios
        users = []
        for i in range(num_users):
            user = generate_user()
            users.append(user)
            if (i + 1) % 10 == 0:
                print(f"   Generados {i + 1}/{num_users} usuarios...")
        
        # Insertar usuarios en la base de datos
        print(f"Insertando usuarios en la base de datos...")
        result = users_collection.insert_many(users)
        
        print(f"¡Completado! Se insertaron {len(result.inserted_ids)} usuarios")
        
        # Mostrar estadísticas
        print(f"\nEstadísticas:")
        print(f"   Total usuarios: {users_collection.count_documents({})}")
        
        # Ejemplos de consultas
        print(f"\nEjemplos de usuarios:")
        for user in users_collection.find().limit(3):
            print(f"\n   • {user['first_name']} {user['last_name']}")
            print(f"     DNI: {user['national_id']}")
            print(f"     Email: {user['email']}")
            print(f"     Edad: {(datetime.now() - user['birth_date']).days // 365} años")
            print(f"     Ingresos: {user['annual_income']:,.2f}€")
            print(f"     Score: {user['credit_score']}")
            print(f"     Productos: {', '.join(user['contracted_products'])}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if 'client' in locals():
            client.close()
            print(f"\nConexión cerrada.")


if __name__ == "__main__":
    # Por defecto genera 100 usuarios, puedes cambiar este número
    num_usuarios = 100
    
    # Si se pasa un argumento, usarlo como número de usuarios
    if len(sys.argv) > 1:
        try:
            num_usuarios = int(sys.argv[1])
        except ValueError:
            print("Argumento inválido, usando valor por defecto (100)")
    
    print(f"Iniciando generación de {num_usuarios} usuarios fake...")
    seed_database(num_usuarios)
