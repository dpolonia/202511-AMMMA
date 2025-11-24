"""
Phase 6: Presentation Creation
Generate 8-slide, 15-minute presentation summarizing the paper.
"""

from pathlib import Path
import config
import utils

def load_paper_metadata():
    """Load selected paper metadata."""
    metadata_path = config.SELECTED_PAPER_DIR / "paper_metadata.json"
    try:
        return utils.load_json(metadata_path)
    except FileNotFoundError:
        print("❌ ERROR: paper_metadata.json not found!")
        return None

def load_paper_text():
    """Load paper text."""
    text_path = config.SELECTED_PAPER_DIR / "paper_text.txt"
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def generate_presentation(paper_metadata, paper_text) -> str:
    """Generate 8-slide presentation in markdown format."""
    
    presentation = f"""# {paper_metadata.get('title', 'Paper Presentation')}

**Presenter**: [Your Name]  
**Date**: [Presentation Date]  
**Class**: Multilevel and Mixed Methods Approaches

---

## Slide 1: Title & Context

### {paper_metadata.get('title', 'Title')}

**Authors**: {paper_metadata.get('authors', 'N/A')}

**Journal**: {paper_metadata.get('publication_name', 'N/A')} ({paper_metadata.get('cover_date', 'N/A')[:4] if paper_metadata.get('cover_date') != 'N/A' else 'N/A'})

**Citations**: {paper_metadata.get('cited_by_count', 0)}

**Context**: 
- Selected from {paper_metadata.get('grading', {}).get('total_score', 0)}/100 scoring system
- Strong multilevel and mixed methods approach
- Relevant to Value-Based Healthcare research

---

## Slide 2: Research Question & Objectives

### Research Question

*[Extract main research question from paper]*

### Objectives

1. *[Objective 1]*
2. *[Objective 2]*
3. *[Objective 3]*

### Significance

*[Why this research matters]*

**Note**: *This slide should be customized based on the actual paper content*

---

## Slide 3: Multilevel Analysis Approach

### Why Multilevel?

- Nested/hierarchical data structure
- Cross-level interactions
- Contextual effects

### Methodology

**Levels Analyzed**:
- Level 1: *[e.g., Individual patients]*
- Level 2: *[e.g., Healthcare providers]*
- Level 3: *[e.g., Hospitals/regions]*

**Statistical Approach**:
- Hierarchical Linear Modeling (HLM)
- Mixed-effects models
- Random intercepts/slopes

### Key Variables

- **Outcome**: *[Dependent variable]*
- **Predictors**: *[Independent variables at each level]*

---

## Slide 4: Mixed Methods Integration

### Qualitative Component

**Methods**:
- Interviews / Focus groups
- Thematic analysis
- Case studies

**Sample**: *[Qualitative sample details]*

### Quantitative Component

**Methods**:
- Survey / Administrative data
- Statistical analysis
- Sample size: *[N]*

### Integration Strategy

- **Convergent design**: Parallel collection and analysis
- **Triangulation**: Comparing qual/quant findings
- **Complementarity**: Qual explains quant patterns

---

## Slide 5: Key Findings

### Multilevel Results

1. **Within-level effects**:
   - *[Finding 1]*
   
2. **Cross-level interactions**:
   - *[Finding 2]*
   
3. **Variance explained**:
   - Level 1: *[%]*
   - Level 2: *[%]*

### Mixed Methods Insights

- **Quantitative**: *[Statistical findings]*
- **Qualitative**: *[Thematic findings]*
- **Integration**: *[How they complement each other]*

---

## Slide 6: Implications for VBHC

### Value-Based Healthcare Relevance

**Outcomes Focus**:
- *[How findings relate to patient outcomes]*

**Cost-Effectiveness**:
- *[Economic implications]*

**Quality Improvement**:
- *[Practice implications]*

### Health Systems Implications

- **Policy**: *[Policy recommendations]*
- **Practice**: *[Clinical/organizational changes]*
- **Research**: *[Future research directions]*

---

## Slide 7: Limitations & Future Research

### Methodological Limitations

1. **Multilevel approach**:
   - *[Limitation 1, e.g., sample size at higher levels]*
   - *[Limitation 2, e.g., cross-sectional design]*

2. **Mixed methods**:
   - *[Limitation 3, e.g., generalizability of qualitative findings]*

### Strengths

- Rigorous multilevel modeling
- Rich mixed methods integration
- Practical relevance

### Future Directions

1. *[Suggestion 1]*
2. *[Suggestion 2]*
3. *[Suggestion 3]*

---

## Slide 8: Discussion & Questions

### Key Takeaways

1. **Multilevel analysis** reveals *[key insight]*
2. **Mixed methods** provide *[complementary understanding]*
3. **VBHC implications**: *[practical application]*

### Critical Reflection

**Strengths of this approach**:
- Captures complexity of healthcare systems
- Integrates multiple perspectives

**Challenges**:
- Data requirements
- Analytical complexity

### Discussion Questions

1. How might this approach apply to other healthcare contexts?
2. What additional levels of analysis could be valuable?
3. How can we better integrate qualitative and quantitative findings?

**Thank you! Questions?**

---

## Presentation Notes

**Timing**: 15 minutes total
- Slides 1-2: 2 minutes (Introduction)
- Slides 3-4: 4 minutes (Methods)
- Slide 5: 3 minutes (Findings)
- Slide 6: 2 minutes (Implications)
- Slide 7: 2 minutes (Limitations)
- Slide 8: 2 minutes (Discussion)

**Tips**:
- Customize content based on actual paper
- Add visual aids (charts, diagrams) where appropriate
- Prepare examples to illustrate multilevel concepts
- Be ready to explain integration of qual/quant methods
"""
    
    return presentation

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 6: PRESENTATION CREATION")
    print("="*60)
    
    # Load paper metadata
    paper_metadata = load_paper_metadata()
    if not paper_metadata:
        return False
    
    # Load paper text
    paper_text = load_paper_text()
    
    # Generate presentation
    print("\nGenerating presentation...")
    presentation = generate_presentation(paper_metadata, paper_text)
    
    # Save presentation
    output_path = config.OUTPUT_FILES['presentation']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(presentation)
    
    print(f"✓ Presentation generated: {output_path}")
    
    print("\n" + "="*60)
    print("✓ PHASE 6 COMPLETE")
    print("="*60)
    print(f"\nPresentation saved to: {output_path.name}")
    print("\n8 slides created for 15-minute presentation")
    print("\n⚠ IMPORTANT: Customize the presentation with actual paper content")
    print("The current version contains placeholders that need to be filled in")
    
    return True

if __name__ == "__main__":
    main()
