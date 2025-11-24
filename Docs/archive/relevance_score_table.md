# Relevance Score Calculation

The relevance score used to rank the top‑10 articles is based on a set of weighted factors. Each factor contributes a fixed number of points (or a weighted contribution) to the total score.

| Factor | Description | Weight (Points) |
|--------|-------------|-----------------|
| **Multilevel** | Presence of terms *multilevel*, *multi‑level*, *hierarchical linear*, or *nested model* in title/abstract | 10 |
| **Hierarchical (fallback)** | Presence of term *hierarchical* (when the above specific terms are absent) | 5 |
| **Mixed Methods** | Explicit mention of *mixed method* in title/abstract | 10 |
| **Qualitative + Quantitative** | Both *qualitative* and *quantitative* appear (when *mixed method* is not found) | 5 |
| **VBHC / Value‑Based** | Presence of *VBHC* or *value‑based* in title/abstract | 5 |
| **Portugal relevance** | Presence of *Portugal* or *Portuguese* in title/abstract | 5 |
| **NHS relevance (fallback)** | Presence of *NHS* when Portugal terms are absent | 3 |
| **Citations** | 0.5 points per citation, capped at 10 citations (max 5 points) | ≤ 5 |

**Total Score** = Sum of all applicable weights (maximum possible ≈ 45 points). The script caps the citation contribution at 5 points to avoid over‑weighting highly cited but less relevant papers.

*The table is used by `enhance_analysis.py` (function `parse_ris_top_10`) to compute the `Relevance Score` column shown in the reports.*
