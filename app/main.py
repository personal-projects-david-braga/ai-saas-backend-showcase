from fastapi import FastAPI, Header, HTTPException

from app.models import Matter
from app.tenancy import TenantContext, visible_to_tenant

app = FastAPI(title="AI SaaS Backend Showcase")

MATTERS = [
    Matter(id=1, tenant_id=1, title="Contract review"),
    Matter(id=2, tenant_id=2, title="Compliance assessment"),
]


def tenant_from_header(x_tenant_id: int = Header(...)) -> TenantContext:
    if x_tenant_id not in {1, 2}:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return TenantContext(id=x_tenant_id, slug=f"tenant-{x_tenant_id}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/matters")
def list_matters(x_tenant_id: int = Header(...)) -> list[dict]:
    tenant = tenant_from_header(x_tenant_id)
    return [row.__dict__ for row in visible_to_tenant(MATTERS, tenant)]


@app.get("/v1/matters/{matter_id}")
def get_matter(matter_id: int, x_tenant_id: int = Header(...)) -> dict:
    tenant = tenant_from_header(x_tenant_id)
    visible = visible_to_tenant(MATTERS, tenant)
    for matter in visible:
        if matter.id == matter_id:
            return matter.__dict__
    raise HTTPException(status_code=404, detail="Matter not found")
