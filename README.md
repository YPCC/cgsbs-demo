# Context-Guided Semantic Beam Search (CGSBS) — Synthetic Demo

End-to-end demonstration of **Context-Guided Semantic Beam Search for Patient-Specific Subgraph Retrieval from Biomedical Ontologies**.

Synthetic multi-ontology RDF (SNOMED-like + RxNorm-like + LOINC-like) so the algorithm runs immediately. Real BioPortal / UMLS dumps and GraphDB can be swapped in via config without changing algorithm code.

**Repository:** https://github.com/YPCC/cgsbs-demo

## Exact scoring function (paper Section 10)

```text
S(u, r, P, C) = α·S_ctx + β·S_rel + γ·S_UMLS-rel + δ·S_UMLS-sim
              + ε·S_type + ζ·S_path + η·S_prov − λ·D(P)
```

Implemented in `src/cgsbs/scoring.py` → `compute_score(...)`.

## Quick Start

```bash
git clone https://github.com/YPCC/cgsbs-demo.git
cd cgsbs-demo
python -m venv .venv && source .venv/bin/activate
pip install -e .
make demo                  # renal + metformin context
make demo-vision           # same T2DM anchor, ophthalmic context
make demo-all
```

## Configurable backends (`config/default.yaml`)

| Roadmap item | Config key | Options |
|---|---|---|
| Real data | `ontology.source` | synthetic \| local_rdf \| bioportal |
| GraphDB | `graph.backend` | rdflib \| graphdb |
| UMLS measures | `similarity.backend` | synthetic \| umls \| embeddings |
| NLP | `context.extractor` | deterministic \| scispacy \| bioportal_annotator \| llm |

```bash
pip install -e ".[graphdb,nlp,umls]"
python -m cgsbs.demo --config config/my_prod.yaml --note note_renal_metformin
```

## Layout

```
cgsbs-demo/
├── config/default.yaml          # switch backends here
├── data/synthetic/              # demo ontology + notes
├── src/cgsbs/
│   ├── scoring.py               # exact S(u,r,P,C)
│   ├── beam_search.py           # multi-anchor CGSBS
│   ├── envelope.py              # Ontology Envelope
│   ├── context.py               # Patient Context Graph
│   ├── demo.py
│   └── backends/                # GraphDB, UMLS, NLP plugins
├── Makefile
└── pyproject.toml
```

## License

MIT. Synthetic RDF is original. Real SNOMED CT / UMLS data requires separate licenses.
