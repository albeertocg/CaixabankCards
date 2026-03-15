"""
Script para generar usuarios fake y poblar la base de datos MongoDB.

Uso:
    cd backend
    python -m scripts.seed_users        # 100 usuarios por defecto
    python -m scripts.seed_users 50     # numero personalizado
"""

import random
import sys
from datetime import datetime, timedelta, timezone

import bcrypt
from faker import Faker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.config.settings import settings
from app.constants.transaction import TransactionCategory, TransactionType
from app.constants.user import EducationLevel, EmploymentStatus, MaritalStatus
from app.models.transaction import Transaction
from app.models.user import UserBase

fake = Faker("es_ES")
Faker.seed(42)


# ── helpers ──────────────────────────────────────────────────────────


def generate_dni() -> str:
    numero = random.randint(10000000, 99999999)
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{numero}{letras[numero % 23]}"


def generate_phone() -> str:
    return f"+346{random.randint(10000000, 99999999)}"


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


# ── generadores ──────────────────────────────────────────────────────


MERCHANTS: dict[TransactionCategory, list[str]] = {
    TransactionCategory.SUPERMARKET: ["Mercadona", "Carrefour", "Lidl", "Dia", "Alcampo"],
    TransactionCategory.RESTAURANT: ["McDonald's", "Burger King", "La Tagliatella", "VIPS", "Telepizza"],
    TransactionCategory.TRANSPORT: ["Renfe", "Metro Madrid", "Cabify", "Uber", "Repsol"],
    TransactionCategory.ENTERTAINMENT: ["Netflix", "Spotify", "Cinesa", "Fnac", "PlayStation Store"],
    TransactionCategory.HEALTH: ["Farmacia", "Hospital", "Clinica Dental", "Optica", "Gimnasio"],
    TransactionCategory.SHOPPING: ["Zara", "H&M", "Amazon", "El Corte Ingles", "MediaMarkt"],
    TransactionCategory.BILLS: ["Iberdrola", "Movistar", "Endesa", "Vodafone", "Orange"],
    TransactionCategory.EDUCATION: ["Universidad", "Academia", "Libreria", "Cursos Online"],
    TransactionCategory.TRAVEL: ["Booking.com", "Ryanair", "Renfe", "Hotel", "Airbnb"],
    TransactionCategory.OTHER_EXPENSE: ["Varios", "Otros"],
}

INCOME_CONCEPTS: dict[TransactionCategory, str] = {
    TransactionCategory.SALARY: "Nomina mensual",
    TransactionCategory.TRANSFER: "Transferencia recibida",
    TransactionCategory.OTHER_INCOME: "Otros ingresos",
}

EXPENSE_AMOUNTS: dict[TransactionCategory, tuple[int, int]] = {
    TransactionCategory.SUPERMARKET: (20, 150),
    TransactionCategory.RESTAURANT: (15, 80),
    TransactionCategory.TRANSPORT: (5, 100),
    TransactionCategory.ENTERTAINMENT: (5, 50),
    TransactionCategory.HEALTH: (10, 200),
    TransactionCategory.SHOPPING: (20, 300),
    TransactionCategory.BILLS: (30, 150),
    TransactionCategory.EDUCATION: (50, 500),
    TransactionCategory.TRAVEL: (100, 1000),
    TransactionCategory.OTHER_EXPENSE: (10, 100),
}


def generate_transactions(num_transactions: int = 50, max_days_back: int = 180) -> list[dict]:
    transactions = []

    for _ in range(num_transactions):
        days_ago = random.randint(1, max_days_back)
        fecha = datetime.now(timezone.utc) - timedelta(
            days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59)
        )

        if random.random() < 0.2:
            transaction_type = TransactionType.INCOME
            category = random.choice(
                [
                    TransactionCategory.SALARY,
                    TransactionCategory.TRANSFER,
                    TransactionCategory.OTHER_INCOME,
                ]
            )
            amount = (
                round(random.uniform(1200, 3500), 2)
                if category == TransactionCategory.SALARY
                else round(random.uniform(50, 1000), 2)
            )
            concept = INCOME_CONCEPTS[category]
            merchant = None
        else:
            transaction_type = TransactionType.EXPENSE
            category = random.choice(list(EXPENSE_AMOUNTS.keys()))
            min_amt, max_amt = EXPENSE_AMOUNTS[category]
            amount = -round(random.uniform(min_amt, max_amt), 2)
            merchant = random.choice(MERCHANTS.get(category, ["Comercio"]))
            concept = f"Compra en {merchant}"

        tx = Transaction(
            date=fecha,
            concept=concept,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            merchant=merchant,
        )
        transactions.append(tx.model_dump(mode="json"))

    transactions.sort(key=lambda transaction: transaction["date"], reverse=True)
    return transactions


