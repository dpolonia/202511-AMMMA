# LLM Model Options for Paper Analysis (Updated November 2025)

## Available Models (Based on API Keys in `.env`)

### 1. Anthropic Claude

| Model | Cost (Input/Output per 1M tokens) | Context Window | Suitability for Task |
|-------|-----------------------------------|----------------|---------------------|
| **Claude Opus 4.1** | $15 / $75 | 200K tokens | ⭐⭐⭐⭐⭐ **Excellent** - Most powerful Claude, best for complex reasoning |
| **Claude Sonnet 4.5** | $3 / $15 | 200K (1M with beta)¹ | ⭐⭐⭐⭐⭐ **Excellent** - Best for coding/agents, most aligned frontier model |
| **Claude Haiku 4.5** | $0.25 / $1.25 | 200K tokens | ⭐⭐⭐⭐ Very Good - Fast, cost-efficient, near-frontier quality |
| Claude Sonnet 4 | $3 / $15 | 200K tokens | ⭐⭐⭐⭐ Very Good - Solid performance, superseded by 4.5 |

¹ *Claude Sonnet 4.5 supports 1M token context with `context-1m-2025-08-07` beta header. Long context pricing ($5/$25 per 1M tokens) applies beyond 200K.*

**Recommended Use**:
- **Development LLM**: Claude Sonnet 4.5 (best for academic analysis and coding)
- **Devil's Advocate**: Claude Haiku 4.5 (cost-effective, high quality)

---

### 2. OpenAI GPT

| Model | Cost (Input/Output per 1M tokens) | Context Window | Suitability for Task |
|-------|-----------------------------------|----------------|---------------------|
| **GPT-5.1** | $1.25 / $10 | 400K tokens | ⭐⭐⭐⭐⭐ **Excellent** - Flagship for coding/agentic tasks, configurable reasoning |
| **GPT-5 mini** | $0.25 / $2 | 128K tokens | ⭐⭐⭐⭐⭐ **Excellent** - Fast, cost-efficient, excellent for well-defined tasks |
| **GPT-5 nano** | $0.05 / $0.40 | 128K tokens | ⭐⭐⭐⭐ Very Good - Ultra-cheap, great for summarization/classification |
| **GPT-4.1** | $2.50 / $10 | 128K tokens | ⭐⭐⭐⭐ Very Good - Advanced programming, large context handling |
| **GPT-4.1 mini** | $0.15 / $0.60 | 128K tokens | ⭐⭐⭐⭐ Very Good - Faster, more economical variant |
| **o1** | $15 / $60 | 200K tokens | ⭐⭐⭐⭐ Very Good - Deep reasoning for complex problems (slower) |
| **o1-mini** | $1.10 / $4.40 | 128K tokens | ⭐⭐⭐ Good - Cost-effective reasoning for STEM tasks |

**Recommended Use**:
- **Development LLM**: GPT-5.1 or GPT-5 mini (best balance)
- **Devil's Advocate**: GPT-5 nano (ultra-cheap, still capable)

---

### 3. Google Gemini

| Model | Cost (Input/Output per 1M tokens) | Context Window | Suitability for Task |
|-------|-----------------------------------|----------------|---------------------|
| **Gemini 3.0 Pro** | $2 / $12 (≤200K)<br>$4 / $18 (>200K) | 1M tokens | ⭐⭐⭐⭐⭐ **Excellent** - Best multimodal, "Deep Think" mode, agentic capabilities |
| **Gemini 2.5 Pro** | $1.25 / $10 (≤200K)<br>$2.50 / $15 (>200K) | 1M tokens | ⭐⭐⭐⭐⭐ **Excellent** - Advanced reasoning, massive context |
| **Gemini 2.5 Flash** | $0.15 / $0.60 (standard)<br>$0.15 / $3.50 (thinking mode) | 1M tokens | ⭐⭐⭐⭐⭐ **Excellent** - Best price-performance |
| Gemini 2.5 Flash-Lite | $0.10 / $0.40 | 1M tokens | ⭐⭐⭐⭐ Very Good - Ultra-cheap |

**Note**: Gemini 3.0 Pro is in preview. Stable pricing expected early 2026 at ~$1.50/$10 (≤200K) and $3/$15 (>200K).

**Recommended Use**:
- **Development LLM**: Gemini 3.0 Pro or 2.5 Pro (massive context, best for long papers)
- **Devil's Advocate**: Gemini 2.5 Flash (excellent price-performance, thinking mode)

---

### 4. xAI Grok

| Model | Cost (Input/Output per 1M tokens) | Context Window | Suitability for Task |
|-------|-----------------------------------|----------------|---------------------|
| **Grok 4.1** | $3 / $15 | 128K tokens | ⭐⭐⭐⭐ Very Good - Latest model, improved reasoning |
| **Grok 4.1 Fast** | $0.20-$0.40 / $0.50-$1.00² | 2M tokens | ⭐⭐⭐⭐⭐ **Excellent** - Massive context, optimized for tool-calling |
| **Grok 4** | $3 / $15 | 256K tokens | ⭐⭐⭐⭐ Very Good - Strong reasoning, real-time events |
| Grok 3 | $3 / $15 | 128K tokens | ⭐⭐⭐ Good - Older generation |
| Grok 3 mini | $0.30 / $0.50 | 128K tokens | ⭐⭐⭐ Good - Budget option |

