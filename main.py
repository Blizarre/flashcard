import json
import uuid
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import logging

# Hijacking the uvicorn logger. Not very pretty but will do for a simple
# project like this
log = logging.getLogger("uvicorn.default")


app = FastAPI()

CARDS_FILE = Path("data/cards.json")

try:
    # Quick and dirty read to make sure that we can access the file
    with open(CARDS_FILE, "rb") as fd:
        fd.read()
    # And read/write to it
    with open(CARDS_FILE, "a+b") as fd:
        fd.read()

except FileNotFoundError:
    log.warning("Cards file not found, creating a dummy one in %s", CARDS_FILE)
    # And if it doesn't exist we create it
    with open(CARDS_FILE, "wb") as fd:
        fd.write(b"{}")


class PostCardInput(BaseModel):
    question: str
    answer: str


@app.post("/card", status_code=201)
async def new(card: PostCardInput) -> str:
    with open(CARDS_FILE, "rb") as fd:
        cards = json.load(fd)

    new_id = uuid.uuid4().hex

    cards[new_id] = dict(
        question=card.question,
        answer=card.answer,
    )

    with open(CARDS_FILE, "w") as fd:
        json.dump(cards, fd)

    return new_id


@app.put("/card/{cardid}", status_code=204)
async def update(cardid: str, card: PostCardInput):
    with open(CARDS_FILE, "rb") as fd:
        cards = json.load(fd)

    cards[cardid] = dict(
        question=card.question,
        answer=card.answer,
    )

    with open(CARDS_FILE, "w") as fd:
        json.dump(cards, fd)


@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")


app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/", StaticFiles(directory="static"), name="static")
