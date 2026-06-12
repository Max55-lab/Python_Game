"""
====================================================================
BLOCK CLASS
====================================================================

Autor: [Josip Kapular]
Projekt: Tetris / Grid Based Game
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ova klasa predstavlja osnovni BLOCK sistem za Tetris igru.

Svaki blok u igri:
- ima svoj oblik
- ima svoju boju
- može se pomicati
- može se rotirati
- zna kako se nacrtati na ekran

Ovo je BASE CLASS (bazna klasa).

To znači:
drugi blokovi poput:
- T Block
- L Block
- I Block
- Square Block

mogu naslijediti ovu klasu.

====================================================================
GAME DEVELOPMENT KONCEPTI
====================================================================

U ovom kodu koriste se:

1. Object Oriented Programming (OOP)
2. Grid Based Movement
3. Tile System
4. Rotation States
5. Rendering System
6. Coordinate Transformations

====================================================================
KAKO RADI SISTEM
====================================================================

Blok se sastoji od više ćelija (tiles).

Primjer T bloka:

    []
[][][]

Svaka ćelija ima:
- row (red)
- column (kolonu)

Sve pozicije se računaju preko:
- lokalnih koordinata
- offset pozicije

====================================================================
IMPORTI
====================================================================
"""

# ---------------------------------------------------------------
# Import Colors klase
# ---------------------------------------------------------------
#
# Ova klasa sadrži definicije boja koje koristimo u igri.
#
# Primjer:
# colors[1] = crvena
# colors[2] = plava
#
# Koristi se za:
# - bojanje blokova
# - vizualni identitet blokova
#
from colors import Colors


# ---------------------------------------------------------------
# Import pygame biblioteke
# ---------------------------------------------------------------
#
# pygame koristimo za:
#
# - crtanje objekata
# - game loop
# - input handling
# - rendering
# - collision
# - audio
#
# U ovom fajlu pygame koristimo prvenstveno za:
# - pygame.Rect
# - pygame.draw.rect
#
import pygame


# ---------------------------------------------------------------
# Import Position klase
# ---------------------------------------------------------------
#
# Position klasa predstavlja:
#
# - row
# - column
#
# Umjesto tuple:
#   (0,1)
#
# koristimo:
#   Position(0,1)
#
# Ovo činim da kod ucinim:
# - čitljivijim
# - organizovanijim
#
from position import Position


