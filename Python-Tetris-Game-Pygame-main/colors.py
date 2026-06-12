"""
====================================================================
COLORS CLASS
====================================================================

Autor: [Josip Kapular]
Projekt: Tetris / Grid Based Game
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ova klasa sadrži sve boje koje se koriste u igri.

Glavni cilj ove klase je:
- centralizacija boja
- lakša organizacija
- lakše mijenjanje dizajna igre
- clean architecture

Umjesto da pišemo boje direktno u kodu:

    (255, 0, 0)

koristimo:

    Colors.red

To čini kod:
- čitljivijim
- lakšim za održavanje

====================================================================
GAME DEV KONCEPT
====================================================================

Ovo je:
- Utility Class
- Static Data Container
- Visual Configuration System

====================================================================
RGB SISTEM
====================================================================

Sve boje koriste RGB format:

(R, G, B)

R = Red
G = Green
B = Blue

Vrijednosti idu:
0 -> 255

Primjeri:

(255, 0, 0)
= čista crvena

(0, 255, 0)
= čista zelena

(0, 0, 255)
= čista plava

====================================================================
KLASA
====================================================================
"""
class Colors:

    # ---------------------------------------------------------------
    # DARK GREY
    # ---------------------------------------------------------------
    #
    # Tamno siva boja.
    #
    # Koristi se za:
    # - background
    # - prazna polja
    # - UI elementi
    #
    dark_grey = (26, 31, 40)


    # ---------------------------------------------------------------
    # GREEN
    # ---------------------------------------------------------------
    #
    # Zelena boja.
    #
    # Koristi se za:
    # - jedan od Tetris blokova
    #
    green = (83, 218, 63)


    # ---------------------------------------------------------------
    # RED
    # ---------------------------------------------------------------
    #
    # Crvena boja.
    #
    # Koristi se za:
    # - jedan od blokova
    # - moguće error state
    #
    red = (234, 20, 28)


    # ---------------------------------------------------------------
    # ORANGE
    # ---------------------------------------------------------------
    #
    # Narandžasta boja.
    #
    orange = (254, 72, 25)


    # ---------------------------------------------------------------
    # YELLOW
    # ---------------------------------------------------------------
    #
    # Žuta boja.
    #
    yellow = (254, 251, 52)


    # ---------------------------------------------------------------
    # PINK
    # ---------------------------------------------------------------
    #
    # Pink boja.
    #
    pink = (255, 29, 206)


    # ---------------------------------------------------------------
    # CYAN
    # ---------------------------------------------------------------
    #
    # Svijetlo plava / cyan boja.
    #
    # Veoma često korištena za:
    # - I Block u Tetrisu
    #
    cyan = (1, 237, 250)


    # ---------------------------------------------------------------
    # BLUE
    # ---------------------------------------------------------------
    #
    # Plava boja.
    #
    blue = (255, 157, 0)


    # ---------------------------------------------------------------
    # WHITE
    # ---------------------------------------------------------------
    #
    # Bijela boja.
    #
    # Koristi se za:
    # - tekst
    # - UI
    # - outline
    #
    white = (255, 255, 255)


    # ---------------------------------------------------------------
    # DARK BLUE
    # ---------------------------------------------------------------
    #
    # Tamno plava boja.
    #
    # Može se koristiti za:
    # - background
    # - panel
    # - UI
    #
    dark_blue = (72, 93, 197)


    # ---------------------------------------------------------------
    # LIGHT BLUE
    # ---------------------------------------------------------------
    #
    # Svjetlija plava.
    #
    # Dobra za:
    # - hover efekte
    # - UI highlights
    #
    light_blue = (59, 85, 162)


    """
    ================================================================
    GET CELL COLORS
    ================================================================

    Ova metoda vraća listu boja za Tetris blokove.

    Koristi se u Block klasi:

        self.colors = Colors.get_cell_colors()

    ================================================================
    ZAŠTO CLASSMETHOD?
    ================================================================

    @classmethod omogućava:
    - pristup klasnim varijablama
    - bez kreiranja objekta

    Možemo pozvati:

        Colors.get_cell_colors()

    bez:

        colors = Colors()

    ================================================================
    """
    @classmethod
    def get_cell_colors(cls):

        # -----------------------------------------------------------
        # VRATI LISTU BOJA
        # -----------------------------------------------------------
        #
        # Redoslijed je VEOMA važan.
        #
        # Block ID koristi indeks:
        #
        # id = 1 -> green
        # id = 2 -> red
        # itd.
        #
        # Primjer:
        #
        # self.colors[self.id]
        #
        # Ako je:
        # self.id = 3
        #
        # dobijemo:
        # orange
        #
        return [

            # -------------------------------------------------------
            # INDEX 0
            # -------------------------------------------------------
            #
            # Tamno siva
            # često predstavlja:
            # - empty cell
            # - background tile
            #
            cls.dark_grey,


            # -------------------------------------------------------
            # INDEX 1
            # -------------------------------------------------------
            #
            # Green block
            #
            cls.green,


            # -------------------------------------------------------
            # INDEX 2
            # -------------------------------------------------------
            #
            # Red block
            #
            cls.red,


            # -------------------------------------------------------
            # INDEX 3
            # -------------------------------------------------------
            #
            # Orange block
            #
            cls.orange,


            # -------------------------------------------------------
            # INDEX 4
            # -------------------------------------------------------
            #
            # Yellow block
            #
            cls.yellow,


            # -------------------------------------------------------
            # INDEX 5
            # -------------------------------------------------------
            #
            # Pink block
            #
            cls.pink,


            # -------------------------------------------------------
            # INDEX 6
            # -------------------------------------------------------
            #
            # Cyan block
            #
            cls.cyan,


            # -------------------------------------------------------
            # INDEX 7
            # -------------------------------------------------------
            #
            # Blue block
            #
            cls.blue
        ]


"""
====================================================================
KRAJ FILE-A
====================================================================

Ova klasa služi kao centralni color management sistem.

Prednosti ovog pristupa:

✔ Lakše održavanje
✔ Lakše mijenjanje teme igre
✔ Čistiji kod
✔ Reusable design

====================================================================
KAKO SE KORISTI
====================================================================

Primjer:

    background = Colors.dark_grey

ili:

    pygame.draw.rect(screen, Colors.red, rect)


====================================================================
GAME DEV ARHITEKTURA
====================================================================

Ova klasa pripada:

VISUAL / CONFIG LAYER-u

Koriste je:
- Block sistem
- UI sistem
- Rendering sistem
- Effects sistem

====================================================================
 GAME DEV PATTERN
====================================================================

Ovo je standardni pattern u game developmentu:

- centralized configuration
- static utility classes
- reusable visual systems

Koriste ga:
- indie igre
- AAA igre
- UI sistemi
- game engines

====================================================================
"""