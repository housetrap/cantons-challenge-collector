import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI()

# Trust proxy forwarding headers (X-Forwarded-Proto/Forwarded) so generated URLs
# keep the original HTTPS scheme when the app is behind a reverse proxy.
app.add_middleware(
    ProxyHeadersMiddleware,
    trusted_hosts=os.getenv("TRUSTED_PROXY_IPS", "*").split(","),
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/health", response_class=HTMLResponse)
async def health():
    return HTMLResponse(
        content="<h1>Health Check</h1><p>The application is running.</p>"
    )


@app.get("/vote/{code}", response_class=HTMLResponse)
async def vote(request: Request, code: str):
    api_url = f"https://api.aperoescape.ch/dc/v1/vote/{code}"
    api_response = None
    api_error = None

    try:
        # The endpoint expects a POST to return vote details.
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(api_url)

        response.raise_for_status()
        api_response = response.json() if response.content else {}
    except httpx.HTTPStatusError as exc:
        api_error = f"HTTP {exc.response.status_code}: {exc.response.text or exc.response.reason_phrase}"
    except httpx.RequestError as exc:
        api_error = f"Connection error: {exc}"
    except ValueError:
        api_error = "API returned non-JSON content"

    if (
        api_error is None
        and api_response is not None
        and api_response.get("error_code") is None
    ):
        template_name = "result_ok.html"
    else:
        template_name = "result_error.html"

    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "code": code,
            "api_url": api_url,
            "api_response": api_response,
            "api_error": api_error,
        },
    )


@app.get("/test-ok", response_class=HTMLResponse)
async def test_ok(request: Request):
    api_url = "https://api.aperoescape.ch/dc/v1/vote/OK"
    api_response = {"message": "This is a test OK response."}
    api_error = None

    template_name = "result_ok.html"

    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "code": "OK",
            "api_url": api_url,
            "api_response": api_response,
            "api_error": api_error,
        },
    )


@app.get("/test-error", response_class=HTMLResponse)
async def test_error(request: Request):
    api_url = "https://api.aperoescape.ch/dc/v1/vote/ERROR"
    api_response = None
    api_error = "This is a test error response."

    template_name = "result_error.html"

    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "code": "ERROR",
            "api_url": api_url,
            "api_response": api_response,
            "api_error": api_error,
        },
    )
