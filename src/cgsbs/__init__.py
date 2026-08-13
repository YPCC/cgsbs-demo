"""
Context-Guided Semantic Beam Search (CGSBS)

Patient-specific subgraph retrieval from biomedical ontologies.
"""

__version__ = "0.1.0-synthetic"

from .scoring import ScoringWeights as ScoringWeights
from .scoring import compute_score as compute_score
from .scoring import PatientContext as PatientContext
from .envelope import load_ontology as load_ontology
from .envelope import build_envelope as build_envelope
from .beam_search import context_guided_beam_search as context_guided_beam_search
from .context import extract_patient_context as extract_patient_context
from .backends.factory import build_from_config as build_from_config

__all__ = [
    "ScoringWeights",
    "compute_score",
    "PatientContext",
    "load_ontology",
    "build_envelope",
    "context_guided_beam_search",
    "extract_patient_context",
    "build_from_config",
]
