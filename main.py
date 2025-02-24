from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static files are handled by a specific sub-router monted on /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# We instanciate a template engine for jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        name="index.html", 
       request=request
    )
