"""
====================================================================
TETRIS BLOCK DEFINITIONS
====================================================================

Autor: [Josip Kapular]
Projekt: Tetris / Grid Based Game
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ovaj fajl sadrži definicije svih Tetris blokova.

Blokovi:
- L Block
- J Block
- I Block
- O Block
- S Block
- T Block
- Z Block

Svaki blok:
- nasljeđuje Block klasu
- ima svoje rotacije
- ima svoj ID
- ima početnu spawn poziciju

====================================================================
GAME DEV KONCEPT
====================================================================

Svaki blok koristi:

1. Inheritance (nasljeđivanje)
2. Rotation States
3. Grid Coordinates
4. Tile Based Design

====================================================================
IMPORTI
====================================================================
"""

# ---------------------------------------------------------------
# Import bazne Block klase
# ---------------------------------------------------------------
#
# Svi blokovi nasljeđuju ovu klasu.
#
# Ona sadrži:
# - movement
# - rotation
# - drawing
# - positioning
#
from block import Block


# ---------------------------------------------------------------
# Import Position klase
# ---------------------------------------------------------------
#
# Position predstavlja:
# - row
# - column
#
# Koristi se za grid koordinatni sistem.
#
from position import Position


"""
====================================================================
L BLOCK
====================================================================

Vizualni oblik:

      []
[][][]

====================================================================
ROTACIJE
====================================================================

ROTATION 0

  . . X
  X X X

ROTATION 1

  . X
  . X
  . X X

ROTATION 2

  X X X
  X . .

ROTATION 3

  X X
  . X
  . X

====================================================================
"""
class LBlock(Block):

    """
    ================================================================
    CONSTRUCTOR
    ================================================================
    """
    def __init__(self):

        # -----------------------------------------------------------
        # POZIV PARENT KLASE
        # -----------------------------------------------------------
        #
        # id = 1
        #
        # Svaki blok ima jedinstveni ID.
        #
        super().__init__(id=1)


        # -----------------------------------------------------------
        # ROTATION STATES
        # -----------------------------------------------------------
        #
        # Dictionary svih rotacija.
        #
        self.cells = {

            # -------------------------------------------------------
            # ROTACIJA 0
            # -------------------------------------------------------
            #
            # . . X
            # X X X
            #
            0: [
                Position(0, 2),
                Position(1, 0),
                Position(1, 1),
                Position(1, 2)
            ],


            # -------------------------------------------------------
            # ROTACIJA 1
            # -------------------------------------------------------
            #
            # . X
            # . X
            # . X X
            #
            1: [
                Position(0, 1),
                Position(1, 1),
                Position(2, 1),
                Position(2, 2)
            ],


            # -------------------------------------------------------
            # ROTACIJA 2
            # -------------------------------------------------------
            #
            # X X X
            # X . .
            #
            2: [
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
                Position(2, 0)
            ],


            # -------------------------------------------------------
            # ROTACIJA 3
            # -------------------------------------------------------
            #
            # X X
            # . X
            # . X
            #
            3: [
                Position(0, 0),
                Position(0, 1),
                Position(1, 1),
                Position(2, 1)
            ]
        }


        # -----------------------------------------------------------
        # POČETNA SPAWN POZICIJA
        # -----------------------------------------------------------
        #
        # Pomjeri blok:
        # - 0 redova
        # - 3 kolone desno
        #
        self.move(0, 3)


"""
====================================================================
J BLOCK
====================================================================

Vizualni oblik:

[][]
  []

====================================================================
"""
class JBlock(Block):

    def __init__(self):

        # ID = 2
        super().__init__(id=2)


        # -----------------------------------------------------------
        # DEFINICIJE ROTACIJA
        # -----------------------------------------------------------
        #
        self.cells = {

            # ROTACIJA 0
            0: [
                Position(0, 0),
                Position(1, 0),
                Position(1, 1),
                Position(1, 2)
            ],

            # ROTACIJA 1
            1: [
                Position(0, 1),
                Position(0, 2),
                Position(1, 1),
                Position(2, 1)
            ],

            # ROTACIJA 2
            2: [
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
                Position(2, 2)
            ],

            # ROTACIJA 3
            3: [
                Position(0, 1),
                Position(1, 1),
                Position(2, 0),
                Position(2, 1)
            ]
        }


        # Spawn pozicija
        self.move(0, 3)


