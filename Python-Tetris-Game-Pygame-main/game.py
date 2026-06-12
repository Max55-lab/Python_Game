"""
====================================================================
GAME CLASS
====================================================================

Autor: [Josip Kapular]
Projekt: Advanced Tetris Clone
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ova klasa predstavlja GLAVNI GAME MANAGER (Kontroler) cijele igre.

Game klasa centralizira i upravlja:
- Core gameplay logikom (State & Rules)
- Score i Level sistemom (Progresija)
- Sistemom kretanja i rotacije (Input Translation)
- Detekcijom kolizija (Collision System)
- Randomizacijom i spawnom blokova (Spawn System)
- Sinkronizacijom s UI panelima iz main.py

====================================================================
GAME DEV ARHITEKTURA
====================================================================

Ova klasa je:

CORE GAMEPLAY CONTROLLER

Komunicira sa:
- Grid klasom (Matrica / Polje za igru)
- Blocks modulom (Sve geometrije Tetris figura)
- Colors klasom (Vizualna konfiguracija ćelija)

====================================================================
IMPORTI
====================================================================
"""

# ---------------------------------------------------------------
# LOKALNI MODULI I STRUKTURE PODATAKA
# ---------------------------------------------------------------
from grid import Grid
from blocks import *
from colors import Colors

# ---------------------------------------------------------------
# SISTEMSKI MODULI
# ---------------------------------------------------------------
import random
import pygame


