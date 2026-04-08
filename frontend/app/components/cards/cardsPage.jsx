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

/* ─── Estilos por categoría (solo presentación, no datos de negocio) ─── */
const CATEGORY_STYLES = {
    viajes: {
        icon: "viajes",
        color: "from-sky-600 to-blue-700",
        light: "bg-sky-50",
        accent: "text-sky-700",
        border: "border-sky-200",
        badge: "bg-sky-100 text-sky-800",
    },
    ecommerce: {
        icon: "ecommerce",
        color: "from-violet-600 to-purple-700",
        light: "bg-violet-50",
        accent: "text-violet-700",
        border: "border-violet-200",
        badge: "bg-violet-100 text-violet-800",
    },
    super: {
        icon: "super",
        color: "from-emerald-600 to-green-700",
        light: "bg-emerald-50",
        accent: "text-emerald-700",
        border: "border-emerald-200",
        badge: "bg-emerald-100 text-emerald-800",
    },
    ocio: {
        icon: "ocio",
        color: "from-rose-600 to-pink-700",
        light: "bg-rose-50",
        accent: "text-rose-700",
        border: "border-rose-200",
        badge: "bg-rose-100 text-rose-800",
    },
    clasicas: {
        icon: "clasicas",
        color: "from-slate-700 to-gray-900",
        light: "bg-slate-50",
        accent: "text-slate-700",
        border: "border-slate-200",
        badge: "bg-slate-100 text-slate-800",
    },
}

function mergeStyles(categories) {
    return categories.map((cat) => ({
        ...cat,
        ...CATEGORY_STYLES[cat.id],
    }))
}

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
    const [categorias, setCategorias] = useState([])
    const [activeCategory, setActiveCategory] = useState("viajes")
    const [showComparison, setShowComparison] = useState(false)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const userData = localStorage.getItem('user')
        const token = localStorage.getItem('token')
        if (!token || !userData) {
            router.push('/login')
            return
        }
        setUser(JSON.parse(userData))

        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/cards/catalog`)
            .then((res) => res.json())
            .then((data) => {
                setCategorias(mergeStyles(data))
                setLoading(false)
            })
            .catch(() => setLoading(false))
    }, [router])

    const activeCat = categorias.find((c) => c.id === activeCategory)

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex items-center justify-center">
                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
            </div>
        )
    }

    if (!categorias.length) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex items-center justify-center">
                <p className="text-gray-500">No se pudieron cargar las tarjetas.</p>
            </div>
        )
    }

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
                        {categorias.map((cat) => (
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
