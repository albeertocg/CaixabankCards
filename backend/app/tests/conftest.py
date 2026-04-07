"""Shared fixtures for agent behavioral tests.

Provides mock user profiles, chat service with patched DB,
and session helpers for end-to-end LLM testing.
"""

import random
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from app.constants.transaction import TransactionCategory, TransactionType
from app.constants.user import EducationLevel, EmploymentStatus, MaritalStatus
from app.services.chat_service import ChatService


EXPENSE_AMOUNTS: dict[TransactionCategory, tuple[int, int]] = {
    TransactionCategory.SUPERMARKET: (20, 150),
    TransactionCategory.RESTAURANT: (15, 80),
    TransactionCategory.TRANSPORT: (5, 100),
    TransactionCategory.ENTERTAINMENT: (5, 50),
    TransactionCategory.SHOPPING: (20, 300),
    TransactionCategory.TRAVEL: (150, 1200),
    TransactionCategory.BILLS: (30, 150),
    TransactionCategory.OTHER_EXPENSE: (10, 100),
}


def _generate_transactions(
    weights: dict[TransactionCategory, int],
    n: int = 50,
    income_amount: float = 3000.0,
) -> list[dict]:
    cats = list(weights.keys())
    ws = list(weights.values())
    txs: list[dict] = []

    for _ in range(n):
        days_ago = random.randint(1, 180)
        date = datetime.now(timezone.utc) - timedelta(days=days_ago)

        if random.random() < 0.12:
            txs.append(
                {
                    "date": date.isoformat(),
                    "concept": "Nomina mensual",
                    "amount": round(
                        random.uniform(income_amount * 0.9, income_amount * 1.1), 2
                    ),
                    "transaction_type": TransactionType.INCOME.value,
                    "category": TransactionCategory.SALARY.value,
                    "merchant": None,
                }
            )
        else:
            cat = random.choices(cats, weights=ws)[0]
            lo, hi = EXPENSE_AMOUNTS.get(cat, (10, 100))
            txs.append(
                {
                    "date": date.isoformat(),
                    "concept": f"Compra {cat.value}",
                    "amount": -round(random.uniform(lo, hi), 2),
                    "transaction_type": TransactionType.EXPENSE.value,
                    "category": cat.value,
                    "merchant": None,
                }
            )

    return txs


