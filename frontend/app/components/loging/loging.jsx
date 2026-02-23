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
            // Guardamos los datos del usuario en localStorage (sin token)
            localStorage.setItem('user', JSON.stringify(data));
            router.push('/dashboard');
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
        <>
            <div className="container mx-auto">
                <div className="flex flex-col justify-center items-center h-screen">
                    <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
                        <div className="flex justify-center mb-5">
                            <img src="/images/caixabank.png" alt="Logo CaixaBank" />
                        </div>

                        <div>
                            <h1 className="text-2xl font-bold flex justify-center mb-10 text-black">Iniciar sesión</h1>
                        </div>

                        {error && (
                            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit}>
                            <div className="mb-4">
                                <label htmlFor="email" className="block mb-2 text-sm font-medium text-black">Email</label>
                                <input type="email" onChange={(e) => setEmail(e.target.value)} id="email" name="email" className="shadow-sm border-gray-300 rounded-md w-full py-2 px-4 bg-gray-100" placeholder="ejemplo@caixabank.com" required />
                            </div>
                            <div className="mb-2">
                                <div className="flex items-center justify-between">
                                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-black">Contraseña</label>
                                    <Link href="/recuperar" className="text-sm text-blue-600 hover:underline">¿Has olvidado tu contraseña?</Link>
                                </div>
                            </div>
                            <input type="password" onChange={(e) => setPassword(e.target.value)} id="password" name="password" className="shadow-sm border-gray-300 rounded-md w-full py-2 px-4 mb-8 bg-gray-100" placeholder="••••••••" required />
                            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md w-full transition duration-300">Iniciar sesión</button>
                        </form>
                        <div className="mt-10 flex justify-center">
                            <p className="text-sm text-gray-500">¿Necesitas ayuda? <Link href="/contacto" className="text-blue-600 hover:underline">Escríbenos</Link></p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )

}
