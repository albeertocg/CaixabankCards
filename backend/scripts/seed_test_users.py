"""
Script para insertar usuarios de prueba con perfiles de gasto específicos.

Útil para testear el chatbot de recomendación de tarjetas.
Cada usuario tiene un patrón de gasto bien definido.

Uso:
    cd backend
    python -m scripts.seed_test_users
"""

import random
from datetime import datetime, timedelta, timezone

import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.config.settings import settings
from app.constants.transaction import TransactionCategory, TransactionType
from app.constants.user import EducationLevel, EmploymentStatus, MaritalStatus
from app.models.transaction import Transaction
from app.models.user import UserBase

# ── constantes ────────────────────────────────────────────────────────

MERCHANTS: dict[TransactionCategory, list[str]] = {
    TransactionCategory.SUPERMARKET: ["Mercadona", "Carrefour", "Lidl", "Dia", "Alcampo"],
    TransactionCategory.RESTAURANT: ["McDonald's", "Burger King", "La Tagliatella", "VIPS", "Telepizza"],
    TransactionCategory.TRANSPORT: ["Renfe", "Metro Madrid", "Cabify", "Uber", "Repsol"],
    TransactionCategory.ENTERTAINMENT: ["Netflix", "Spotify", "Cinesa", "Fnac", "PlayStation Store"],
    TransactionCategory.HEALTH: ["Farmacia", "Hospital", "Clinica Dental", "Optica", "Gimnasio"],
    TransactionCategory.SHOPPING: ["Zara", "H&M", "Amazon", "El Corte Ingles", "MediaMarkt"],
    TransactionCategory.BILLS: ["Iberdrola", "Movistar", "Endesa", "Vodafone", "Orange"],
    TransactionCategory.EDUCATION: ["Universidad", "Academia", "Libreria", "Cursos Online"],
    TransactionCategory.TRAVEL: ["Booking.com", "Ryanair", "Vueling", "Hotel", "Airbnb", "Iberia", "LATAM"],
    TransactionCategory.OTHER_EXPENSE: ["Varios", "Otros"],
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
    TransactionCategory.TRAVEL: (150, 1200),
    TransactionCategory.OTHER_EXPENSE: (10, 100),
}

# Perfiles de prueba: cada uno tiene pesos para las categorías de gasto
# Los pesos se usan en random.choices para determinar la categoría de cada transacción
TEST_PROFILES = [
    {
        "name": "TEST Viajero Frecuente",
        "first_name": "Carlos",
        "last_name": "Viajes Test",
        "email": "test.viajero@ejemplo.com",
        "password": "Test1234!",
        "income": 55000,
        "employment": EmploymentStatus.EMPLOYED,
        "education": EducationLevel.UNIVERSITY,
        "marital": MaritalStatus.MARRIED,
        "score": 750,
        "age": 38,
        "description": "90% gastos en viajes y transporte",
        "weights": {
            TransactionCategory.TRAVEL: 70,
            TransactionCategory.TRANSPORT: 10,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.SHOPPING: 5,
            TransactionCategory.ENTERTAINMENT: 5,
        },
    },
    {
        "name": "TEST Shopper Online",
        "first_name": "Laura",
        "last_name": "Compras Test",
        "email": "test.shopper@ejemplo.com",
        "password": "Test1234!",
        "income": 32000,
        "employment": EmploymentStatus.EMPLOYED,
        "education": EducationLevel.UNIVERSITY,
        "marital": MaritalStatus.SINGLE,
        "score": 680,
        "age": 28,
        "description": "~80% gastos en compras y moda",
        "weights": {
            TransactionCategory.SHOPPING: 65,
            TransactionCategory.SUPERMARKET: 12,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.ENTERTAINMENT: 8,
            TransactionCategory.BILLS: 5,
        },
    },
    {
        "name": "TEST Foodie y Ocio",
        "first_name": "Miguel",
        "last_name": "Restaurantes Test",
        "email": "test.foodie@ejemplo.com",
        "password": "Test1234!",
        "income": 40000,
        "employment": EmploymentStatus.SELF_EMPLOYED,
        "education": EducationLevel.UNIVERSITY,
        "marital": MaritalStatus.SINGLE,
        "score": 700,
        "age": 33,
        "description": "~75% gastos en restaurantes y ocio",
        "weights": {
            TransactionCategory.RESTAURANT: 55,
            TransactionCategory.ENTERTAINMENT: 20,
            TransactionCategory.SHOPPING: 10,
            TransactionCategory.SUPERMARKET: 10,
            TransactionCategory.TRANSPORT: 5,
        },
    },
    {
        "name": "TEST Jubilado Conservador",
        "first_name": "Antonio",
        "last_name": "Pension Test",
        "email": "test.jubilado@ejemplo.com",
        "password": "Test1234!",
        "income": 22000,
        "employment": EmploymentStatus.RETIRED,
        "education": EducationLevel.HIGH_SCHOOL,
        "marital": MaritalStatus.MARRIED,
        "score": 720,
        "age": 68,
        "description": "~90% gastos en facturas, super y salud",
        "weights": {
            TransactionCategory.BILLS: 40,
            TransactionCategory.SUPERMARKET: 30,
            TransactionCategory.HEALTH: 20,
            TransactionCategory.TRANSPORT: 10,
        },
    },
    {
        "name": "TEST Estudiante Universitario",
        "first_name": "Sofia",
        "last_name": "Estudiante Test",
        "email": "test.estudiante@ejemplo.com",
        "password": "Test1234!",
        "income": 8000,
        "employment": EmploymentStatus.STUDENT,
        "education": EducationLevel.UNIVERSITY,
        "marital": MaritalStatus.SINGLE,
        "score": 580,
        "age": 22,
        "description": "Gastos mixtos: restaurantes, ocio, super y transporte",
        "weights": {
            TransactionCategory.RESTAURANT: 30,
            TransactionCategory.ENTERTAINMENT: 25,
            TransactionCategory.SUPERMARKET: 20,
            TransactionCategory.TRANSPORT: 15,
            TransactionCategory.EDUCATION: 10,
        },
    },
]