² *Pricing varies by input size: $0.20/$0.50 for <128K tokens, $0.40/$1.00 for ≥128K tokens*

**Recommended Use**:
- **Development LLM**: Grok 4.1 (competitive pricing, good reasoning)
- **Devil's Advocate**: Grok 4.1 Fast (very cheap, huge 2M context)

---

## Cost Estimates for This Workflow

### Estimated Token Usage per Paper:
- **Paper text**: ~20K tokens
- **Evaluation questions**: ~5K tokens
- **Phase 4 (Initial answers)**: ~30K input, ~10K output
- **Phase 4.5 (2 adversarial rounds)**: ~80K input, ~30K output
- **Total per paper**: ~110K input, ~40K output

### Cost Comparison by Model Combination:

| Development LLM | Devil's Advocate | Total Cost per Paper | Quality Rating |
|-----------------|------------------|---------------------|----------------|
| **GPT-5 mini** | **GPT-5 nano** | **$0.04** | ⭐⭐⭐⭐⭐ |
| **Gemini 2.5 Pro** | **Gemini 2.5 Flash** | **$0.16** | ⭐⭐⭐⭐⭐ |
| **GPT-5.1** | **GPT-5 nano** | **$0.16** | ⭐⭐⭐⭐⭐ |
| Gemini 3.0 Pro | Gemini 2.5 Flash | $0.26 | ⭐⭐⭐⭐⭐ |
| GPT-5.1 | GPT-5 mini | $0.22 | ⭐⭐⭐⭐⭐ |
| Grok 4.1 | Grok 4.1 Fast | $0.35 | ⭐⭐⭐⭐⭐ |
| Claude Sonnet 4.5 | Claude Haiku 4.5 | $0.38 | ⭐⭐⭐⭐⭐ |

---

## Recommendations

### 🏆 **Best Overall (Cost)**: GPT-5 mini + GPT-5 nano
- **Cost**: $0.04 per paper (cheapest!)
- **Pros**: Extremely affordable, excellent quality, fast
- **Cons**: Smaller context (128K vs 1M for Gemini)

### 🚀 **Best Overall (Quality)**: GPT-5.1 + GPT-5 nano
- **Cost**: $0.16 per paper
- **Pros**: Flagship model, 400K context, configurable reasoning, ultra-cheap devil's advocate
- **Cons**: None significant

### 💎 **Best for Long Papers**: Gemini 2.5 Pro + Gemini 2.5 Flash
- **Cost**: $0.16 per paper
- **Pros**: 1M token context window, excellent for very long papers
- **Cons**: None significant

### 🎭 **Best Diversity**: GPT-5.1 + Gemini 2.5 Flash
- **Cost**: $0.16 per paper
- **Pros**: Different model families = diverse perspectives
- **Cons**: Requires two API providers

### 🔬 **Best for Complex Reasoning**: Claude Sonnet 4.5 + Claude Haiku 4.5
- **Cost**: $0.38 per paper
- **Pros**: Most aligned frontier model, excellent for academic work
- **Cons**: More expensive

---

## Special Features

### GPT-5.1 Configurable Reasoning
- "none" reasoning mode for fast responses
- High reasoning effort for complex tasks
- 400K token input context, 128K output
- Specialized `gpt-5.1-codex` variant for coding

### Gemini 3.0 Pro "Deep Think" Mode
- Evaluates multiple possibilities
- Checks own logic before responding
- Adjustable thinking levels
- Optimized for academic analysis

### Gemini 2.5 Flash "Thinking Mode"
- $3.50/1M output tokens (vs $0.60 standard)
- Toggle per request
- Good for complex critique

### Grok 4.1 Fast
- 2M token context window (largest available)
- Optimized for agentic tool-calling
- Tiered pricing based on input size

### Claude Sonnet 4.5 Extended Context
- 1M token context with beta header
- Higher pricing ($5/$25 per 1M) beyond 200K
- Most aligned frontier model

---

## Final Recommendation for This Task

**Development LLM**: **GPT-5.1** or **Gemini 2.5 Pro**
- GPT-5.1: Best overall, 400K context, configurable reasoning
- Gemini 2.5 Pro: Best for very long papers (1M context), slightly cheaper

**Devil's Advocate**: **GPT-5 nano** or **Gemini 2.5 Flash**
- GPT-5 nano: Ultra-cheap ($0.05/$0.40), still capable
- Gemini 2.5 Flash: Thinking mode available, excellent quality

**Optimal Combination**: **GPT-5.1 + GPT-5 nano** ($0.16/paper)
- Best balance of quality, cost, and features
- 400K context sufficient for academic papers
- Configurable reasoning for complex analysis