class Game:

    """
    ================================================================
    KONSTRUKTOR KLASE (__init__)
    ================================================================

    Inicijalizira osnovno stanje igre prilikom pokretanja aplikacije.
    Stvara instancu mreže i priprema prve blokove.

    ================================================================
    """
    def __init__(self):

        # Instanciranje mreže igre (10x20 polja)
        self.grid = Grid()

        # Lista dostupnih blokova za random selekciju (7-bag sistem ublažavanja)
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]

        # Postavljanje trenutnog i sljedećeg bloka na osnovu random odabira
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

        # Statusne varijable igre
        self.game_over = False
        self.score = 0
        self.level = 1

        # Dinamičke varijable za sistem rivala / meta (Target UI)
        self.target_score = 0
        self.target_name = ""


    # ---------------------------------------------------------------
    # GET RANDOM BLOCK
    # ---------------------------------------------------------------
    #
    # Bira nasumičan blok iz liste. Ako se lista isprazni,
    # ponovo je puni svim blokovima (Standardni Tetris Randomizer).
    #
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block


    # ---------------------------------------------------------------
    # MOVE LEFT
    # ---------------------------------------------------------------
    #
    # Pomijera blok ulijevo za jednu kolonu. Ako dodiruje zid
    # ili drugi blok, automatski poništava pomjeranje (Undo Pattern).
    #
    def move_left(self):
        if self.game_over:
            return
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)


    # ---------------------------------------------------------------
    # MOVE RIGHT
    # ---------------------------------------------------------------
    #
    # Pomijera blok udesno za jednu kolonu. Sadrži identičan
    # sigurnosni mehanizam provjere granica i kolizije.
    #
    def move_right(self):
        if self.game_over:
            return
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)


    # ---------------------------------------------------------------
    # MOVE DOWN
    # ---------------------------------------------------------------
    #
    # Spušta blok za jedan red naniže (Gravitacija).
    # Ako blok udari u dno ili fiksirani entitet, zaključava se.
    #
    def move_down(self):
        if self.game_over:
            return
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()


    # ---------------------------------------------------------------
    # ROTATE
    # ---------------------------------------------------------------
    #
    # Rotira blok u smjeru kazaljke na satu. Ukoliko rotacija
    # narušava granice grida ili pravi preklapanje, vraća se nazad.
    #
    def rotate(self):
        if self.game_over:
            return
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()


    # ---------------------------------------------------------------
    # HOLD BLOCK
    # ---------------------------------------------------------------
    #
    # Rezervirano za buduću nadogradnju mehanike zamjene blokova.
    #
    def hold_block(self):
        pass


    # ---------------------------------------------------------------
    # HARD DROP
    # ---------------------------------------------------------------
    #
    # Instantno spušta blok na najnižu moguću poziciju u grideru
    # koristeći brzu while petlju provjere kolizije.
    #
    def hard_drop(self):
        while not self.game_over:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_block()
                break


    # ---------------------------------------------------------------
    # BLOCK INSIDE
    # ---------------------------------------------------------------
    #
    # Validira da li se sve ćelije trenutnog bloka nalaze
    # unutar dozvoljenih dimenzija matrice (Grid Boundary Check).
    #
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True


    # ---------------------------------------------------------------
    # BLOCK FITS
    # ---------------------------------------------------------------
    #
    # Provjerava da li su polja na koja blok pokušava stupiti
    # prazna (Vrijednost 0). Služi za detekciju kolizije sa starim blokovima.
    #
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True


    # ---------------------------------------------------------------
    # LOCK BLOCK
    # ---------------------------------------------------------------
    #
    # Trajno utiskuje ID trenutnog bloka u matricu (Grid),
    # vrši zamjenu sa sljedećim i provjerava Game Over uslov.
    #
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            self.grid.grid[tile.row][tile.column] = self.current_block.id

        # Tranzicija blokova (Queue sistem)
        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        # Ako novi spawn blok odmah pravi koliziju -> Kraj Igre
        if not self.block_fits():
            self.game_over = True


    # ---------------------------------------------------------------
    # GET FULL ROWS
    # ---------------------------------------------------------------
    #
    # Skenira matricu i vraća listu indeksa svih redova
    # koji su u potpunosti popunjeni blokovima.
    #
    def get_full_rows(self):
        full_rows = []
        for row in range(self.grid.num_rows):
            if self.grid.is_row_full(row):
                full_rows.append(row)
        return full_rows


    # ---------------------------------------------------------------
    # CLEAR LINES
    # ---------------------------------------------------------------
    #
    # Poziva brisanje popunjenih redova, ažurira bodove i
    # dinamički podiže nivo igre na svakih osvojenih 500 bodova.
    #
    def clear_lines(self):
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared)

        # Proračun nivoa za dinamičko ubrzanje (main.py preuzima ovaj podatak)
        self.level = (self.score // 500) + 1


    # ---------------------------------------------------------------
    # UPDATE SCORE
    # ---------------------------------------------------------------
    #
    # Klasični arkadni sistem bodovanja u zavisnosti od broja
    # istovremeno očišćenih linija (Nagrađivanje "Tetris" poteza).
    #
    def update_score(self, rows_cleared):
        if rows_cleared == 1:
            self.score += 100
        elif rows_cleared == 2:
            self.score += 300
        elif rows_cleared == 3:
            self.score += 500
        elif rows_cleared == 4:
            self.score += 800


    # ---------------------------------------------------------------
    # SET NEXT TARGET (RIVAL SYSTEM)
    # ---------------------------------------------------------------
    #
    # Skenira High Score tabelu i pronalazi igrača koji je direktno
    # iznad trenutnog rezultata korisnika, stvarajući motivacijsku metu.
    #
    def set_next_target(self, scores):
        if not scores:
            self.target_score = 1000
            self.target_name = "Be first!"
            return

        for entry in scores:
            if entry["score"] > self.score:
                self.target_score = entry["score"]
                self.target_name = entry["name"]
                return

        # Ako je igrač prešao sve rezultate iz JSON-a
        self.target_score = 0
        self.target_name = "Top player!"


    # ---------------------------------------------------------------
    # RESET
    # ---------------------------------------------------------------
    #
    # Vraća sve parametre na fabrička podešavanja. Koristi se
    # prilikom tranzicije iz Menija u novu igru nakon poraza.
    #
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.level = 1
        self.game_over = False


    """
    ================================================================
    DRAW PIPELINE
    ================================================================

    Iscrtava isključivo aktivne komponente gameplay-a:
    1. Grid (fiksirane blokove u matrici)
    2. Current Block (upravljivi aktivni blok sa offsetom)

    ================================================================
    ZAŠTO OVAKAV PRISTUP?
    ================================================================
    
    Ova metoda crta samo unutar koordinata (11, 11) čime čuva 
    "Separation of Concerns" princip. Tekstualne panele i stanja 
    menija prepušta glavnoj petlji u main.py.

    ================================================================
    """
    def draw(self, screen):
        # Iscrtavanje statične mreže
        self.grid.draw(screen)

        # Iscrtavanje aktivnog bloka sa pomakom od 11px radi margina prozora
        self.current_block.draw(screen, 11, 11)


"""
====================================================================
KRAJ FILE-A
====================================================================

Game klasa uspješno izoluje matematičku logiku Tetrisa od samog
prozora i stanja menadžmenta aplikacije.

====================================================================
"""