"""
====================================================================
BLOCK CLASS
====================================================================

Ovo je glavna bazna klasa za sve blokove u igri.

Svaki blok:
- ima ID
- ima boju
- ima rotacije
- ima poziciju
- zna kako se crta

====================================================================
"""
class Block:

    """
    ================================================================
    CONSTRUCTOR
    ================================================================

    __init__ metoda se automatski poziva kada napravimo objekat.

    Primjer:
        block = Block(1)

    ================================================================
    """
    def __init__(self, id):

        # -----------------------------------------------------------
        # ID BLOKA
        # -----------------------------------------------------------
        #
        # Jedinstveni identifikator bloka.
        #
        # Koristi se za:
        # - identifikaciju tipa bloka
        # - određivanje boje
        # - gameplay logiku
        #
        # Primjer:
        # 1 = T Block
        # 2 = L Block
        # 3 = I Block
        #
        self.id = id


        # -----------------------------------------------------------
        # CELLS DICTIONARY
        # -----------------------------------------------------------
        #
        # Ovdje čuvamo sve rotacije bloka.
        #
        # Dictionary format:
        #
        # self.cells = {
        #     0: [pozicije],
        #     1: [pozicije],
        #     2: [pozicije],
        #     3: [pozicije]
        # }
        #
        # Svaki broj predstavlja stanje rotacije.
        #
        # Primjer:
        #
        # 0 = normalna rotacija
        # 1 = 90 stepeni
        # 2 = 180 stepeni
        # 3 = 270 stepeni
        #
        # Pozicije su lokalne koordinate.
        #
        self.cells = {}


        # -----------------------------------------------------------
        # CELL SIZE
        # -----------------------------------------------------------
        #
        # Veličina jedne ćelije u pikselima.
        #
        # 30 znači:
        # - širina = 30 px
        # - visina = 30 px
        #
        # Ovo određuje:
        # - veličinu blokova
        # - izgled igre
        #
        self.cell_size = 30


        # -----------------------------------------------------------
        # ROW OFFSET
        # -----------------------------------------------------------
        #
        # Vertikalna pozicija bloka na gridu.
        #
        # Pomjera blok:
        # - gore
        # - dole
        #
        self.row_offset = 0


        # -----------------------------------------------------------
        # COLUMN OFFSET
        # -----------------------------------------------------------
        #
        # Horizontalna pozicija bloka na gridu.
        #
        # Pomjera blok:
        # - lijevo
        # - desno
        #
        self.column_offset = 0


        # -----------------------------------------------------------
        # ROTATION STATE
        # -----------------------------------------------------------
        #
        # Predstavlja trenutno stanje rotacije.
        #
        # Primjer:
        #
        # 0 = početna rotacija
        # 1 = rotirano 90°
        # 2 = rotirano 180°
        # 3 = rotirano 270°
        #
        self.rotation_state = 0


        # -----------------------------------------------------------
        # COLORS
        # -----------------------------------------------------------
        #
        # Dohvaćamo sve boje iz Colors klase.
        #
        # Primjer:
        #
        # self.colors[1]
        #
        # vraća boju za blok sa ID-em 1.
        #
        self.colors = Colors.get_cell_colors()


    """
    ================================================================
    MOVE METHOD
    ================================================================

    Ova metoda pomjera blok.

    Parametri:
    - rows
    - columns

    Primjer:
        move(1,0)
        -> pomjeri dole

        move(0,-1)
        -> pomjeri lijevo

    ================================================================
    """
    def move(self, rows, columns):

        # -----------------------------------------------------------
        # POMJERANJE PO Y OSI
        # -----------------------------------------------------------
        #
        # rows određuje vertikalni pomak.
        #
        self.row_offset += rows


        # -----------------------------------------------------------
        # POMJERANJE PO X OSI
        # -----------------------------------------------------------
        #
        # columns određuje horizontalni pomak.
        #
        self.column_offset += columns


    """
    ================================================================
    GET CELL POSITIONS
    ================================================================

    Ova metoda računa finalne/globalne pozicije bloka.
    
    - cells sadrži lokalne koordinate
    - offset sadrži globalnu poziciju

    ================================================================
    """
    def get_cell_positions(self):

        # -----------------------------------------------------------
        # DOHVATI TILEOVE/BLOKOVE ZA TRENUTNU ROTACIJU
        # -----------------------------------------------------------
        #
        # Primjer:
        # rotation_state = 2
        #
        # Dohvati:
        # self.cells[2]
        #
        tiles = self.cells[self.rotation_state]


        # -----------------------------------------------------------
        # LISTA FINALNIH POZICIJA
        # -----------------------------------------------------------
        #
        # Ovdje spremamo:
        # - stvarne pozicije bloka na gridu
        #
        moved_tiles = []


        # -----------------------------------------------------------
        # PROLAZAK KROZ TILEOVE
        # -----------------------------------------------------------
        #
        for position in tiles:

            # -------------------------------------------------------
            # RAČUNANJE GLOBALNE POZICIJE
            # -------------------------------------------------------
            #
            # Dodajemo offset na lokalnu poziciju.
            #
            # Primjer:
            #
            # Lokalna:
            #   (0,1)
            #
            # Offset:
            #   row = 5
            #   col = 3
            #
            # Finalna:
            #   (5,4)
            #
            position = Position(
                position.row + self.row_offset,
                position.column + self.column_offset
            )


            # -------------------------------------------------------
            # DODAJ U LISTU
            # -------------------------------------------------------
            #
            moved_tiles.append(position)


        # -----------------------------------------------------------
        # VRATI FINALNE POZICIJE
        # -----------------------------------------------------------
        #
        return moved_tiles


    """
    ================================================================
    ROTATE METHOD
    ================================================================

    Rotira blok na sljedeću rotaciju.

    Primjer:
    0 -> 1
    1 -> 2
    2 -> 3
    3 -> 0

    ================================================================
    """
    def rotate(self):

        # -----------------------------------------------------------
        # PRELAZAK NA SLJEDEĆU ROTACIJU
        # -----------------------------------------------------------
        #
        self.rotation_state += 1


        # -----------------------------------------------------------
        # RESET ROTACIJE
        # -----------------------------------------------------------
        #
        # Ako smo prešli zadnju rotaciju:
        #
        # vrati se na početak.
        #
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0


    """
    ================================================================
    UNDO ROTATION
    ================================================================

    Vraća rotaciju unazad.

    Koristi se kada:
    - rotacija udara u zid
    - rotacija udara u drugi blok
    - rotacija nije validna

    ================================================================
    """
    def undo_rotation(self):

        # -----------------------------------------------------------
        # VRATI JEDNU ROTACIJU NAZAD
        # -----------------------------------------------------------
        #
        self.rotation_state -= 1


        # -----------------------------------------------------------
        # AKO SMO ISPOD NULE
        # -----------------------------------------------------------
        #
        # Idi na zadnju rotaciju.
        #
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1


    """
    ================================================================
    DRAW METHOD
    ================================================================

    Ova metoda crta blok na ekran.

    Parametri:
    - screen
    - offset_x
    - offset_y

    ================================================================
    """
    def draw(self, screen, offset_x, offset_y):

        # -----------------------------------------------------------
        # DOHVATI FINALNE POZICIJE
        # -----------------------------------------------------------
        #
        tiles = self.get_cell_positions()


        # -----------------------------------------------------------
        # PROLAZAK KROZ TILEOVE
        # -----------------------------------------------------------
        #
        for tile in tiles:

            # -------------------------------------------------------
            # KREIRANJE RECTANGLE OBJEKTA
            # -------------------------------------------------------
            #
            # pygame.Rect:
            #
            # x
            # y
            # width
            # height
            #
            # Formula:
            #
            # x = offset_x + column * cell_size
            # y = offset_y + row * cell_size
            #
            tile_rect = pygame.Rect(

                # X pozicija
                offset_x + tile.column * self.cell_size,

                # Y pozicija
                offset_y + tile.row * self.cell_size,

                # Width
                self.cell_size - 1,

                # Height
                self.cell_size - 1
            )


            # -------------------------------------------------------
            # CRTANJE TILEA
            # -------------------------------------------------------
            #
            # pygame.draw.rect(
            #     surface,
            #     color,
            #     rectangle
            # )
            #
            pygame.draw.rect(

                # Surface za crtanje
                screen,

                # Boja bloka
                self.colors[self.id],

                # Rectangle shape
                tile_rect
            )


"""
====================================================================
KRAJ KLASE
====================================================================

Ova klasa predstavlja srce Tetris block sistema.

====================================================================
GAME DEV ARHITEKTURA
====================================================================

Ova klasa pripada:

GAMEPLAY LAYER-u

Komunicira sa:
- Grid sistemom
- Collision sistemom
- Input sistemom
- Rendering sistemom

====================================================================
GAME DEV PATTERN
====================================================================

Ovo je:
- reusable architecture
- modular architecture
- object oriented design

Isti princip koriste:
- puzzle igre
- strategy igre
- tile based RPG igre
- Tetris klonovi

====================================================================
"""