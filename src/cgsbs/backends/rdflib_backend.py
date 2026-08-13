"""In-memory RDFLib backend (default for synthetic demo)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Set, Tuple

from rdflib import Graph, URIRef, RDF, RDFS
from rdflib.namespace import SKOS

from .base import GraphBackend
from ..envelope import (
    load_ontology,
    build_envelope as _build_envelope,
    ALLOWED_PREDICATES,
    get_label,
)


class RDFLibBackend(GraphBackend):
    def __init__(self, ontology_path: str | Path):
        self.ontology_path = Path(ontology_path)
        self._g: Optional[Graph] = None

    def load(self) -> None:
        self._g = load_ontology(str(self.ontology_path))

    def get_graph(self) -> Graph:
        if self._g is None:
            self.load()
        assert self._g is not None
        return self._g

    def neighbors(
        self, node: URIRef, allowed_predicates: Optional[Set] = None
    ) -> List[Tuple[URIRef, URIRef]]:
        g = self.get_graph()
        preds = allowed_predicates or ALLOWED_PREDICATES
        out: List[Tuple[URIRef, URIRef]] = []
        for p, o in g.predicate_objects(node):
            if p in preds and isinstance(o, URIRef):
                out.append((p, o))
        for s, p in g.subject_predicates(node):
            if p in preds and isinstance(s, URIRef):
                out.append((p, s))
        return out

    def build_envelope(
        self,
        anchors: List[URIRef],
        max_depth: int = 3,
        max_nodes: int = 80,
    ) -> Graph:
        return _build_envelope(self.get_graph(), anchors, max_depth, max_nodes)
