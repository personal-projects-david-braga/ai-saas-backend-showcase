from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    id: int
    slug: str


def visible_to_tenant(rows: list, tenant: TenantContext) -> list:
    """Return only rows owned by the active tenant."""
    return [row for row in rows if getattr(row, "tenant_id", None) == tenant.id]