"""
====================================================================
I BLOCK
====================================================================

Vizualni oblik:

[][][][]

====================================================================
SPECIJALNO
====================================================================

I Block koristi drugačiji spawn offset
zbog svoje širine.

====================================================================
"""
class IBlock(Block):

    def __init__(self):

        # ID = 3
        super().__init__(id=3)


        # -----------------------------------------------------------
        # ROTACIJE
        # -----------------------------------------------------------
        #
        self.cells = {

            # Horizontalna linija
            0: [
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
                Position(1, 3)
            ],

            # Vertikalna linija
            1: [
                Position(0, 2),
                Position(1, 2),
                Position(2, 2),
                Position(3, 2)
            ],

            # Horizontalna
            2: [
                Position(2, 0),
                Position(2, 1),
                Position(2, 2),
                Position(2, 3)
            ],

            # Vertikalna
            3: [
                Position(0, 1),
                Position(1, 1),
                Position(2, 1),
                Position(3, 1)
            ]
        }


        # -----------------------------------------------------------
        # SPAWN OFFSET
        # -----------------------------------------------------------
        #
        # -1 row:
        # omogućava spawn iznad grid-a
        #
        self.move(-1, 3)


"""
====================================================================
O BLOCK
====================================================================

Vizualni oblik:

[][]
[][]

====================================================================
SPECIJALNO
====================================================================

O Block nema rotacije
jer izgleda isto iz svih uglova.

====================================================================
"""
class OBlock(Block):

    def __init__(self):

        # ID = 4
        super().__init__(id=4)


        # -----------------------------------------------------------
        # SAMO JEDNA ROTACIJA
        # -----------------------------------------------------------
        #
        self.cells = {

            0: [
                Position(0, 0),
                Position(0, 1),
                Position(1, 0),
                Position(1, 1)
            ]
        }


        # Spawn pozicija
        self.move(0, 4)


"""
====================================================================
S BLOCK
====================================================================

Vizualni oblik:

  [][]
[][]

====================================================================
"""
class SBlock(Block):

    def __init__(self):

        # ID = 5
        super().__init__(id=5)


        # Rotacije
        self.cells = {

            0: [
                Position(0, 1),
                Position(0, 2),
                Position(1, 0),
                Position(1, 1)
            ],

            1: [
                Position(0, 1),
                Position(1, 1),
                Position(1, 2),
                Position(2, 2)
            ],

            2: [
                Position(1, 1),
                Position(1, 2),
                Position(2, 0),
                Position(2, 1)
            ],

            3: [
                Position(0, 0),
                Position(1, 0),
                Position(1, 1),
                Position(2, 1)
            ]
        }


        # Spawn pozicija
        self.move(0, 3)


"""
====================================================================
T BLOCK
====================================================================

Vizualni oblik:

  []
[][][]

====================================================================
"""
class TBlock(Block):

    def __init__(self):

        # ID = 6
        super().__init__(id=6)


        # Rotacije
        self.cells = {

            0: [
                Position(0, 1),
                Position(1, 0),
                Position(1, 1),
                Position(1, 2)
            ],

            1: [
                Position(0, 1),
                Position(1, 1),
                Position(1, 2),
                Position(2, 1)
            ],

            2: [
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
                Position(2, 1)
            ],

            3: [
                Position(0, 1),
                Position(1, 0),
                Position(1, 1),
                Position(2, 1)
            ]
        }


        # Spawn pozicija
        self.move(0, 3)


"""
====================================================================
Z BLOCK
====================================================================

Vizualni oblik:

[][]
  [][]

====================================================================
"""
class ZBlock(Block):

    def __init__(self):

        # ID = 7
        super().__init__(id=7)


        # Rotacije
        self.cells = {

            0: [
                Position(0, 0),
                Position(0, 1),
                Position(1, 1),
                Position(1, 2)
            ],

            1: [
                Position(0, 2),
                Position(1, 1),
                Position(1, 2),
                Position(2, 1)
            ],

            2: [
                Position(1, 0),
                Position(1, 1),
                Position(2, 1),
                Position(2, 2)
            ],

            3: [
                Position(0, 1),
                Position(1, 0),
                Position(1, 1),
                Position(2, 0)
            ]
        }


        # Spawn pozicija
        self.move(0, 3)


"""
====================================================================
KRAJ FILE-A
====================================================================

Ovaj fajl definiše sve Tetris blokove.

Svaki blok:
- koristi isti rendering sistem
- koristi isti movement sistem
- koristi isti rotation sistem

To je moguće zahvaljujući:
- inheritance
- modular architecture
- reusable code design

====================================================================
GAME DEV ARHITEKTURA
====================================================================

Ovaj fajl pripada:

GAMEPLAY OBJECT LAYER-u

Komunicira sa:
- Grid sistemom
- Collision sistemom
- Rendering sistemom
- Input sistemom

====================================================================
 GAME DEV PATTERN
====================================================================

Ovo je pattern koji koriste:
- Tetris klonovi
- puzzle igre
- tile based igre
- strategy igre

====================================================================
"""