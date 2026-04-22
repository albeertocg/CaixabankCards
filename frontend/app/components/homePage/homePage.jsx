"use client"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen w-full bg-[#F8FAFC]">

      <header className="w-full bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <img
            src="/images/caixabank.png"
            alt="CaixaBank"
            className="h-14"
          />
          <Link
            href="/login"
            className="bg-[#007EAE] hover:bg-[#006490] text-white font-medium px-5 py-2.5 rounded-xl transition-colors text-sm"
          >
            Iniciar sesión
          </Link>
        </div>
      </header>

      <section className="flex-grow flex items-center px-6 py-16 md:py-24">
        <div className="max-w-6xl mx-auto w-full">
          <div className="max-w-2xl">
            <span className="inline-block text-[#007EAE] text-sm font-medium tracking-wide uppercase mb-4">
              Gestión de tarjetas
            </span>
            <h1 className="text-4xl md:text-5xl font-semibold text-[#1A1A2E] leading-tight mb-6">
              Tus tarjetas,<br />
              <span className="text-[#007EAE]">bajo control.</span>
            </h1>
            <p className="text-gray-600 text-base leading-relaxed mb-8 max-w-xl">
              Consulta tus tarjetas, recibe recomendaciones personalizadas y gestiona tus finanzas con la seguridad que mereces.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/login"
                className="bg-[#007EAE] hover:bg-[#006490] text-white font-medium px-5 py-2.5 rounded-xl transition-colors text-sm text-center"
              >
                Acceder a mi cuenta
              </Link>
              <a
                href="#beneficios"
                className="border border-gray-200 text-gray-700 hover:bg-gray-100 font-medium px-5 py-2.5 rounded-xl transition-colors text-sm text-center"
              >
                Conocer más
              </a>
            </div>
          </div>
        </div>
      </section>

      <div className="border-t border-gray-200" />

      <section id="beneficios" className="px-6 py-16 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-semibold text-[#1A1A2E] leading-tight mb-3">
              Diseñado para simplificar tu banca
            </h2>
            <p className="text-gray-500 text-sm leading-relaxed max-w-md mx-auto">
              Todo lo que necesitas para gestionar tus tarjetas en un solo lugar.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
              <div className="w-10 h-10 bg-[#007EAE]/10 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-5 h-5 text-[#007EAE]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3v-3z" />
                </svg>
              </div>
              <h3 className="text-[#1A1A2E] font-semibold text-base mb-2">Asesor inteligente</h3>
              <p className="text-gray-500 text-sm leading-relaxed">
                Chatea con nuestro asistente para obtener recomendaciones personalizadas según tu perfil financiero.
              </p>
            </div>

            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
              <div className="w-10 h-10 bg-[#40BFE8]/10 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-5 h-5 text-[#40BFE8]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
                  <line x1="1" y1="10" x2="23" y2="10" />
                </svg>
              </div>
              <h3 className="text-[#1A1A2E] font-semibold text-base mb-2">Tarjetas para ti</h3>
              <p className="text-gray-500 text-sm leading-relaxed">
                Visualiza todas tus tarjetas activas, sus límites y movimientos recientes en una vista clara y ordenada.
              </p>
            </div>

            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
              <div className="w-10 h-10 bg-[#059669]/10 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-5 h-5 text-[#059669]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
              </div>
              <h3 className="text-[#1A1A2E] font-semibold text-base mb-2">Seguridad garantizada</h3>
              <p className="text-gray-500 text-sm leading-relaxed">
                Tus datos están protegidos con los estándares de seguridad más exigentes del sector bancario europeo.
              </p>
            </div>

          </div>
        </div>
      </section>

      <footer className="bg-white border-t border-gray-200 px-6 py-6">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-gray-400 text-xs">
            © 2026 CaixaBank, S.A. Todos los derechos reservados.
          </p>
          <div className="flex items-center gap-5">
            <a href="#" className="text-gray-400 hover:text-[#007EAE] text-xs transition-colors">
              Aviso legal
            </a>
            <a href="#" className="text-gray-400 hover:text-[#007EAE] text-xs transition-colors">
              Política de cookies
            </a>
            <a href="#" className="text-gray-400 hover:text-[#007EAE] text-xs transition-colors">
              Política de privacidad
            </a>
          </div>
        </div>
      </footer>

    </div>
  )
}
