"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import ChatWidget from '../chat/ChatWidget'

/* ─── Iconos SVG inline ─── */
const icons = {
    viajes: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
    ),
    ecommerce: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
        </svg>
    ),
    super: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
        </svg>
    ),
    ocio: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
    ),
    clasicas: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
    ),
    check: (
        <svg className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
        </svg>
    ),
    star: (
        <svg className="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
    ),
}

/* ─── Datos de todas las tarjetas ─── */
const CATEGORIAS = [
    {
        id: "viajes",
        nombre: "Viajes",
        icon: "viajes",
        color: "from-sky-600 to-blue-700",
        light: "bg-sky-50",
        accent: "text-sky-700",
        border: "border-sky-200",
        badge: "bg-sky-100 text-sky-800",
        tarjetas: [
            {
                nombre: "Travel Classic",
                tier: "Classic",
                cuota: "0€",
                cuotaNote: "Sin coste",
                cashback: "0,5%",
                cashbackDesc: "en compras en el extranjero",
                limite: "3.000€",
                seguroViaje: "30.000€",
                ingresos: "No requerido",
                perfil: "Viajeros ocasionales (1-3 viajes/año)",
                destacado: false,
                beneficios: [
                    "Cambio de divisa preferencial sin comisión",
                    "Seguro de cancelación hasta 500€",
                    "Asistencia telefónica 24/7 en español",
                    "Compatible con Apple Pay y Google Pay",
                    "Emisión y reposición gratuitas",
                ],
                extras: [
                    { label: "Salas VIP", value: "No" },
                    { label: "Retirada extranjero", value: "3% (mín. 3€)" },
                    { label: "Seguro equipaje", value: "No" },
                ],
            },
            {
                nombre: "Travel Gold",
                tier: "Gold",
                cuota: "50€/año",
                cuotaNote: "Bonificable con 12.000€ en compras",
                cashback: "1,5%",
                cashbackDesc: "en compras en el extranjero",
                limite: "12.000€",
                seguroViaje: "100.000€",
                ingresos: "24.000€/año",
                perfil: "Viajeros frecuentes (5-10 viajes/año)",
                destacado: true,
                beneficios: [
                    "4 accesos/año a salas VIP (Priority Pass)",
                    "Seguro de equipaje hasta 2.000€",
                    "Seguro de cancelación hasta 3.000€",
                    "Compensación por retraso de vuelo (+4h)",
                    "Concierge: reservas hoteles, restaurantes",
                    "Programa de puntos: 2 pts/€ en viajes",
                ],
                extras: [
                    { label: "Salas VIP", value: "4 accesos/año" },
                    { label: "Retirada extranjero", value: "0€" },
                    { label: "Seguro equipaje", value: "2.000€" },
                ],
            },
            {
                nombre: "Travel Platinum",
                tier: "Platinum",
                cuota: "120€/año",
                cuotaNote: "Bonificable con 30.000€ en compras",
                cashback: "3%",
                cashbackDesc: "en viajes (vuelos, hoteles, coches)",
                limite: "30.000€",
                seguroViaje: "500.000€",
                ingresos: "60.000€/año",
                perfil: "Grandes viajeros (+15 viajes/año)",
                destacado: false,
                beneficios: [
                    "Acceso ilimitado a +1.000 salas VIP mundiales",
                    "Fast Track en controles de seguridad",
                    "Seguro equipaje hasta 5.000€ (electrónica incl.)",
                    "Seguro coche de alquiler completo (CDW)",
                    "Concierge Premium 24/7 en 25 idiomas",
                    "Metal card · Puntos élite: 3 pts/€",
                    "Upgrades automáticos en hoteles y aerolíneas",
                ],
                extras: [
                    { label: "Salas VIP", value: "Ilimitado" },
                    { label: "Retirada extranjero", value: "0€" },
                    { label: "Seguro equipaje", value: "5.000€" },
                ],
            },
        ],
        comparativa: {
            headers: ["Característica", "Classic", "Gold", "Platinum"],
            rows: [
                ["Cuota anual", "0€", "50€", "120€"],
                ["Ingresos mínimos", "No requerido", "24.000€", "60.000€"],
                ["Cashback viajes", "0,5%", "1,5%", "3%"],
                ["Límite crédito", "3.000€", "12.000€", "30.000€"],
                ["Seguro viaje", "30.000€", "100.000€", "500.000€"],
                ["Seguro equipaje", "No", "2.000€", "5.000€"],
                ["Salas VIP", "No", "4/año", "Ilimitado"],
                ["Fast Track", "No", "No", "Sí"],
                ["Concierge", "No", "Sí", "Premium 24/7"],
                ["Puntos por €", "No", "2 (viajes)", "3"],
            ],
        },
    },
    {
        id: "ecommerce",
        nombre: "Compras Online",
        icon: "ecommerce",
        color: "from-violet-600 to-purple-700",
        light: "bg-violet-50",
        accent: "text-violet-700",
        border: "border-violet-200",
        badge: "bg-violet-100 text-violet-800",
        tarjetas: [
            {
                nombre: "E-Commerce Basic",
                tier: "Basic",
                cuota: "0€",
                cuotaNote: "Sin coste",
                cashback: "0,5%",
                cashbackDesc: "en comercios adheridos",
                limite: "2.000€",
                seguroViaje: null,
                seguroCompras: "300€",
                ingresos: "No requerido",
                perfil: "Compradores online ocasionales",
                destacado: false,
                beneficios: [
                    "Tarjeta virtual con número diferente a la física",
                    "Tarjetas de un solo uso ilimitadas",
                    "Verificación 3D Secure en todas las compras",
                    "Extensión de garantía 6 meses (electrónica)",
                    "5-10% descuento en tiendas seleccionadas",
                    "Alta 100% online en 5 minutos",
                ],
                extras: [
                    { label: "Tarjetas virtuales", value: "Sí" },
                    { label: "Protección precio", value: "No" },
                    { label: "Extensión garantía", value: "6 meses" },
                ],
            },
            {
                nombre: "E-Commerce Advanced",
                tier: "Advanced",
                cuota: "20€/año",
                cuotaNote: "Bonificable con 5.000€ en compras online",
                cashback: "2%",
                cashbackDesc: "en todas las compras online (sin límite)",
                limite: "8.000€",
                seguroViaje: null,
                seguroCompras: "2.000€",
                ingresos: "18.000€/año",
                perfil: "Compradores frecuentes (5-15 compras/mes)",
                destacado: true,
                beneficios: [
                    "Verificación biométrica (huella + facial)",
                    "Generador ilimitado de tarjetas virtuales",
                    "Protección de precio: reembolso si baja en 30 días",
                    "Extensión de garantía 1 año en todos los productos",
                    "Hasta 15% descuento en marcas premium online",
                    "Envíos gratis en tiendas seleccionadas",
                    "Control parental para tarjetas adicionales",
                ],
                extras: [
                    { label: "Tarjetas virtuales", value: "Ilimitadas" },
                    { label: "Protección precio", value: "30 días" },
                    { label: "Extensión garantía", value: "1 año" },
                ],
            },
            {
                nombre: "E-Commerce Premium",
                tier: "Premium",
                cuota: "60€/año",
                cuotaNote: "Bonificable con 15.000€ en compras online",
                cashback: "4%",
                cashbackDesc: "en compras online (sin límite ni techo)",
                limite: "20.000€",
                seguroViaje: null,
                seguroCompras: "10.000€",
                ingresos: "36.000€/año",
                perfil: "Grandes compradores (+20 compras/mes)",
                destacado: false,
                beneficios: [
                    "Autenticación multifactor avanzada + monitoreo dark web",
                    "Cashback acreditado en 24h",
                    "Protección de precio extendida: 90 días",
                    "Extensión de garantía 2 años en todo",
                    "Asesor personal de compras y personal shopper virtual",
                    "Hasta 25% descuento en marcas de lujo",
                    "Gestión devoluciones premium: nos encargamos de todo",
                    "Hasta 5 tarjetas físicas + ilimitadas virtuales",
                ],
                extras: [
                    { label: "Tarjetas virtuales", value: "Personalizables" },
                    { label: "Protección precio", value: "90 días" },
                    { label: "Extensión garantía", value: "2 años" },
                ],
            },
        ],
        comparativa: {
            headers: ["Característica", "Basic", "Advanced", "Premium"],
            rows: [
                ["Cuota anual", "0€", "20€", "60€"],
                ["Ingresos mínimos", "No requerido", "18.000€", "36.000€"],
                ["Cashback", "0,5%", "2%", "4%"],
                ["Límite crédito", "2.000€", "8.000€", "20.000€"],
                ["Seguro compras", "300€", "2.000€", "10.000€"],
                ["Extensión garantía", "6 meses", "1 año", "2 años"],
                ["Protección precio", "No", "30 días", "90 días"],
                ["Tarjetas virtuales", "Sí", "Ilimitadas", "Personalizables"],
                ["Asesor personal", "No", "No", "Sí"],
                ["Descuentos", "5-10%", "Hasta 15%", "Hasta 25%"],
            ],
        },
    },
    {
        id: "super",
        nombre: "Supermercado",
        icon: "super",
        color: "from-emerald-600 to-green-700",
        light: "bg-emerald-50",
        accent: "text-emerald-700",
        border: "border-emerald-200",
        badge: "bg-emerald-100 text-emerald-800",
        tarjetas: [
            {
                nombre: "SuperCompra Ahorro",
                tier: "Ahorro",
                cuota: "0€",
                cuotaNote: "Sin coste",
                cashback: "2%",
                cashbackDesc: "en supermercados + 5% en partners",
                limite: "500€/día (débito)",
                seguroViaje: null,
                ingresos: "No requerido",
                perfil: "Familias con presupuesto ajustado",
                destacado: false,
                beneficios: [
                    "5% descuento adicional en partners (Mercadona, Carrefour, Dia…)",
                    "Vales descuento mensuales según gasto acumulado",
                    "App de control con alertas de presupuesto",
                    "Tickets digitales organizados automáticamente",
                    "Programa Cashback Boost en productos seleccionados",
                ],
                extras: [
                    { label: "Tarjetas adicionales", value: "No" },
                    { label: "Financiación sin intereses", value: "No" },
                    { label: "Cashback farmacias", value: "No" },
                ],
            },
            {
                nombre: "SuperCompra Familia",
                tier: "Familia",
                cuota: "15€/año",
                cuotaNote: "Bonificable con 6.000€ en compras",
                cashback: "3%",
                cashbackDesc: "en súpers + 2% farmacias + 1,5% gasolineras",
                limite: "5.000€",
                seguroViaje: null,
                ingresos: "20.000€ (familiar)",
                perfil: "Familias 2-5 miembros, gasto medio",
                destacado: true,
                beneficios: [
                    "Hasta 4 tarjetas adicionales sin coste para la familia",
                    "10% descuento en supermercados partner",
                    "Financiación sin intereses: 3-6 meses",
                    "Seguro de compra de alimentos hasta 500€",
                    "Envío a domicilio gratis en compras +50€",
                    "Programa de puntos: 1 pto/€ (canjeables en súper)",
                    "App familiar: gastos unificados + control parental",
                ],
                extras: [
                    { label: "Tarjetas adicionales", value: "4 gratis" },
                    { label: "Financiación sin intereses", value: "3-6 meses" },
                    { label: "Cashback farmacias", value: "2%" },
                ],
            },
            {
                nombre: "SuperCompra Gourmet",
                tier: "Gourmet",
                cuota: "50€/año",
                cuotaNote: "Bonificable con 15.000€ en compras",
                cashback: "5%",
                cashbackDesc: "en gourmet y delicatessen",
                limite: "15.000€",
                seguroViaje: null,
                ingresos: "40.000€/año",
                perfil: "Amantes de la gastronomía premium",
                destacado: false,
                beneficios: [
                    "3% en tiendas especializadas, 2% marketplaces gourmet",
                    "Hasta 20% descuento en tiendas gourmet y vinos selectos",
                    "Catas de vino, showcookings y ferias VIP",
                    "Sommelier virtual y asesor gastronómico personal",
                    "Envío gratuito desde 30€ y servicio personal shopper",
                    "Club de ventajas con niveles Bronze/Silver/Gold",
                    "Seguro de productos premium hasta 2.000€",
                ],
                extras: [
                    { label: "Tarjetas adicionales", value: "Sí" },
                    { label: "Financiación sin intereses", value: "12 meses" },
                    { label: "Eventos exclusivos", value: "Sí" },
                ],
            },
        ],
        comparativa: {
            headers: ["Característica", "Ahorro", "Familia", "Gourmet"],
            rows: [
                ["Cuota anual", "0€", "15€", "50€"],
                ["Ingresos mínimos", "No requerido", "20.000€", "40.000€"],
                ["Cashback súpers", "2%", "3%", "5%"],
                ["Límite", "500€/día (débito)", "5.000€", "15.000€"],
                ["Tarjetas adicionales", "No", "4 gratis", "Sí"],
                ["Financiación 0%", "No", "3-6 meses", "12 meses"],
                ["Cashback farmacias", "No", "2%", "N/A"],
                ["Puntos por €", "No", "1 pto/€", "2 ptos/€"],
                ["Eventos exclusivos", "No", "No", "Sí"],
                ["Envío gratis", "No", "+50€", "+30€"],
            ],
        },
    },
    {
        id: "ocio",
        nombre: "Restaurante y Ocio",
        icon: "ocio",
        color: "from-rose-600 to-pink-700",
        light: "bg-rose-50",
        accent: "text-rose-700",
        border: "border-rose-200",
        badge: "bg-rose-100 text-rose-800",
        tarjetas: [
            {
                nombre: "Ocio Joven",
                tier: "Joven",
                cuota: "0€",
                cuotaNote: "Gratis (18-30 años)",
                cashback: "2%",
                cashbackDesc: "en restaurantes, bares y cafeterías",
                limite: "1.500€",
                seguroViaje: null,
                ingresos: "No requerido",
                perfil: "Jóvenes 18-30 años con vida social activa",
                destacado: false,
                beneficios: [
                    "Cines 2x1 los martes + 15% resto de días",
                    "Preventas exclusivas de conciertos y festivales",
                    "Hasta 20% descuento en parques temáticos",
                    "10% descuento en McDonald's, Burger King, KFC",
                    "App social: divide cuentas, planes cercanos con IA",
                    "Diseño personalizable (10 diseños o tu foto)",
                    "Puntos x2 en ocio nocturno (viernes y sábados)",
                ],
                extras: [
                    { label: "Concierge", value: "No" },
                    { label: "Acceso spas", value: "No" },
                    { label: "Restaurantes Michelin", value: "No" },
                ],
            },
            {
                nombre: "Ocio Lifestyle",
                tier: "Lifestyle",
                cuota: "30€/año",
                cuotaNote: "Bonificable con 8.000€ en ocio",
                cashback: "4%",
                cashbackDesc: "en restaurantes + 3% ocio + 2% wellness",
                limite: "8.000€",
                seguroViaje: null,
                ingresos: "24.000€/año",
                perfil: "Profesionales 25-45 con vida social activa",
                destacado: true,
                beneficios: [
                    "Concierge para reservas en restaurantes con lista de espera",
                    "15% descuento en +500 restaurantes premium",
                    "4 accesos/año a circuitos de spa incluidos",
                    "15% descuento en gimnasios (DiR, Holmes Place…)",
                    "12 experiencias/año: catas, menús degustación, eventos",
                    "Programa de niveles Silver / Gold / Platinum",
                    "Seguro de cancelación de reservas hasta 200€",
                ],
                extras: [
                    { label: "Concierge", value: "Sí" },
                    { label: "Acceso spas", value: "4/año" },
                    { label: "Restaurantes Michelin", value: "Selección" },
                ],
            },
            {
                nombre: "Ocio Exclusive",
                tier: "Exclusive",
                cuota: "100€/año",
                cuotaNote: "Bonificable con 25.000€ en compras",
                cashback: "6%",
                cashbackDesc: "en Michelin + 5% alta gastronomía",
                limite: "25.000€",
                seguroViaje: null,
                ingresos: "60.000€/año",
                perfil: "Amantes del lujo y la alta gastronomía",
                destacado: false,
                beneficios: [
                    "Mesa garantizada en los restaurantes más exclusivos",
                    "6 cenas anuales en restaurantes Michelin incluidas",
                    "12 catas premium + 4 viajes gastronómicos al año",
                    "Concierge Premium 24/7 en 25 idiomas",
                    "Acceso VIP: F1, Fashion Week, galas benéficas",
                    "Metal card con grabado personalizado",
                    "Personal Chef Advisor para tus eventos",
                    "Club privado de socios con networking exclusivo",
                ],
                extras: [
                    { label: "Concierge", value: "Premium 24/7" },
                    { label: "Acceso spas", value: "Ilimitado" },
                    { label: "Restaurantes Michelin", value: "Acceso total" },
                ],
            },
        ],
        comparativa: {
            headers: ["Característica", "Joven", "Lifestyle", "Exclusive"],
            rows: [
                ["Cuota anual", "0€", "30€", "100€"],
                ["Edad", "18-30 años", "Sin límite", "Sin límite"],
                ["Ingresos mínimos", "No requerido", "24.000€", "60.000€"],
                ["Cashback restaurantes", "2%", "4%", "6% (Michelin)"],
                ["Límite crédito", "1.500€", "8.000€", "25.000€"],
                ["Concierge", "No", "Sí", "Premium 24/7"],
                ["Acceso spas", "No", "4/año", "Ilimitado"],
                ["Eventos exclusivos", "Preventas", "12/año", "Ilimitados"],
                ["Puntos por €", "1", "2-4", "3"],
                ["Tarjeta metal", "No", "Opcional", "Incluida"],
            ],
        },
    },
    {
        id: "clasicas",
        nombre: "Clásicas",
        icon: "clasicas",
        color: "from-slate-700 to-gray-900",
        light: "bg-slate-50",
        accent: "text-slate-700",
        border: "border-slate-200",
        badge: "bg-slate-100 text-slate-800",
        tarjetas: [
            {
                nombre: "CaixaBank Clásica",
                tier: "Clásica",
                cuota: "0€",
                cuotaNote: "Sin coste",
                cashback: "0,5%",
                cashbackDesc: "en todas las compras",
                limite: "1.000€/día (débito)",
                seguroViaje: "12.000€ (accidentes)",
                ingresos: "No requerido",
                perfil: "Uso diario sin complicaciones",
                destacado: false,
                beneficios: [
                    "Tarjeta de débito: gasta solo lo que tienes",
                    "Contactless, Apple Pay, Google Pay, Samsung Pay",
                    "Bizum integrado para envío instantáneo",
                    "Bloqueo temporal desde la app móvil",
                    "Sistema antifraude con monitoreo 24/7",
                    "Retiradas gratuitas en red CaixaBank",
                ],
                extras: [
                    { label: "Financiación 0%", value: "No" },
                    { label: "Comisión extranjero", value: "3% retiradas" },
                    { label: "Salas VIP", value: "No" },
                ],
            },
            {
                nombre: "CaixaBank Oro",
                tier: "Oro",
                cuota: "40€/año",
                cuotaNote: "0€ con nómina domiciliada",
                cashback: "1,5%",
                cashbackDesc: "en todas las compras sin excepción",
                limite: "10.000€",
                seguroViaje: "60.000€",
                ingresos: "24.000€/año",
                perfil: "Crédito flexible + seguros ampliados",
                destacado: true,
                beneficios: [
                    "Seguro de compras hasta 1.000€ por artículo (90 días)",
                    "Financiación sin intereses hasta 12 meses (+300€)",
                    "0€ en compras y retiradas en todo el mundo",
                    "Seguro de viaje hasta 60.000€ con asistencia",
                    "Programa de puntos: 1 pto/2€ + 2.000 pts bienvenida",
                    "Tarjeta de emergencia en viajes",
                ],
                extras: [
                    { label: "Financiación 0%", value: "Hasta 12 meses" },
                    { label: "Comisión extranjero", value: "0€" },
                    { label: "Salas VIP", value: "No" },
                ],
            },
            {
                nombre: "CaixaBank Infinite",
                tier: "Infinite",
                cuota: "200€/año",
                cuotaNote: "Bonificable con 50.000€ en compras",
                cashback: "3%",
                cashbackDesc: "en todas las compras (sin techo)",
                limite: "Desde 30.000€ (flexible)",
                seguroViaje: "1.000.000€",
                ingresos: "90.000€ o patrimonio 150.000€",
                perfil: "Clientes premium de alto patrimonio",
                destacado: false,
                beneficios: [
                    "Acceso ilimitado a +1.300 salas VIP (Priority Pass Prestige)",
                    "Concierge Premium 24/7 en 25 idiomas",
                    "Personal Banker dedicado con línea directa",
                    "Seguro de compras hasta 5.000€ + 1 año garantía extra",
                    "Financiación sin intereses hasta 18 meses (+1.000€)",
                    "Metal card con grabado personalizado",
                    "Bonus: +500€ si gastas +50.000€/año",
                    "Experiencias: vuelos Business, hoteles 5★, eventos VIP",
                ],
                extras: [
                    { label: "Financiación 0%", value: "Hasta 18 meses" },
                    { label: "Comisión extranjero", value: "0€" },
                    { label: "Salas VIP", value: "Ilimitado" },
                ],
            },
        ],
        comparativa: {
            headers: ["Característica", "Clásica", "Oro", "Infinite"],
            rows: [
                ["Cuota anual", "0€", "40€ (0€ nómina)", "200€"],
                ["Ingresos mínimos", "No requerido", "24.000€", "90.000€ / 150k€"],
                ["Tipo", "Débito", "Crédito", "Crédito Premium"],
                ["Cashback", "0,5%", "1,5%", "3%"],
                ["Límite", "1.000€/día", "10.000€", "Desde 30.000€"],
                ["Seguro viaje", "12.000€", "60.000€", "1.000.000€"],
                ["Seguro compras", "No", "1.000€", "5.000€"],
                ["Financiación 0%", "No", "12 meses", "18 meses"],
                ["Comisión extranjero", "3% retiradas", "0€", "0€"],
                ["Concierge", "No", "No", "Premium 24/7"],
                ["Salas VIP", "No", "No", "Ilimitado"],
                ["Personal Banker", "No", "No", "Sí"],
            ],
        },
    },
]

