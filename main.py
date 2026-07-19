#!/usr/bin/env python3
"""
Sombras en la UNMSM
Punto de entrada principal del juego.
Desarrolador: Tapia Acosta Sandro Estanislao
FCM-UNMSM - 2026
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
