"use client"

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function loginHandler(user, router, setError) {
    try {
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            router.push('/cards');
        } else {
            const errorData = await response.json().catch(() => null);
            setError(errorData?.detail || 'Email o contraseña incorrectos');
        }
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
        setError('No se pudo conectar con el servidor');
    }
}

export default function Login() {

    const router = useRouter()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault();
        setError("");
        const user = {
            email: email,
            password: password,
        }
        loginHandler(user, router, setError);
    }

    return (
        <div className="min-h-screen w-full flex">
            <div
                className="hidden lg:flex lg:w-1/2 flex-col justify-between p-12"
                style={{ backgroundColor: '#007EAE' }}
            >
                <div>
                    <img
                        src="/images/caixabank.png"
                        alt="Logo CaixaBank"
                        className="h-10 brightness-0 invert"
                    />
                </div>

                <div className="space-y-8">
                    <div
                        className="w-20 h-20 rounded-2xl flex items-center justify-center"
                        style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}
                    >
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="4" y="10" width="32" height="22" rx="4" stroke="white" strokeWidth="1.5"/>
                            <rect x="4" y="16" width="32" height="6" fill="white" fillOpacity="0.3"/>
                            <rect x="8" y="25" width="8" height="3" rx="1" fill="white" fillOpacity="0.6"/>
                            <rect x="20" y="25" width="12" height="3" rx="1" fill="white" fillOpacity="0.4"/>
                        </svg>
                    </div>

                    <div className="space-y-4">
                        <h1 className="text-4xl font-bold text-white leading-tight">
                            Gestiona tus<br />tarjetas con<br />total control
                        </h1>
                        <p className="text-base leading-relaxed" style={{ color: 'rgba(255,255,255,0.75)' }}>
                            Consulta movimientos, controla gastos y administra todos tus productos desde un único lugar seguro.
                        </p>
                    </div>

                    <div className="space-y-3">
                        {[
                            'Acceso seguro con cifrado de extremo a extremo',
                            'Consulta de saldos y movimientos en tiempo real',
                            'Gestión completa de todas tus tarjetas',
                        ].map((feature) => (
                            <div key={feature} className="flex items-center gap-3">
                                <div
                                    className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                                    style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}
                                >
                                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                                        <path d="M2 5l2 2 4-4" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                                    </svg>
                                </div>
                                <span className="text-sm" style={{ color: 'rgba(255,255,255,0.8)' }}>{feature}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <p className="text-xs" style={{ color: 'rgba(255,255,255,0.5)' }}>
                    © 2026 CaixaBank, S.A. Todos los derechos reservados.
                </p>
            </div>

            <div className="w-full lg:w-1/2 flex items-center justify-center bg-[#F8FAFC] px-6 py-12">
                <div className="w-full max-w-md">

                    <div className="flex justify-center mb-10 lg:hidden">
                        <img src="/images/caixabank.png" alt="Logo CaixaBank" className="h-9" />
                    </div>

                    <div className="mb-8">
                        <h2 className="text-2xl font-bold leading-tight" style={{ color: '#1A1A2E' }}>
                            Bienvenido de nuevo
                        </h2>
                        <p className="mt-1 text-sm text-gray-500 leading-relaxed">
                            Introduce tus credenciales para acceder a tu banca digital.
                        </p>
                    </div>

                    {error && (
                        <div className="mb-6 flex items-start gap-3 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
                            <svg className="w-4 h-4 mt-0.5 flex-shrink-0" viewBox="0 0 16 16" fill="none">
                                <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
                                <path d="M8 5v3M8 11h.01" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                            <span>{error}</span>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="space-y-1.5">
                            <label htmlFor="email" className="block text-sm font-medium" style={{ color: '#1A1A2E' }}>
                                Email
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#007EAE]/30 focus:border-[#007EAE] transition-colors text-sm"
                                placeholder="ejemplo@caixabank.com"
                                required
                            />
                        </div>

                        <div className="space-y-1.5">
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm font-medium" style={{ color: '#1A1A2E' }}>
                                    Contraseña
                                </label>
                                <Link
                                    href="/recuperar"
                                    className="text-xs font-medium hover:underline transition-colors"
                                    style={{ color: '#007EAE' }}
                                >
                                    ¿Has olvidado tu contraseña?
                                </Link>
                            </div>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#007EAE]/30 focus:border-[#007EAE] transition-colors text-sm"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            className="w-full bg-[#007EAE] hover:bg-[#006490] text-white font-medium px-5 py-2.5 rounded-xl transition-colors text-sm mt-2"
                        >
                            Iniciar sesión
                        </button>
                    </form>

                    <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                        <p className="text-sm text-gray-500">
                            ¿Necesitas ayuda?{' '}
                            <Link
                                href="/contacto"
                                className="font-medium hover:underline transition-colors"
                                style={{ color: '#007EAE' }}
                            >
                                Escríbenos
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )

}
