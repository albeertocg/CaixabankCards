# Sistema de Diseño — CaixaBank Cards

## Paleta de Colores

### Primarios (marca CaixaBank)
| Token | Hex | Uso |
|-------|-----|-----|
| `caixa-teal` | `#007EAE` | Acciones principales, links, botones primarios |
| `caixa-dark` | `#1A1A2E` | Textos principales, headers |
| `caixa-star` | `#40BFE8` | Acento de marca (estrella del logo), highlights |

### Neutros
| Token | Hex | Uso |
|-------|-----|-----|
| `gray-50` | `#F8FAFC` | Fondo de página |
| `gray-100` | `#F1F5F9` | Fondo de secciones, cards |
| `gray-200` | `#E2E8F0` | Bordes, separadores |
| `gray-400` | `#94A3B8` | Texto secundario, placeholders |
| `gray-600` | `#475569` | Texto de cuerpo |
| `gray-900` | `#0F172A` | Texto principal |

### Semánticos
| Token | Hex | Uso |
|-------|-----|-----|
| `success` | `#059669` | Confirmaciones, elegible |
| `warning` | `#D97706` | Alertas, atención |
| `error` | `#DC2626` | Errores, no elegible |

## Tipografía

- **Font family**: Geist Sans (ya configurada en layout.js)
- **Headings**: `font-semibold` o `font-bold`, nunca `font-black`
- **Body**: `text-sm` (14px) o `text-base` (16px)
- **Captions/labels**: `text-xs` (12px)
- Interlineado: `leading-relaxed` para cuerpo, `leading-tight` para headings

## Espaciado

- Padding de página: `px-6 py-8` (mobile), `px-8 py-12` (desktop)
- Gap entre secciones: `gap-8` o `gap-12`
- Padding de cards: `p-6`
- Padding de botones: `px-5 py-2.5`

## Componentes

### Botón primario
```
bg-[#007EAE] hover:bg-[#006490] text-white font-medium px-5 py-2.5 rounded-xl transition-colors
```

### Botón secundario
```
border border-gray-200 text-gray-700 hover:bg-gray-50 font-medium px-5 py-2.5 rounded-xl transition-colors
```

### Card
```
bg-white rounded-2xl border border-gray-200 shadow-sm p-6
```

### Input
```
w-full px-4 py-2.5 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-400
focus:outline-none focus:ring-2 focus:ring-[#007EAE]/30 focus:border-[#007EAE] transition-colors
```

## Layout

- Max width contenido: `max-w-6xl mx-auto`
- Fondo de página: `bg-gray-50` (no blanco puro)
- Sin modo oscuro (no es necesario para esta aplicación bancaria)
- Responsive: mobile-first con breakpoints `sm:`, `md:`, `lg:`

## Iconografía

- Solo SVG inline (no icon libraries)
- Tamaño estándar: `w-5 h-5` en UI, `w-8 h-8` en features
- Stroke width: 1.5 o 2

## Logos

- Logo principal: `/images/caixabank.png` (horizontal, para header)
- Placeholder para favicon y logo cuadrado: preparar slot en layout.js
- No usar logos por defecto de Next.js ni Vercel

## Principios

1. **Limpio**: mucho espacio en blanco, sin saturar
2. **Profesional**: aspecto bancario, transmitir confianza
3. **Directo**: CTAs claros, sin pasos innecesarios
4. **Consistente**: mismos radios, colores y espacios en toda la app
