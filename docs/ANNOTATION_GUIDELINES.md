# Wound & Tissue Annotation Guidelines

These guidelines define the semantic labeling protocol for diabetic foot ulcer images to ensure clinical validity and inter-annotator reliability.

---

## 1. Outer Wound Boundary Segmentation

- **Definition**: The outer perimeter separating epithelialized periwound skin from the open wound bed.
- **Inclusions**: Include all active granulation tissue, fibrinous slough, necrotic eschar, and exposed subcutaneous structures.
- **Exclusions**: Do not include intact periwound hyperkeratosis (callus) or surrounding erythema within the wound boundary. Callus must be recorded separately if evaluated.
- **Ambiguous Margins**: Where macerated or rolling edges (epibole) occur, annotate along the innermost non-epithelialized margin and tag with uncertainty flag.

---

## 2. Tissue Composition Classes (Multi-Class Sub-Segmentation)

1. **Granulation Tissue (Class 1 - Red)**:
   - Viable, highly vascularized connective tissue characterized by a healthy, granular, bright or deep red surface.
2. **Slough Tissue (Class 2 - Yellow/Cream)**:
   - Non-viable subcutaneous tissue, proteinaceous matrix, fibrin, and cellular debris. Typically stringy, moist, yellow, cream, or greyish.
3. **Necrotic Eschar (Class 3 - Black/Dark Brown)**:
   - Non-viable devitalized dry or leathery tissue covering the wound base.

---

## 3. Scale Calibration Reference Annotation

- When automated circular marker detection is ambiguous, annotators define 4 points across the circular diameter ($10.0\text{ mm}$ reference) or a calibrated ruler span to establish millimeter scale calibration.
