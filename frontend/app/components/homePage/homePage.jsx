"use client"
import Link from "next/link"

export default function HomePage() {

    return (
        <div className="font-sans flex flex-col min-h-screen w-full">

            <header className="bg-gray-100 p-4 text-center">
                <img src="/images/caixabank.png" alt="Logo de Caixa-Bank" className="h-12 mx-auto" />
            </header>

            <main className="flex-grow flex flex-col justify-center p-4 text-center">
                <h1 className="text-6xl font-bold flex justify-center mb-10 montBlack">Bienvenido a Caixa Bank</h1>
                <p className="mb-8">Gestiona tus tarjetas de forma sencilla, rápida y segura desde cualquier lugar.</p>
                <div className="flex justify-center">
                    <Link href="/login" className="bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 transition duration-300 mt-20">
                        Iniciar sesión
                    </Link>
                </div>
            </main>

            <footer className="bg-gray-100 p-4 text-center flex justify-between">
                <div>
                    <a href="#" className="text-blue-600 hover:underline mx-2">Sobre Caixa Bank</a>
                </div>
                <div>
                    <a href="#" className="text-blue-600 hover:underline mx-2">Política de cookies</a>
                    <span>|</span>
                    <a href="#" className="text-blue-600 hover:underline mx-2">Política de privacidad</a>
                </div>
            </footer>

        </div>
    );
}