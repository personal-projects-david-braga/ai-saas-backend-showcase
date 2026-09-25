from app.models import KnowledgeChunk
from app.tenancy import TenantContext, visible_to_tenant


def retrieve_context(
    chunks: list[KnowledgeChunk],
    tenant: TenantContext,
    query: str,
    limit: int = 3,
) -> list[KnowledgeChunk]:
    """Return only tenant-owned chunks, ranked by simple lexical overlap."""
    tenant_chunks = visible_to_tenant(chunks, tenant)
    terms = {term.lower() for term in query.split() if term.strip()}

    ranked = sorted(
        tenant_chunks,
        key=lambda chunk: sum(term in chunk.text.lower() for term in terms),
        reverse=True,
    )
    return ranked[:limit]
