"use client"

import { useState, useEffect, useRef } from "react"

const WS_BASE = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/api/chat/ws"

export default function ChatWidget({ userId }) {
    const [open, setOpen] = useState(false)
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState("")
    const [status, setStatus] = useState("idle")
    const [waiting, setWaiting] = useState(false)

    const wsRef = useRef(null)
    const bottomRef = useRef(null)
    const inputRef = useRef(null)
    const sessionIdRef = useRef(null)

    useEffect(() => {
        if (!userId || wsRef.current) return

        const storedSid = sessionStorage.getItem(`chat_session_${userId}`)
        const wsUrl = storedSid
            ? `${WS_BASE}/${userId}?session_id=${storedSid}`
            : `${WS_BASE}/${userId}`

        setStatus("connecting")
        const ws = new WebSocket(wsUrl)
        wsRef.current = ws

        ws.onopen = () => setStatus("connected")

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === "greeting") {
                sessionIdRef.current = data.session_id
                sessionStorage.setItem(`chat_session_${userId}`, data.session_id)
                setMessages((prev) => [...prev, { role: "assistant", text: data.response }])
                setWaiting(false)
            } else if (data.type === "history") {
                setMessages((prev) => [...prev, { role: data.role, text: data.text }])
            } else {
                setMessages((prev) => [...prev, { role: "assistant", text: data.response }])
                setWaiting(false)
            }
        }

        ws.onclose = () => {
            wsRef.current = null
            setStatus("error")
        }

        ws.onerror = () => ws.close()

        return () => {
            ws.close()
            wsRef.current = null
        }
    }, [userId])

    useEffect(() => {
        if (open) inputRef.current?.focus()
    }, [open])

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages, waiting])

    const sendMessage = () => {
        const text = input.trim()
        if (!text || status !== "connected" || waiting) return

        setMessages((prev) => [...prev, { role: "user", text }])
        wsRef.current.send(text)
        setInput("")
        setWaiting(true)
    }

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    const statusLabel = {
        idle: "Iniciando…",
        connecting: "Conectando…",
        connected: "En línea",
        error: "Sin conexión",
    }[status]

    const canType = status === "connected" && !waiting

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
            {open && (
                <div className="flex flex-col w-[90vw] max-w-[800px] h-[85vh] max-h-[800px] bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
                    {/* Header */}
                    <div className="flex items-center gap-3 px-4 py-3 bg-blue-600 text-white">
                        <div className="flex items-center justify-center w-8 h-8 bg-white/20 rounded-full shrink-0">
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="font-semibold text-sm leading-tight">Asistente CaixaBank</p>
                            <p className="text-[11px] text-blue-200 flex items-center gap-1">
                                <span className={`inline-block w-1.5 h-1.5 rounded-full ${
                                    status === "connected" ? "bg-emerald-400" :
                                    status === "error"     ? "bg-red-400" :
                                                            "bg-yellow-300 animate-pulse"
                                }`} />
                                {statusLabel}
                            </p>
                        </div>
                        <button
                            onClick={() => setOpen(false)}
                            className="p-1 rounded-lg hover:bg-white/20 transition-colors"
                            aria-label="Cerrar chat"
                        >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3 bg-gray-50">
                        {status === "connecting" && messages.length === 0 && (
                            <p className="text-center text-xs text-gray-400 mt-10">
                                Estableciendo conexión con el asistente…
                            </p>
                        )}

                        {status === "error" && (
                            <div className="mx-auto mt-10 text-center text-xs text-red-500 bg-red-50 border border-red-200 rounded-xl px-4 py-3">
                                No se pudo conectar con el asistente.<br />
                                Comprueba que el servidor esté activo.
                            </div>
                        )}

                        {status === "connected" && messages.length === 0 && !waiting && (
                            <p className="text-center text-xs text-gray-400 mt-10">
                                Pregúntame sobre tarjetas CaixaBank
                            </p>
                        )}

                        {messages.map((msg, i) => (
                            <div
                                key={i}
                                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                            >
                                <div
                                    className={`max-w-[82%] px-3 py-2 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                                        msg.role === "user"
                                            ? "bg-blue-600 text-white rounded-br-sm"
                                            : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm"
                                    }`}
                                >
                                    {msg.text}
                                </div>
                            </div>
                        ))}

                        {waiting && (
                            <div className="flex justify-start">
                                <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm">
                                    <span className="flex gap-1 items-center">
                                        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
                                    </span>
                                </div>
                            </div>
                        )}

                        <div ref={bottomRef} />
                    </div>

                    {/* Input */}
                    <div className="px-3 py-3 bg-white border-t border-gray-100 flex gap-2">
                        <input
                            ref={inputRef}
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={
                                status === "error"      ? "Sin conexión con el servidor" :
                                status !== "connected"  ? "Esperando conexión…" :
                                                         "Escribe tu mensaje…"
                            }
                            disabled={!canType}
                            className="flex-1 text-sm text-black px-3 py-2 border border-gray-200 rounded-xl bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 placeholder-gray-400"
                        />
                        <button
                            onClick={sendMessage}
                            disabled={!canType || !input.trim()}
                            className="p-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                            aria-label="Enviar"
                        >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                            </svg>
                        </button>
                    </div>
                </div>
            )}

            {/* Toggle button */}
            <button
                onClick={() => setOpen((v) => !v)}
                className="relative flex items-center justify-center w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition-all duration-200 hover:scale-105 active:scale-95"
                aria-label={open ? "Cerrar chat" : "Abrir chat"}
            >
                {!open && status === "connected" && (
                    <span className="absolute top-0.5 right-0.5 w-3 h-3 bg-emerald-400 border-2 border-white rounded-full" />
                )}
                {!open && status === "error" && (
                    <span className="absolute top-0.5 right-0.5 w-3 h-3 bg-red-400 border-2 border-white rounded-full" />
                )}

                {open ? (
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                ) : (
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                )}
            </button>
        </div>
    )
}