def _make_user(
    *,
    first_name: str = "Ana",
    last_name: str = "García Test",
    annual_income: float = 35000.0,
    age: int = 35,
    employment_status: str = EmploymentStatus.EMPLOYED.value,
    education_level: str = EducationLevel.UNIVERSITY.value,
    marital_status: str = MaritalStatus.SINGLE.value,
    credit_score: int = 700,
    transactions: list[dict] | None = None,
) -> dict:
    birth = datetime.now(timezone.utc) - timedelta(days=age * 365 + 100)
    return {
        "_id": "test_user_fixture",
        "national_id": "12345678Z",
        "first_name": first_name,
        "last_name": last_name,
        "email": "test@fixture.com",
        "phone": "+34600000000",
        "birth_date": birth,
        "address": "Calle Test 1",
        "city": "Barcelona",
        "postal_code": "08001",
        "province": "Barcelona",
        "annual_income": annual_income,
        "employment_status": employment_status,
        "education_level": education_level,
        "marital_status": marital_status,
        "num_dependents": 0,
        "customer_tenure_months": 36,
        "contracted_products": ["cuenta_corriente"],
        "average_balance": round(annual_income * 0.15, 2),
        "credit_score": credit_score,
        "has_debts": False,
        "debt_amount": 0.0,
        "transactions": transactions or [],
        "registration_date": datetime.now(timezone.utc).isoformat(),
        "active": True,
        "hashed_password": "$2b$12$fakehash",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


VIAJERO = _make_user(
    first_name="Carlos",
    last_name="Viajes Test",
    annual_income=55000.0,
    age=38,
    credit_score=750,
    transactions=_generate_transactions(
        {
            TransactionCategory.TRAVEL: 70,
            TransactionCategory.TRANSPORT: 10,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.SHOPPING: 5,
            TransactionCategory.ENTERTAINMENT: 5,
        }
    ),
)

SHOPPER_ONLINE = _make_user(
    first_name="Laura",
    last_name="Compras Test",
    annual_income=32000.0,
    age=28,
    credit_score=680,
    transactions=_generate_transactions(
        {
            TransactionCategory.SHOPPING: 65,
            TransactionCategory.SUPERMARKET: 12,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.ENTERTAINMENT: 8,
            TransactionCategory.BILLS: 5,
        }
    ),
)

SUPERMERCADO = _make_user(
    first_name="María",
    last_name="Super Test",
    annual_income=25000.0,
    age=42,
    marital_status=MaritalStatus.MARRIED.value,
    credit_score=710,
    transactions=_generate_transactions(
        {
            TransactionCategory.SUPERMARKET: 60,
            TransactionCategory.BILLS: 15,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.SHOPPING: 10,
            TransactionCategory.OTHER_EXPENSE: 5,
        }
    ),
)

SIN_TRANSACCIONES_ALTO = _make_user(
    first_name="Pedro",
    last_name="Premium Test",
    annual_income=80000.0,
    age=45,
    credit_score=800,
    transactions=[],
)

SIN_TRANSACCIONES_BAJO = _make_user(
    first_name="Sofía",
    last_name="Básico Test",
    annual_income=12000.0,
    age=22,
    employment_status=EmploymentStatus.STUDENT.value,
    education_level=EducationLevel.UNIVERSITY.value,
    credit_score=580,
    transactions=[],
)

NO_ELEGIBLE_PREMIUM = _make_user(
    first_name="Javier",
    last_name="Modesto Test",
    annual_income=20000.0,
    age=30,
    credit_score=650,
    transactions=_generate_transactions(
        {
            TransactionCategory.TRAVEL: 60,
            TransactionCategory.TRANSPORT: 20,
            TransactionCategory.RESTAURANT: 10,
            TransactionCategory.SHOPPING: 10,
        }
    ),
)

MENOR_EDAD = _make_user(
    first_name="Hugo",
    last_name="Joven Test",
    annual_income=6000.0,
    age=16,
    employment_status=EmploymentStatus.STUDENT.value,
    credit_score=500,
    transactions=[],
)

FOODIE = _make_user(
    first_name="Miguel",
    last_name="Restaurantes Test",
    annual_income=40000.0,
    age=33,
    employment_status=EmploymentStatus.SELF_EMPLOYED.value,
    credit_score=700,
    transactions=_generate_transactions(
        {
            TransactionCategory.RESTAURANT: 55,
            TransactionCategory.ENTERTAINMENT: 20,
            TransactionCategory.SHOPPING: 10,
            TransactionCategory.SUPERMARKET: 10,
            TransactionCategory.TRANSPORT: 5,
        }
    ),
)


USER_PROFILES: dict[str, dict] = {
    "viajero": VIAJERO,
    "shopper_online": SHOPPER_ONLINE,
    "supermercado": SUPERMERCADO,
    "sin_tx_alto": SIN_TRANSACCIONES_ALTO,
    "sin_tx_bajo": SIN_TRANSACCIONES_BAJO,
    "no_elegible_premium": NO_ELEGIBLE_PREMIUM,
    "menor_edad": MENOR_EDAD,
    "foodie": FOODIE,
}

_active_user: dict | None = None


def set_active_user(user: dict | None) -> None:
    global _active_user
    _active_user = user


async def _mock_find_by_id(self, user_id: str) -> dict | None:
    return _active_user


@pytest.fixture(autouse=True)
def _patch_user_repo(monkeypatch):
    from app.repositories.user_repository import UserRepository

    monkeypatch.setattr(UserRepository, "find_by_id", _mock_find_by_id)


@pytest_asyncio.fixture
async def chat() -> ChatService:
    return ChatService()


@pytest_asyncio.fixture
async def session_viajero(chat: ChatService):
    set_active_user(VIAJERO)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {"session_id": session_id, "greeting": greeting, "user": VIAJERO}


@pytest_asyncio.fixture
async def session_shopper(chat: ChatService):
    set_active_user(SHOPPER_ONLINE)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {"session_id": session_id, "greeting": greeting, "user": SHOPPER_ONLINE}


@pytest_asyncio.fixture
async def session_supermercado(chat: ChatService):
    set_active_user(SUPERMERCADO)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {"session_id": session_id, "greeting": greeting, "user": SUPERMERCADO}


@pytest_asyncio.fixture
async def session_sin_tx_alto(chat: ChatService):
    set_active_user(SIN_TRANSACCIONES_ALTO)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {
        "session_id": session_id,
        "greeting": greeting,
        "user": SIN_TRANSACCIONES_ALTO,
    }


@pytest_asyncio.fixture
async def session_sin_tx_bajo(chat: ChatService):
    set_active_user(SIN_TRANSACCIONES_BAJO)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {
        "session_id": session_id,
        "greeting": greeting,
        "user": SIN_TRANSACCIONES_BAJO,
    }


@pytest_asyncio.fixture
async def session_no_elegible(chat: ChatService):
    set_active_user(NO_ELEGIBLE_PREMIUM)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {"session_id": session_id, "greeting": greeting, "user": NO_ELEGIBLE_PREMIUM}


@pytest_asyncio.fixture
async def session_foodie(chat: ChatService):
    set_active_user(FOODIE)
    session_id, greeting = await chat.create_session_with_greeting("test_user_fixture")
    return {"session_id": session_id, "greeting": greeting, "user": FOODIE}
