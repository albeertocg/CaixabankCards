---
name: git-commit
description: Use when creating git commits, before writing any commit message - enforces project commit conventions including Spanish language, imperative mood, and conventional commit types
---

# Git Commit

## Overview

All commit messages in this project MUST be written in Spanish following conventional commit format.

## Format

```
[tipo]: descripcion breve en minusculas
```

Optional body after blank line (max 72 chars per line).

## Types

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Correccion de bug |
| `docs` | Cambios de documentacion |
| `style` | Cambios de formato/linting |
| `refactor` | Reorganizacion de codigo |
| `test` | Agregar/actualizar tests |
| `chore` | Configuracion, dependencias |

## Rules

- Spanish. Always.
- Present imperative ("agregar", not "agregado" or "agrega")
- First line: max 50 characters
- Focus on "what" and "why", not "how"
- Atomic commits: one logical change per commit

## Examples

```
feat: agregar validacion de tarjetas
fix: corregir calculo de comisiones
docs: actualizar guia de contribucion
refactor: extraer logica de autenticacion a servicio
test: agregar tests para endpoint de tarjetas
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| English message | Translate to Spanish |
| Past tense ("agregado") | Use imperative ("agregar") |
| Vague ("cambios varios") | Be specific ("agregar validacion de email") |
| Too long first line | Keep under 50 chars |
| Multiple changes in one commit | Split into atomic commits |
