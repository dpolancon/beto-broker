# Original Research — AI Big Short / Investigación Original — Big Short de IA

> **EN** — Four research reports that form the intellectual foundation of the `beto-broker` system. Each report is available in its original Spanish (`_es`) and a full English translation (`_en`). Read these before `PROMPT.md` to understand *why* the system is built the way it is.
>
> **ES** — Cuatro reportes de investigación que forman la base intelectual del sistema `beto-broker`. Cada reporte está disponible en su español original (`_es`) y una traducción completa al inglés (`_en`). Léelos antes de `PROMPT.md` para entender *por qué* el sistema está construido como está.

---

## Report 1 · Reporte 1

### BigShort v1 — System Architecture / Arquitectura del Sistema

| | |
|---|---|
| 🇬🇧 **EN** | [deep-research-report_BigShort_v1_en.md](./deep-research-report_BigShort_v1_en.md) |
| 🇪🇸 **ES** | [deep-research-report_BigShort_v1_es.md](./deep-research-report_BigShort_v1_es.md) |

**EN thesis:** A global real-time market monitoring and execution system is always two coupled systems — a low-latency data pipeline and a risk-controlled execution plane — and the bottleneck is almost never the model but correct data engineering and operational discipline.

**Tesis ES:** Un sistema de monitoreo y ejecución bursátil en tiempo real es siempre dos sistemas acoplados — una tubería de datos de baja latencia y un plano de ejecución con control de riesgo — y el cuello de botella casi nunca es el modelo sino la ingeniería de datos correcta y la disciplina operativa.

---

## Report 2 · Reporte 2

### BigShort v2 — AI Bubble Short Thesis / Tesis del Big Short contra la Burbuja de IA

| | |
|---|---|
| 🇬🇧 **EN** | [deep-research-report_BigShort_v2_en.md](./deep-research-report_BigShort_v2_en.md) |
| 🇪🇸 **ES** | [deep-research-report_BigShort_v2_es.md](./deep-research-report_BigShort_v2_es.md) |

**EN thesis:** Shorting the AI narrative is not a single trade but a portfolio of instruments with bounded-loss structures (puts, spreads, pairs) governed by a risk engine that must survive a market that stays irrational longer than your margin — and the winning edge comes from a quantitative vulnerability score (EV/Sales, P/FCF, AI exposure, short interest, borrow fee, IV skew) applied to a curated asset basket.

**Tesis ES:** Apostar a la baja en la narrativa de IA no es una sola operación sino un portafolio de instrumentos con pérdida acotada (puts, spreads, pares) gobernado por un motor de riesgo que debe sobrevivir a que el mercado siga irracional más tiempo que tu margen — y la ventaja ganadora viene de un score cuantitativo de vulnerabilidad (EV/Sales, P/FCF, exposición IA, short interest, borrow fee, IV skew) aplicado a una canasta de activos curada.

---

## Report 3 · Reporte 3

### BigShort v3 — Bounded-Loss Deployment Blueprint / Plano de Despliegue con Pérdida Acotada

| | |
|---|---|
| 🇬🇧 **EN** | [deep-research-report_BigShort_v3_en.md](./deep-research-report_BigShort_v3_en.md) |
| 🇪🇸 **ES** | [deep-research-report_BigShort_v3_es.md](./deep-research-report_BigShort_v3_es.md) |

**EN thesis:** A fast, bounded-loss big short against the AI bubble can be deployed in 8–12 weeks using a convexity-controlled program of puts and debit put spreads — with the asset universe divided into four buckets (semiconductors, hyperscalers, high-beta software, ETF benchmarks) scored by a MAD-robust quantitative model and sized to equalize variance contribution across positions.

**Tesis ES:** Un big short rápido y con pérdida acotada contra la burbuja de IA puede desplegarse en 8–12 semanas usando un programa de convexidad controlada de puts y debit put spreads — con el universo de activos dividido en cuatro buckets (semiconductores, hyperscalers, software de alta beta, ETFs de referencia) puntuados por un modelo cuantitativo robusto por MAD y dimensionados para igualar la contribución de varianza entre posiciones.

---

## Report 4 · Reporte 4

### Short-Run Strategy — Supervised ML with Social Sentiment / Estrategia de Corto Plazo con ML Supervisado y Sentimiento Social

| | |
|---|---|
| 🇬🇧 **EN** | [deep-research-report-Short-Run-Strategy_en.md](./deep-research-report-Short-Run-Strategy_en.md) |
| 🇪🇸 **ES** | [deep-research-report-Short-Run-Strategy_es.md](./deep-research-report-Short-Run-Strategy_es.md) |

**EN thesis:** A very short-term algorithmic trading strategy can be built by combining real-time social sentiment signals (X/Twitter NLP, social network analysis, finfluencer PageRank) with classical technical indicators in a supervised ML model — provided the system operates under continuous human supervision with an immediate kill switch, since no model alone survives herd-driven market dynamics.

**Tesis ES:** Una estrategia algorítmica de muy corto plazo puede construirse combinando señales de sentimiento social en tiempo real (NLP de X/Twitter, análisis de redes sociales, PageRank de finfluencers) con indicadores técnicos clásicos en un modelo ML supervisado — siempre que el sistema opere bajo supervisión humana continua con un kill switch inmediato, ya que ningún modelo por sí solo sobrevive a las dinámicas de mercado impulsadas por manada.

---

## Reading order · Orden de lectura

```
R1 (architecture) → R2 (thesis + instruments) → R3 (deployment blueprint) → R4 (ML sentiment layer)
```

These reports are research priors — they are the *inputs* to the system, not outputs of it. The vault nodes in `../vault/examples/ai-bubble-short/` operationalize what these reports define.

---

*Traceability: see [GitHub Issue #1](https://github.com/dpolancon/beto-broker/issues/1) for a full mapping of every vault node back to the specific report section that sourced it.*
