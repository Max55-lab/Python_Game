"""
====================================================================
GRID CLASS
====================================================================

Autor: [Josip Kapular]
Projekt: Advanced Tetris Clone
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ova klasa predstavlja GAME GRID odnosno GAME BOARD.

Grid je srce Tetris igre jer:
- čuva sve postavljene blokove
- provjerava kolizije
- briše pune redove
- crta stanje igre

====================================================================
ŠTO JE GRID?
====================================================================

Grid je 2D matrica.

Vizualno:

[0][0][0][0][0]
[0][1][1][0][0]
[0][2][0][0][0]

Svaki broj predstavlja:
0 = prazno polje
1 = određeni blok
2 = drugi blok
itd.

====================================================================
GAME DEV KONCEPTI
====================================================================

Ovaj sistem koristi:

✔ 2D Matrix System
✔ Tile Based Architecture
✔ Collision Grid
✔ Line Clear Logic
✔ Rendering Grid
✔ Spatial Representation

====================================================================
IMPORTI
====================================================================
"""

# ---------------------------------------------------------------
# PYGAME
# ---------------------------------------------------------------
#
# Koristimo za:
# - rendering
# - rectangles
# - drawing
#
import pygame


# ---------------------------------------------------------------
# COLORS
# ---------------------------------------------------------------
#
# Klasa sa svim bojama igre.
#
from colors import Colors


"""
====================================================================
GRID CLASS
====================================================================

Grid predstavlja:
- play field
- game matrix
- collision map

====================================================================
"""
class Grid:

    """
    ================================================================
    CONSTRUCTOR
    ================================================================

    Kreira novi grid.

    ================================================================
    """
    def __init__(self):

        # -----------------------------------------------------------
        # BROJ REDOVA
        # -----------------------------------------------------------
        #
        # Standardni Tetris:
        # 20 redova
        #
        self.num_rows = 20


        # -----------------------------------------------------------
        # BROJ KOLONA
        # -----------------------------------------------------------
        #
        # Standardni Tetris:
        # 10 kolona
        #
        self.num_cols = 10


        # -----------------------------------------------------------
        # VELIČINA ĆELIJE
        # -----------------------------------------------------------
        #
        # Svaki tile:
        # 30x30 px
        #
        self.cell_size = 30


        # -----------------------------------------------------------
        # GRID MATRICA
        # -----------------------------------------------------------
        #
        # Kreiramo 2D listu.
        #
        # Vizualno:
        #
        # [
        #   [0,0,0,0],
        #   [0,0,0,0],
        #   [0,0,0,0]
        # ]
        #
        # 0 znači:
        # prazna ćelija
        #
        self.grid = [

            [
                0 for j in range(self.num_cols)
            ]

            for i in range(self.num_rows)
        ]


        # -----------------------------------------------------------
        # COLORS
        # -----------------------------------------------------------
        #
        # Lista boja za rendering.
        #
        self.colors = Colors.get_cell_colors()


    """
    ================================================================
    PRINT GRID
    ================================================================

    Debug metoda.

    Ispisuje grid u terminal.

    ================================================================
    """
    def print_grid(self):

        # -----------------------------------------------------------
        # PROLAZ KROZ REDOVE
        # -----------------------------------------------------------
        #
        for row in range(self.num_rows):

            # -------------------------------------------------------
            # PROLAZ KROZ KOLONE
            # -------------------------------------------------------
            #
            for column in range(self.num_cols):

                # Ispiši vrijednost ćelije
                print(
                    self.grid[row][column],
                    end=" "
                )

            # Novi red
            print()


    """
    ================================================================
    IS INSIDE
    ================================================================

    Provjerava da li je pozicija unutar granica grid-a.

    ================================================================
    """
    def is_inside(self, row, column):

        # -----------------------------------------------------------
        # BOUNDARY CHECK
        # -----------------------------------------------------------
        #
        # Provjeravamo:
        #
        # row:
        # >= 0
        # < broj redova
        #
        # column:
        # >= 0
        # < broj kolona
        #
        if (
            row >= 0
            and row < self.num_rows
            and column >= 0
            and column < self.num_cols
        ):

            return True


        return False


    """
    ================================================================
    IS EMPTY
    ================================================================

    Provjerava da li je ćelija prazna.

    ================================================================
    """
    def is_empty(self, row, column):

        # -----------------------------------------------------------
        # EMPTY CELL CHECK
        # -----------------------------------------------------------
        #
        # 0 znači:
        # prazna ćelija
        #
        if self.grid[row][column] == 0:

            return True


        return False


    """
    ================================================================
    IS ROW FULL
    ================================================================

    Provjerava da li je red potpuno popunjen.

    ================================================================
    """
    def is_row_full(self, row):

        # -----------------------------------------------------------
        # PROLAZ KROZ KOLONE
        # -----------------------------------------------------------
        #
        for column in range(self.num_cols):

            # -------------------------------------------------------
            # AKO POSTOJI PRAZNO POLJE
            # -------------------------------------------------------
            #
            if self.grid[row][column] == 0:

                return False


        # -----------------------------------------------------------
        # RED JE PUN
        # -----------------------------------------------------------
        #
        return True


    """
    ================================================================
    CLEAR ROW
    ================================================================

    Briše jedan red.

    ================================================================
    """
    def clear_row(self, row):

        # -----------------------------------------------------------
        # RESET REDA
        # -----------------------------------------------------------
        #
        # Sve ćelije postaju 0.
        #
        for column in range(self.num_cols):

            self.grid[row][column] = 0


    """
    ================================================================
    MOVE ROW DOWN
    ================================================================

    Pomjera red dole.

    Koristi se nakon line clear-a.

    ================================================================
    """
    def move_row_down(self, row, num_rows):

        # -----------------------------------------------------------
        # COPY ROW DOWN
        # -----------------------------------------------------------
        #
        for column in range(self.num_cols):

            # -------------------------------------------------------
            # COPY VALUE
            # -------------------------------------------------------
            #
            self.grid[row + num_rows][column] = (
                self.grid[row][column]
            )


            # -------------------------------------------------------
            # CLEAR ORIGINAL
            # -------------------------------------------------------
            #
            self.grid[row][column] = 0


    """
    ================================================================
    CLEAR FULL ROWS
    ================================================================

    Glavna line clear logika.

    ================================================================
    """
    def clear_full_rows(self):

        # -----------------------------------------------------------
        # BROJ OBRISANIH REDOVA
        # -----------------------------------------------------------
        #
        completed = 0


        # -----------------------------------------------------------
        # ITERACIJA OD DNA PREMA VRHU
        # -----------------------------------------------------------
        #
        # Veoma važno:
        # line clear se radi bottom-up
        #
        for row in range(
            self.num_rows - 1,
            0,
            -1
        ):

            # -------------------------------------------------------
            # AKO JE RED PUN
            # -------------------------------------------------------
            #
            if self.is_row_full(row):

                # Obriši red
                self.clear_row(row)

                # Povećaj counter
                completed += 1


            # -------------------------------------------------------
            # AKO IMAMO OBRISANE REDOVE
            # -------------------------------------------------------
            #
            elif completed > 0:

                # Pomjeri red dole
                self.move_row_down(
                    row,
                    completed
                )


        # -----------------------------------------------------------
        # VRATI BROJ OBRISANIH REDOVA
        # -----------------------------------------------------------
        #
        return completed


    """
    ================================================================
    RESET GRID
    ================================================================

    Briše cijeli grid.

    ================================================================
    """
    def reset(self):

        # -----------------------------------------------------------
        # RESET SVIH ĆELIJA
        # -----------------------------------------------------------
        #
        for row in range(self.num_rows):

            for column in range(self.num_cols):

                self.grid[row][column] = 0


    """
    ================================================================
    DRAW GRID
    ================================================================

    Crta grid na ekran.

    ================================================================
    """
    def draw(self, screen):

        # -----------------------------------------------------------
        # PROLAZ KROZ GRID
        # -----------------------------------------------------------
        #
        for row in range(self.num_rows):

            for column in range(self.num_cols):


                # ---------------------------------------------------
                # CELL VALUE
                # ---------------------------------------------------
                #
                # Vrijednost ćelije:
                #
                # 0 = prazno
                # 1 = zeleni blok
                # 2 = crveni blok
                #
                cell_value = self.grid[row][column]


                # ---------------------------------------------------
                # RECTANGLE
                # ---------------------------------------------------
                #
                # Izračun pixel pozicije.
                #
                cell_rect = pygame.Rect(

                    # X pozicija
                    column * self.cell_size + 11,

                    # Y pozicija
                    row * self.cell_size + 11,

                    # Width
                    self.cell_size - 1,

                    # Height
                    self.cell_size - 1
                )


                # ---------------------------------------------------
                # DRAW CELL
                # ---------------------------------------------------
                #
                pygame.draw.rect(

                    # Surface
                    screen,

                    # Color
                    self.colors[cell_value],

                    # Rectangle
                    cell_rect
                )


