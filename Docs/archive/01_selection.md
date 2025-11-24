# SCOPUS Search Keyword Evaluation

**Objective:** Find a paper for a "Multilevel and Mixed Methods" class that aligns with a PhD on VBHC in Beveridgean systems (Portugal).

## 1. Evaluation of Current String
**Query:** `"mixed methods" AND (VBHC and health*)`

| Component | Status | Critique |
| :--- | :--- | :--- |
| `"mixed methods"` | ✅ **Strong** | Correctly quotes the specific methodological term. Essential for the class. |
| `VBHC` | ⚠️ **Risky** | Using only the acronym is dangerous. Many papers use the full term "Value-Based Healthcare" or "Value Based Health Care" without the acronym in the title/abstract. |
| `health*` | ⚠️ **Redundant** | "VBHC" already implies health. If you expand VBHC correctly, this becomes unnecessary noise. |
| **(Missing)** | ❌ **Critical** | The class is explicitly about **Multilevel** modeling/methods. Your current string does not filter for this, meaning you will mostly find general mixed methods papers, not multilevel ones. |

## 2. Recommendations

### Option A: The "Class Compliant" Search (Recommended)
This targets the specific intersection of the class topic (Multilevel + Mixed Methods) and your research area.
```text
"mixed methods" AND ("multilevel" OR "multi-level" OR "hierarchical") AND ("VBHC" OR "value based health*")
```

### Option B: The "PhD Context" Search
If you want to prioritize the Portuguese/Beveridgean context over the "multilevel" keyword (risking less relevance to the specific class module):
```text
"mixed methods" AND ("VBHC" OR "value based health*") AND ("Portugal" OR "National Health Service" OR "NHS")
```

### Option C: Broad Search (High Recall)
Use this if Option A yields too few results. It fixes the acronym issue but remains broad.
```text
"mixed methods" AND ("VBHC" OR "value based health*")
```

## 3. Search Tips
*   **Multilevel Keywords:** If "multilevel" is too restrictive, try adding terms that imply nested data structures often used in multilevel modeling, such as `"nested"`, `"cluster"`, or `"hierarchical linear model"`.
*   **Spelling:** "Value-based" is often hyphenated. Using `value based health*` (without quotes or with wildcards depending on the exact database, but SCOPUS handles loose phrases well) or `"value-based healthcare"` is safer than just VBHC.

> **Note:** I analyzed the class document `20241212 SCEE I - AMMMMA.pdf`. The document title **"Multilevel and Mixed Methods Approaches"** and references to "Multi-level Issues" (Yammarino & Dansereau) explicitly confirm that **Multilevel Analysis** is a core requirement. A search string without "multilevel" (or related terms) will likely fail to meet the assignment criteria.
