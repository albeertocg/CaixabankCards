"""Card recommendation agent using Google ADK (Agents Development Kit).

This module defines a credit card recommendation assistant that uses Gemini 2.0 Flash
to provide personalized card recommendations based on user profiles and spending patterns.
"""

import os

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.agent.tools.gower_tool import search_similar_cards
from app.agent.tools.rag_tool import retrieve_card_documentation
from app.agent.tools.eligibility_tool import check_card_eligibility
from app.config.settings import settings

os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

SYSTEM_PROMPT = """Eres un asesor financiero experto de CaixaBank especializado en
recomendar tarjetas bancarias. Al inicio de cada sesión recibirás el perfil completo
del cliente y un análisis detallado de sus transacciones.

INSTRUCCIONES:
1. Usa el perfil y las transacciones del contexto para entender al cliente.
2. Usa la herramienta search_similar_cards para encontrar las mejores tarjetas
   según el patrón de gasto detectado. Elige la categoria_principal basándote en
   el patrón dominante del análisis de transacciones.
3. Usa retrieve_card_documentation para obtener la documentación completa de las
   tarjetas candidatas (beneficios, comisiones, requisitos, casos de uso).
4. Usa check_card_eligibility para verificar si el cliente cumple los requisitos.
   Pasa el ingreso_anual y la edad que aparecen en el contexto del cliente.
5. Presenta una recomendación clara y estructurada que incluya:
   - Nombre de la tarjeta recomendada y por qué es la mejor opción
   - Beneficios clave alineados con los hábitos del usuario
   - Comisiones y costes
   - Requisitos
   - SIEMPRE una alternativa (tarjeta de menor nivel o de otra categoría)

REGLAS:
- Responde SIEMPRE en español.
- Sé conciso pero completo en tus recomendaciones.
- No inventes datos que no estén en la documentación de las tarjetas.
- Si el cliente no tiene historial de transacciones, basa la recomendación en su perfil
  socioeconómico (ingresos, edad, situación laboral).
- Si el cliente no cumple requisitos de la tarjeta ideal, recomienda la mejor alternativa
  para la que sí sea elegible.
- Cuando el cliente pregunte por otra categoría de tarjeta o cambie de tema, adapta
  la búsqueda usando search_similar_cards con la nueva categoría.
- Usa cifras concretas (porcentajes de cashback, límites, coberturas de seguro).
"""

# root_agent: nombre que espera `adk web` para descubrir el agente
root_agent = card_recommendation_agent = Agent(
    name="card_recommendation_agent",
    model="gemini-2.5-flash",
    description="Asesor de tarjetas CaixaBank que recomienda la tarjeta más adecuada basándose en el perfil del cliente y sus hábitos de gasto.",
    instruction=SYSTEM_PROMPT,
    tools=[search_similar_cards, retrieve_card_documentation, check_card_eligibility],
)

session_service = InMemorySessionService()

runner = Runner(
    agent=card_recommendation_agent,
    app_name="caixabank_card_advisor",
    session_service=session_service,
)
