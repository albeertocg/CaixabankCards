"""
Script de prueba para testear los endpoints de la API.
Ejecutar: python -m app.tests.test_api
(Asegúrate de que el servidor esté corriendo primero)
"""

import httpx

BASE_URL = "http://127.0.0.1:8000"

# ─── Datos de prueba ───────────────────────────────────────────

usuario_prueba = {
    "national_id": "12345678A",
    "first_name": "Carlos",
    "last_name": "García López",
    "email": "carlos@example.com",
    "phone": "+34600000000",
    "birth_date": "1990-05-15T00:00:00Z",
    "address": "Calle Ejemplo 123",
    "city": "Madrid",
    "postal_code": "28001",
    "province": "Madrid",
    "annual_income": 35000.00,
    "employment_status": "empleado",
    "education_level": "universidad",
    "marital_status": "soltero",
    "num_dependents": 0,
    "customer_tenure_months": 24,
    "contracted_products": [],
    "average_balance": 8500.50,
    "credit_score": 720,
    "has_debts": False,
    "debt_amount": 0.0,
    "registration_date": "2024-02-01T10:00:00Z",
    "active": True,
    "password": "123456789"
}

login_prueba = {
    "email": "carlos@example.com",
    "password": "123456789"
}


# ─── Funciones de test ─────────────────────────────────────────

def test_registro():
    """POST - Registrar un nuevo usuario"""
    print("\n🔹 TEST: Registrar usuario")
    print(f"   POST {BASE_URL}/api/auth/register")
    
    response = httpx.post(f"{BASE_URL}/api/auth/register", json=usuario_prueba, timeout=30.0)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response


def test_login():
    """POST - Login de usuario"""
    print("\n🔹 TEST: Login")
    print(f"   POST {BASE_URL}/api/auth/login")
    
    response = httpx.post(f"{BASE_URL}/api/auth/login", json=login_prueba, timeout=30.0)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response


# ─── Ejecutar tests ────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  TESTS DE LA API - CaixabankCards")
    print("=" * 50)

    # 1. Registro
    test_registro()

    # 2. Login
    test_login()

    print("\n" + "=" * 50)
    print("  TESTS COMPLETADOS")
    print("=" * 50)
