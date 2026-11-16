from __future__ import annotations

import secrets
import string
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Clave Clara", description="Generador seguro de contraseñas")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class PasswordOptions(BaseModel):
    length: int = Field(default=20, ge=8, le=64)
    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True
    exclude_similar: bool = False

    @model_validator(mode="after")
    def require_character_group(self) -> PasswordOptions:
        if not any((self.uppercase, self.lowercase, self.numbers, self.symbols)):
            raise ValueError("Selecciona al menos un tipo de carácter.")
        return self


def create_password(options: PasswordOptions) -> tuple[str, int, str]:
    groups: list[str] = []
    if options.uppercase:
        groups.append(string.ascii_uppercase)
    if options.lowercase:
        groups.append(string.ascii_lowercase)
    if options.numbers:
        groups.append(string.digits)
    if options.symbols:
        groups.append("!@#$%^&*()-_=+[]{};:,.?")

    if options.exclude_similar:
        similar = set("Il1O0")
        groups = ["".join(char for char in group if char not in similar) for group in groups]

    password_chars = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    password_chars.extend(
        secrets.choice(alphabet) for _ in range(options.length - len(password_chars))
    )
    secrets.SystemRandom().shuffle(password_chars)

    entropy = round(options.length * (len(alphabet).bit_length() - 1))
    if entropy < 60:
        strength = "Básica"
    elif entropy < 80:
        strength = "Buena"
    elif entropy < 100:
        strength = "Fuerte"
    else:
        strength = "Excelente"

    return "".join(password_chars), entropy, strength


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/generate")
def generate_password(options: PasswordOptions, response: Response) -> dict[str, str | int]:
    password, entropy, strength = create_password(options)
    response.headers["Cache-Control"] = "no-store"
    return {"password": password, "entropy": entropy, "strength": strength}


