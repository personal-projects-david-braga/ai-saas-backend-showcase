from dataclasses import dataclass


@dataclass
class Matter:
    id: int
    tenant_id: int
    title: str
    status: str = "open"


@dataclass
class KnowledgeChunk:
    id: int
    tenant_id: int
    source: str
    text: str
