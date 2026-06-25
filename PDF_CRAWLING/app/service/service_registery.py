import socket
from contextlib import asynccontextmanager
from fastapi import FastAPI
import consul

from app.core.config import settings

consul_client = consul.Consul(host="localhost" , port=8500)

@asynccontextmanager
async def lifespan(app: FastAPI):
    consul_client.agent.service.register(
        name=settings.APP_NAME,
        service_id=settings.SERVICE_ID,
        address=get_ip(),
        port=8080,
        tags=[
            "traefik.enable=true",
            "traefik.http.routers.customer.rule=PathPrefix(`/pdf`)",
            "traefik.http.services.customer.loadbalancer.server.port=8080"
        ],
        check=consul.Check.http(
            url=f"http://{get_ip()}:8080/health",
            interval="10s",
            timeout="5s",
            deregister="1m"
        )
    )

    yield

    consul_client.agent.service.deregister(settings.SERVICE_ID)



app = FastAPI(lifespan=lifespan)
def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address