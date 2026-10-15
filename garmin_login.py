#!/usr/bin/env python3
"""Login interactivo a Garmin Connect. Pide credenciales en la terminal
(la contraseña no se muestra ni se guarda); solo se guardan los tokens."""
import getpass
import os
import sys
from pathlib import Path

from garminconnect import Garmin

TOKENSTORE = Path(os.getenv("GARMINTOKENS", "~/.garminconnect")).expanduser()


def connect() -> Garmin:
    # 1) Intentar con tokens guardados
    if TOKENSTORE.exists():
        try:
            g = Garmin()
            g.login(str(TOKENSTORE))
            return g
        except Exception as e:
            print(f"Tokens guardados no válidos ({type(e).__name__}); login nuevo.")

    # 2) Login con credenciales
    email = input("Email de Garmin: ").strip()
    password = getpass.getpass("Contraseña de Garmin: ")
    g = Garmin(email, password, prompt_mfa=lambda: input("Código MFA (si lo pide): ").strip())
    TOKENSTORE.mkdir(parents=True, exist_ok=True)
    os.chmod(TOKENSTORE, 0o700)
    g.login(str(TOKENSTORE))
    return g


if __name__ == "__main__":
    try:
        g = connect()
    except Exception as e:
        print(f"Error de login: {e}", file=sys.stderr)
        sys.exit(1)
    print("Conectado como:", g.get_full_name())
    try:
        for d in g.get_devices():
            print("Dispositivo:", d.get("productDisplayName") or d.get("displayName"))
    except Exception as e:
        print("No se pudieron listar dispositivos:", e)
    print(f"Tokens guardados en {TOKENSTORE}")
