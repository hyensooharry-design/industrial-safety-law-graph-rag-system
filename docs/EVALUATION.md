# Manuscript Evaluation

This page summarizes the evaluation reported in the manuscript **Knowledge Graph-Based Legal Chain Reasoning for Industrial Safety Decision Support**.

## Evaluation objective

The evaluation tests whether the Legal Graph-RAG framework can reconstruct case-relevant legal evidence as a connected evidence structure rather than merely retrieve one matching article.

The manuscript evaluates both:

1. **Case-based Legal Bundle reconstruction**
2. **Evidence Pack, Legal Chain, source traceability, and citation-oriented answer generation**

## Case-scenario dataset

A total of **42 industrial-safety legal scenarios** are used in the final manuscript evaluation.

| Type | Cases | Purpose |
|---|---:|---|
| Criminal precedent-based | 33 | Occupational accidents and criminal-liability-related cases |
| Administrative adjudication-based | 9 | Prevention, administrative fines, and administrative-disposition-related cases |
| **Total** | **42** | Industrial-safety case-based legal scenarios |

The ground-truth structure is a **Legal Bundle**, not a single article. Depending on the case, the bundle can include primary obligations, health obligations, contractor obligations, Serious Accidents Punishment Act obligations, detailed rules, criminal penalties, corporate liability, administrative consequences, and supporting evidence.

## Reported main results

The manuscript evaluates direct legal-reference selection at three statutory reference levels.

| Reference level | F1-score |
|---|---:|
| Article | **0.737** |
| Paragraph | **0.715** |
| Subparagraph / Item | **0.607** |

The manuscript reports that the proposed framework achieved the highest direct-selection F1 among the compared methods at these three levels. The proposed method reduced unnecessary legal references and improved precision, while broader role-based retrieval showed higher recall with more false positives.

## Repository artifacts

The `evaluation/` directory retains the public case-scenario evaluation workspace, including dataset construction, extraction, mapping, reviewed results, ablation/development outputs, and reports.

The broader raw source-case collection is stored separately under:

```text
data/raw_cases/
```

The raw source inventory is larger than the 42-case final manuscript evaluation set. This distinction is intentional: the manuscript reports results on the final 42-case evaluation set, while the repository retains broader public artifacts used during dataset construction and validation.

## Current limitations reported in the manuscript

- The final evaluation set contains 42 scenarios and therefore does not establish generalization across all industrial-safety legal situations.
- Internal evidence selection and Legal Chain construction remain relatively article-centered.
- Ranking weights are heuristic and were not subjected to a systematic sensitivity analysis.
- Old-to-current statutory article mapping can contain ambiguity when statutes are revised.
- Future work should expand citation-accuracy and faithfulness evaluation and improve fine-grained article/paragraph/subparagraph alignment.

## Publication metadata

Any publication-specific replication label, final table/figure numbering, DOI-linked artifact version, and final citation will be added upon publication.
