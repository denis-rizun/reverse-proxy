from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from src.domain.entities.metrics import metrics_storage

router = APIRouter(tags=["metrics"])


@router.get(path="/metrics", response_class=HTMLResponse)
async def metrics_page() -> HTMLResponse:
    html = "<html><head><title>Proxy Metrics</title></head><body>"
    html += f"<h2>Total Requests: {metrics_storage.total_requests}</h2>"

    html += "<h3>Requests per IP:</h3><ul>"
    for ip, count in metrics_storage.requests_per_ip.items():
        html += f"<li>{ip}: {count}</li>"
    html += "</ul>"

    html += "<h3>Upstream Status:</h3><ul>"
    for up, status in metrics_storage.upstream_status.items():
        html += f"<li>{up}: {status} (slots: {
            metrics_storage.upstream_semaphores_count.get(up, 0)
        })</li>"
    html += "</ul>"

    html += f"<p>Global Semaphore Slots: {metrics_storage.global_semaphore_count}</p>"

    html += "</body></html>"
    return html