/* ─── Componentes auxiliares ─── */

function TierBadge({ tier, className }) {
    return (
        <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${className}`}>
            {tier}
        </span>
    )
}

function CardTier({ card, cat, index }) {
    return (
        <div
            className={`relative flex flex-col bg-white rounded-2xl border transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${
                card.destacado
                    ? `ring-2 ring-offset-2 ring-blue-500 shadow-lg ${cat.border}`
                    : `border-gray-200 shadow-md`
            }`}
        >
            {card.destacado && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
                    <span className="inline-flex items-center gap-1 bg-gradient-to-r from-blue-600 to-blue-500 text-white text-xs font-semibold px-4 py-1 rounded-full shadow-md">
                        {icons.star} Más popular
                    </span>
                </div>
            )}

            {/* Header */}
            <div className={`px-6 pt-7 pb-5 bg-gradient-to-br ${cat.color} rounded-t-2xl text-white`}>
                <TierBadge tier={card.tier} className="bg-white/20 text-white/90" />
                <h3 className="text-xl font-bold mt-3 leading-tight">{card.nombre}</h3>
                <p className="text-white/70 text-sm mt-1">{card.perfil}</p>
            </div>

            {/* Pricing */}
            <div className="px-6 py-5 border-b border-gray-100">
                <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-extrabold text-gray-900">{card.cuota}</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">{card.cuotaNote}</p>

                <div className="mt-4 grid grid-cols-2 gap-3">
                    <div className={`rounded-xl p-3 ${cat.light}`}>
                        <p className="text-[11px] font-semibold text-gray-500 uppercase tracking-wide">Cashback</p>
                        <p className={`text-lg font-bold ${cat.accent}`}>{card.cashback}</p>
                        <p className="text-[11px] text-gray-500 leading-tight mt-0.5">{card.cashbackDesc}</p>
                    </div>
                    <div className={`rounded-xl p-3 ${cat.light}`}>
                        <p className="text-[11px] font-semibold text-gray-500 uppercase tracking-wide">Límite</p>
                        <p className={`text-lg font-bold ${cat.accent}`}>{card.limite}</p>
                        <p className="text-[11px] text-gray-500 mt-0.5">Ingresos: {card.ingresos}</p>
                    </div>
                </div>
            </div>

            {/* Benefits */}
            <div className="px-6 py-5 flex-1">
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Beneficios incluidos</p>
                <ul className="space-y-2.5">
                    {card.beneficios.map((b, i) => (
                        <li key={i} className="flex gap-2 text-sm text-gray-700 leading-snug">
                            {icons.check}
                            <span>{b}</span>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Extras Footer */}
            <div className="px-6 py-4 bg-gray-50/80 rounded-b-2xl border-t border-gray-100">
                <div className="grid grid-cols-3 gap-2">
                    {card.extras.map((ex, i) => (
                        <div key={i} className="text-center">
                            <p className="text-[10px] text-gray-400 font-medium uppercase">{ex.label}</p>
                            <p className="text-xs font-semibold text-gray-700 mt-0.5">{ex.value}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

function ComparisonTable({ comparativa, cat }) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm">
                <thead>
                    <tr>
                        {comparativa.headers.map((h, i) => (
                            <th
                                key={i}
                                className={`text-left py-3 px-4 font-semibold ${
                                    i === 0 ? "text-gray-600" : `${cat.accent}`
                                } ${i === 0 ? "w-[200px]" : ""}`}
                            >
                                {h}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {comparativa.rows.map((row, ri) => (
                        <tr key={ri} className={ri % 2 === 0 ? "bg-gray-50/60" : ""}>
                            {row.map((cell, ci) => (
                                <td
                                    key={ci}
                                    className={`py-2.5 px-4 ${
                                        ci === 0 ? "font-medium text-gray-600" : "text-gray-800"
                                    }`}
                                >
                                    {cell}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

/* ─── Componente principal ─── */

export default function CardsPage() {
    const router = useRouter()
    const [user, setUser] = useState(null)
    const [activeCategory, setActiveCategory] = useState("viajes")
    const [showComparison, setShowComparison] = useState(false)

    useEffect(() => {
        const userData = localStorage.getItem('user')
        const token = localStorage.getItem('token')
        if (!token || !userData) {
            router.push('/login')
            return
        }
        setUser(JSON.parse(userData))
    }, [router])

    const activeCat = CATEGORIAS.find((c) => c.id === activeCategory)

    return (
        <>
        <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
            {/* Top bar */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-30 shadow-sm">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-4">
                        <img src="/images/caixabank.png" alt="CaixaBank" className="h-8" />
                        <span className="hidden sm:inline text-gray-300">|</span>
                        <h1 className="hidden sm:inline text-lg font-semibold text-gray-800">Tarjetas</h1>
                    </div>
                    {user && (
                        <p className="text-sm text-gray-500">
                            Hola, <span className="font-medium text-gray-700">{user.first_name} {user.last_name}</span>
                        </p>
                    )}
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
                {/* Hero */}
                <div className="text-center mb-10">
                    <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                        Encuentra tu tarjeta ideal
                    </h2>
                    <p className="mt-3 text-gray-500 max-w-2xl mx-auto">
                        5 categorías, 15 tarjetas. Desde opciones gratuitas hasta servicios premium exclusivos.
                        Compara y elige la que mejor se adapte a ti.
                    </p>
                </div>

                {/* Category Tabs */}
                <div className="flex justify-center mb-10">
                    <div className="inline-flex flex-wrap justify-center gap-2 p-1.5 bg-white rounded-2xl shadow-sm border border-gray-200">
                        {CATEGORIAS.map((cat) => (
                            <button
                                key={cat.id}
                                onClick={() => {
                                    setActiveCategory(cat.id)
                                    setShowComparison(false)
                                }}
                                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                                    activeCategory === cat.id
                                        ? `bg-gradient-to-r ${cat.color} text-white shadow-md`
                                        : "text-gray-600 hover:bg-gray-100"
                                }`}
                            >
                                {icons[cat.icon]}
                                <span className="hidden sm:inline">{cat.nombre}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Category Title */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h3 className="text-2xl font-bold text-gray-900">
                            Tarjetas {activeCat.nombre}
                        </h3>
                        <p className="text-sm text-gray-500 mt-1">Selecciona el nivel que se adapte a tus necesidades</p>
                    </div>
                    <button
                        onClick={() => setShowComparison(!showComparison)}
                        className="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors flex items-center gap-1.5"
                    >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
                        </svg>
                        {showComparison ? "Ocultar comparativa" : "Ver comparativa"}
                    </button>
                </div>

                {/* Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    {activeCat.tarjetas.map((card, i) => (
                        <CardTier key={card.nombre} card={card} cat={activeCat} index={i} />
                    ))}
                </div>

                {/* Comparison Table */}
                {showComparison && (
                    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 mb-10 animate-in fade-in">
                        <h4 className="text-lg font-bold text-gray-900 mb-4">Comparativa detallada</h4>
                        <ComparisonTable comparativa={activeCat.comparativa} cat={activeCat} />
                    </div>
                )}

                {/* Footer info */}
                <div className="text-center text-xs text-gray-400 mt-12 pb-8 space-y-1">
                    <p>Información actualizada a Febrero 2026</p>
                    <p>
                        Para más información:{" "}
                        <span className="text-blue-500">www.caixabank.es</span> | 900 40 40 90
                    </p>
                </div>
            </main>
        </div>
        <ChatWidget userId={user?.id} />
        </>
    )
}
