from contextlib import asynccontextmanager
from databases import Database
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from db.queries import (
    get_active_chains,
    get_available_chain,
    create_new_chain,
    add_chain_element,
    set_chain_active,
    get_chain_history
)
import random

# Static files are handled by a specific sub-router 
static = StaticFiles(directory="static")

# We instanciate a template engine for jinja2
templates = Jinja2Templates(directory="templates")

# And set a database
database = Database('sqlite+aiosqlite:///example.db')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# We mount the static files handler under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Récupération des chaînes actives avec leur dernier élément
    active_chains = await get_active_chains(database)
    
    # On récupère le nom du joueur depuis le cookie
    player_name = request.cookies.get("player_name")
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "active_chains": active_chains,
            "player_name": player_name
        }
    )

@app.post("/start-game")
async def start_game(request: Request, player_name: str = Form(...)):
    # Une chance sur 5 de créer une nouvelle chaîne (sans passer par get_available_chain)
    chain = (await get_available_chain(database)) if random.random() < 0.8 else None

    if chain:
        expected_type = "drawing" if chain["last_type"] == "text" else "text"
        response = templates.TemplateResponse(
            "play.html",
            {
                "request": request,
                "chain_id": chain["id"],
                "last_type": chain["last_type"],
                "last_content": chain["last_content"],
                "player_name": player_name,
                "expected_type": expected_type
            }
        )
    else:
        response = templates.TemplateResponse(
            "new_chain.html",
            {"request": request, "player_name": player_name}
        )
    
    # On ajoute le cookie avec le nom du joueur (expire dans 30 jours)
    response.set_cookie(
        key="player_name",
        value=player_name,
        max_age=30 * 24 * 3600,
        httponly=True
    )
    
    return response

@app.post("/new-chain")
async def create_chain(
    player_name: str = Form(...),
    initial_text: str = Form(...)
):
    # Création d'une nouvelle chaîne
    chain_id = await create_new_chain(database, player_name, initial_text)
    return RedirectResponse(url=f"/chain/{chain_id}", status_code=303)

@app.post("/play/{chain_id}")
async def play_turn(
    request: Request,
    chain_id: int,
    player_name: str = Form(...),
    content: str = Form(...),
    element_type: str = Form(...)
):
    # Vérification du type
    if element_type not in ["text", "drawing"]:
        raise HTTPException(status_code=400, detail="Type invalide")
    
    # Ajout de l'élément à la chaîne
    await add_chain_element(database, chain_id, player_name, content, element_type)
    
    # On remet la chaîne en inactive
    await set_chain_active(database, chain_id, False)
    
    return RedirectResponse(url="/", status_code=303)

@app.get("/chain/{chain_id}")
async def view_chain(request: Request, chain_id: int):
    # Récupération de l'historique de la chaîne
    chain_elements = await get_chain_history(database, chain_id)
    
    if not chain_elements:
        raise HTTPException(status_code=404, detail="Chaîne non trouvée")
    
    return templates.TemplateResponse(
        "chain_history.html",
        {"request": request, "chain_elements": chain_elements}
    )