"""
====================================================================
KRAJ GRID KLASE
====================================================================

Ova klasa predstavlja:
- game matrix
- collision system
- line clear system
- tile renderer

====================================================================
KLJUČNI GAME DEV SISTEMI
====================================================================

Ovaj kod implementira:

✔ Matrix Based World
✔ Tile Rendering
✔ Collision Detection
✔ Spatial Partitioning
✔ Row Clearing Logic
✔ Occupancy Grid
✔ Boundary Detection

====================================================================
KAKO RADI TETRIS GRID
====================================================================

Grid je:
- 20x10 matrica
- svaki broj predstavlja tile
- 0 = prazno
- ostali brojevi = blokovi

====================================================================
LINE CLEAR ALGORITAM
====================================================================

Proces:

1. Provjeri red
2. Ako je pun:
   - obriši ga
3. Pomjeri sve iznad dole
4. Nastavi dalje

===================================================================
 GAME DEV PATTERN
====================================================================

Ovo je standardni:
- tile map system
- occupancy matrix
- collision grid

Koriste ga:
- Tetris igre
- puzzle igre
- strategy igre
- roguelike igre
- tile based RPG igre

====================================================================
AAA GAME DEV PRINCIPI
====================================================================

Kod koristi:
✔ Separation of Concerns
✔ Modular Design
✔ Reusable Systems
✔ Matrix Architecture
✔ Deterministic Logic

====================================================================
"""