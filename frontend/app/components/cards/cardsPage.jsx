"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function CardsPage() {

    const router = useRouter()
    const [user, setUser] = useState(null)

    useEffect(() => {
        const userData = localStorage.getItem('user')
        const token = localStorage.getItem('token')
        if (!token || !userData) {
            router.push('/login')
            return
        }
        setUser(JSON.parse(userData))
    }, [router])

    const tarjetas = [
        { id: 1, nombre: "Visa Classic", tipo: "Débito" },
        { id: 2, nombre: "Visa Gold", tipo: "Crédito" },
        { id: 3, nombre: "MasterCard", tipo: "Crédito" },
        { id: 4, nombre: "Visa Platinum", tipo: "Crédito" },
        { id: 5, nombre: "Visa Joven", tipo: "Débito" },
    ]

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-black"> Informacion de Tarjetas</h1>
                    {user && (
                        <p className="text-gray-600">Hola, {user.first_name} {user.last_name}</p>
                    )}
                </div>

                <div className="flex gap-4">
                    {tarjetas.map((tarjeta) => (
                        <div
                            key={tarjeta.id}
                            className="flex-1 bg-white rounded-xl shadow-md p-6 min-h-[200px] flex flex-col justify-between hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
                        >
                            <div>
                                <h2 className="text-lg font-semibold text-black">{tarjeta.nombre}</h2>
                                <p className="text-sm text-gray-500 mt-1">{tarjeta.tipo}</p>
                            </div>
                            <div className="mt-4">
                                <p className="text-xs text-gray-400">**** **** **** ****</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
