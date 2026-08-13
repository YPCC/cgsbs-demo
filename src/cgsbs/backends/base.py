"""Abstract interfaces so the four roadmap items are swappable."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from rdflib import Graph, URIRef

from ..scoring import PatientContext


class GraphBackend(ABC):
    """
    Abstraction over the graph store.

    Implementations:
      - RDFLibBackend   (in-memory / file, current default)
      - GraphDBBackend  (SPARQL endpoint + optional path-search SERVICE)
    """

    @abstractmethod
    def load(self) -> None:
        """Load or connect to the ontology data."""

    @abstractmethod
    def get_graph(self) -> Graph:
        """Return an rdflib.Graph view (or a compatible wrapper)."""

    @abstractmethod
    def neighbors(
        self, node: URIRef, allowed_predicates: Optional[set] = None
    ) -> List[Tuple[URIRef, URIRef]]:
        """Return list of (predicate, neighbor)."""

    @abstractmethod
    def build_envelope(
        self,
        anchors: List[URIRef],
        max_depth: int = 3,
        max_nodes: int = 80,
    ) -> Graph:
        """Construct the Ontology Envelope around the given anchors."""

    def close(self) -> None:
        """Optional cleanup."""


class SimilarityProvider(ABC):
    """
    Provides S_UMLS-rel and S_UMLS-sim style scores.

    Implementations:
      - SyntheticSimilarity   (heuristic, always available)
      - UMLSSimilarity        (pyumls-similarity / umls-similarity)
      - EmbeddingSimilarity   (sentence-transformers)
    """

    @abstractmethod
    def relatedness(self, node_uri: str, node_label: str, context: PatientContext) -> float:
        ...

    @abstractmethod
    def similarity(self, node_uri: str, node_label: str, context: PatientContext) -> float:
        ...


class ContextExtractor(ABC):
    """
    Turns free-text clinical notes into a PatientContext graph.

    Implementations:
      - DeterministicExtractor   (current demo)
      - SciSpacyExtractor
      - BioPortalAnnotatorExtractor
      - LLMExtractor (stub)
    """

    @abstractmethod
    def extract(self, note_id: str, text: str) -> PatientContext:
        ...
