"""Pluggable backends for ontology data, graph engine, similarity, and NLP."""

from .base import GraphBackend, SimilarityProvider, ContextExtractor
from .factory import build_from_config

__all__ = [
    "GraphBackend",
    "SimilarityProvider",
    "ContextExtractor",
    "build_from_config",
]
