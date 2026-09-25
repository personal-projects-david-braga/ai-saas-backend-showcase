from app.models import KnowledgeChunk
from app.services.retrieval import retrieve_context
from app.tenancy import TenantContext


def test_retrieval_never_crosses_tenant_boundary() -> None:
    chunks = [
        KnowledgeChunk(id=1, tenant_id=1, source="a", text="contract payment terms"),
        KnowledgeChunk(id=2, tenant_id=2, source="b", text="contract payment terms"),
    ]

    results = retrieve_context(
        chunks,
        TenantContext(id=1, slug="tenant-1"),
        query="payment terms",
    )

    assert [chunk.id for chunk in results] == [1]