# ── helpers ───────────────────────────────────────────────────────────


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def generate_dni() -> str:
    n = random.randint(10000000, 99999999)
    return f"{n}{'TRWAGMYFPDXBNJZSQVHLCKE'[n % 23]}"


def generate_transactions(category_weights: dict, n: int = 70) -> list[dict]:
    cats = list(category_weights.keys())
    weights = list(category_weights.values())
    txs = []

    for _ in range(n):
        days_ago = random.randint(1, 180)
        fecha = datetime.now(timezone.utc) - timedelta(
            days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59)
        )

        # 15% ingresos (nomina)
        if random.random() < 0.15:
            tx = Transaction(
                date=fecha,
                concept="Nomina mensual",
                amount=round(random.uniform(1800, 4000), 2),
                transaction_type=TransactionType.INCOME,
                category=TransactionCategory.SALARY,
                merchant=None,
            )
        else:
            cat = random.choices(cats, weights=weights)[0]
            lo, hi = EXPENSE_AMOUNTS[cat]
            merchant = random.choice(MERCHANTS.get(cat, ["Comercio"]))
            tx = Transaction(
                date=fecha,
                concept=f"Compra en {merchant}",
                amount=-round(random.uniform(lo, hi), 2),
                transaction_type=TransactionType.EXPENSE,
                category=cat,
                merchant=merchant,
            )
        txs.append(tx.model_dump(mode="json"))

    txs.sort(key=lambda t: t["date"], reverse=True)
    return txs


# ── seed ─────────────────────────────────────────────────────────────


def seed_test_users() -> None:
    print("Conectando a MongoDB...")
    client = MongoClient(settings.mongo_uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)

    try:
        col = client[settings.mongo_db_name]["users"]

        # Limpiar test users previos para evitar duplicados
        test_emails = [p["email"] for p in TEST_PROFILES]
        deleted = col.delete_many({"email": {"$in": test_emails}})
        if deleted.deleted_count:
            print(f"Eliminados {deleted.deleted_count} test users previos\n")

        docs = []
        for p in TEST_PROFILES:
            dni = generate_dni()
            now = datetime.now(timezone.utc)
            birth = now - timedelta(days=p["age"] * 365 + random.randint(0, 365))
            reg = now - timedelta(days=random.randint(365, 1800))

            user = UserBase(
                national_id=dni,
                first_name=p["first_name"],
                last_name=p["last_name"],
                email=p["email"],
                phone=f"+346{random.randint(10000000, 99999999)}",
                birth_date=birth,
                address="Calle Test 1",
                city="Barcelona",
                postal_code="08001",
                province="Barcelona",
                annual_income=float(p["income"]),
                employment_status=p["employment"],
                education_level=p["education"],
                marital_status=p["marital"],
                num_dependents=0,
                customer_tenure_months=random.randint(12, 60),
                contracted_products=["cuenta_corriente", "cuenta_nomina"],
                average_balance=round(p["income"] * 0.15, 2),
                credit_score=p["score"],
                has_debts=False,
                debt_amount=0.0,
                transactions=generate_transactions(p["weights"], n=70),
                registration_date=reg,
                active=True,
            )

            doc = user.model_dump(mode="json")
            doc["hashed_password"] = hash_password(p["password"])
            doc["created_at"] = now.isoformat()
            docs.append((p, doc))

        col.insert_many([doc for _, doc in docs])

        print("Usuarios de prueba insertados exitosamente:")
        print("=" * 65)
        for p, _ in docs:
            top = sorted(p["weights"].items(), key=lambda x: x[1], reverse=True)
            print(f"Perfil  : {p['name']}")
            print(f"  Descripcion: {p['description']}")
            print(f"  Email      : {p['email']}")
            print(f"  Password   : {p['password']}")
            print(f"  Ingresos   : {p['income']:,}€  |  Score: {p['score']}  |  Edad: {p['age']}")
            top_str = ", ".join(f"{c.value}({w}%)" for c, w in top[:3])
            print(f"  Top cats   : {top_str}")
            print()

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        client.close()
        print("Conexion cerrada.")


if __name__ == "__main__":
    seed_test_users()