def generate_user() -> dict:
    edad = random.randint(18, 75)
    fecha_nacimiento = datetime.now(timezone.utc) - timedelta(days=edad * 365 + random.randint(0, 365))

    # Situacion laboral segun edad
    if edad < 25:
        situacion = random.choice([EmploymentStatus.STUDENT, EmploymentStatus.EMPLOYED, EmploymentStatus.UNEMPLOYED])
    elif edad > 65:
        situacion = random.choice([EmploymentStatus.RETIRED, EmploymentStatus.SELF_EMPLOYED])
    else:
        situacion = random.choice(
            [EmploymentStatus.EMPLOYED, EmploymentStatus.SELF_EMPLOYED, EmploymentStatus.UNEMPLOYED]
        )

    # Ingresos segun situacion
    income_ranges = {
        EmploymentStatus.STUDENT: (0, 12000),
        EmploymentStatus.UNEMPLOYED: (0, 15000),
        EmploymentStatus.RETIRED: (15000, 35000),
        EmploymentStatus.SELF_EMPLOYED: (20000, 80000),
        EmploymentStatus.EMPLOYED: (18000, 70000),
    }
    lo, hi = income_ranges[situacion]
    ingresos = random.uniform(lo, hi)

    # Nivel de estudios segun edad
    if edad < 25:
        nivel_estudios = random.choice(
            [EducationLevel.HIGH_SCHOOL, EducationLevel.VOCATIONAL, EducationLevel.UNIVERSITY]
        )
    else:
        nivel_estudios = random.choice(list(EducationLevel))

    # Estado civil segun edad
    if edad < 25:
        estado_civil = random.choice([MaritalStatus.SINGLE, MaritalStatus.MARRIED])
    else:
        estado_civil = random.choice(list(MaritalStatus))

    # Dependientes
    if estado_civil == MaritalStatus.MARRIED and edad > 25:
        num_dependientes = random.choices([0, 1, 2, 3], weights=[0.2, 0.3, 0.3, 0.2])[0]
    else:
        num_dependientes = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]

    antiguedad_meses = random.randint(0, 180)

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
        "plan_pensiones",
    ]
    productos = random.sample(productos_disponibles, random.randint(1, 5))

    saldo = random.uniform(ingresos * 0.05, ingresos * 0.3)

    base_score = 600 + min(100, ingresos / 1000) + min(50, edad - 18) + random.randint(-50, 100)
    score = max(300, min(850, int(base_score)))

    tiene_deudas = score < 650 and random.random() < 0.6
    deuda = random.uniform(5000, 50000) if tiene_deudas else 0.0

    if antiguedad_meses > 0:
        dias_registro = antiguedad_meses * 30 - random.randint(0, 30)
        fecha_registro = datetime.now(timezone.utc) - timedelta(days=max(1, dias_registro))
    else:
        fecha_registro = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))

    # Generar password y hashearla
    dni = generate_dni()
    password = f"Password{dni[:4]}"

    transactions = generate_transactions(random.randint(20, 100), max_days_back=180)

    # Validar con UserBase (sin password ni campos de BD)
    user = UserBase(
        national_id=dni,
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
        employment_status=situacion,
        education_level=nivel_estudios,
        marital_status=estado_civil,
        num_dependents=num_dependientes,
        customer_tenure_months=antiguedad_meses,
        contracted_products=productos,
        average_balance=round(saldo, 2),
        credit_score=score,
        has_debts=tiene_deudas,
        debt_amount=round(deuda, 2),
        transactions=transactions,
        registration_date=fecha_registro,
        active=True,
    )

    doc = user.model_dump(mode="json")
    doc["hashed_password"] = hash_password(password)
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    return doc


# ── seed ─────────────────────────────────────────────────────────────


def seed_database(num_users: int = 100) -> None:
    print("Conectando a MongoDB...")

    client = MongoClient(settings.mongo_uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)

    try:
        db = client[settings.mongo_db_name]
        users_collection = db["users"]

        print(f"Conectado. Generando {num_users} usuarios...")

        users = []
        for user_index in range(num_users):
            users.append(generate_user())
            if (user_index + 1) % 10 == 0:
                print(f"   Generados {user_index + 1}/{num_users}")

        print("Insertando en la base de datos...")
        result = users_collection.insert_many(users)
        print(f"Insertados {len(result.inserted_ids)} usuarios")

        print(f"\nTotal en coleccion: {users_collection.count_documents({})}")

        for user in users_collection.find().limit(3):
            edad = (datetime.now(timezone.utc) - datetime.fromisoformat(user["birth_date"])).days // 365
            print(f"\n   {user['first_name']} {user['last_name']}")
            print(f"     DNI: {user['national_id']}")
            print(f"     Email: {user['email']}")
            print(f"     Edad: {edad} | Ingresos: {user['annual_income']:,.2f}e")
            print(f"     Score: {user['credit_score']} | Transacciones: {len(user['transactions'])}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("\nConexion cerrada.")


if __name__ == "__main__":
    num_usuarios = 100
    if len(sys.argv) > 1:
        try:
            num_usuarios = int(sys.argv[1])
        except ValueError:
            print("Argumento invalido, usando 100")

    seed_database(num_usuarios)
