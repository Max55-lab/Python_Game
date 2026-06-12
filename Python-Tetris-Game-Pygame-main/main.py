"""
====================================================================
MAIN DRIVER FILE
====================================================================

Autor: [Josip Kapular]
Projekt: Advanced Tetris Clone
Engine: Pygame
Jezik: Python

====================================================================
OPIS
====================================================================

Ova datoteka je GLAVNA POKRETAČKA TAČKA (Entry Point) cijele igre.

Main datoteka upravlja:
- inicijalizacijom podsistema (Pygame, Mixer)
- konfiguracijom prozora i FPS-a
- State Machine-om (upravljanje stanjima igre)
- glavnom petljom (Main Game Loop)
- obradom korisničkog unosa (Event Handling)
- renderovanjem UI panela i animacija

====================================================================
GAME DEV ARHITEKTURA
====================================================================

Ova klasa je:

APPLICATION ENTRY POINT & TOP-LEVEL CONTROLLER

Komunicira sa:
- Game klasom (Core Gameplay)
- Colors klasom (Visual Config)
- Datotečnim sistemom (JSON High Score)

====================================================================
IMPORTI
====================================================================
"""

# ---------------------------------------------------------------
# SISTEMSKI MODULI
# ---------------------------------------------------------------
import pygame
import sys
import json
import os

# ---------------------------------------------------------------
# LOKALNI MODULI (PROJEKTNE KLASE)
# ---------------------------------------------------------------
from game import Game
from colors import Colors

# ==============================================================================
# INICIJALIZACIJA PODSISTEMA
# ==============================================================================
#
# Pokrećemo osnovne Pygame module za grafiku, unos i zvuk.
# Inicijalizacija mixera je izdvojena radi stabilnosti audio kanala.
#
pygame.init()
pygame.mixer.init()


# ==============================================================================
# UPRAVLJANJE ZVUKOM (ROBUSTNOST)
# ==============================================================================
#
# Funkcija za pokretanje pozadinske muzike.
#
# GRACEFUL DEGRADATION PATTERN:
# Ako datoteka sa zvukom nedostaje ili je audio kartica zauzeta,
# try-except blok sprječava crash aplikacije i omogućava nastavak igre u tišini.
#
def start_music():
    try:
        # Konstrukcija apsolutne putanje do audio zapisa
        base_dir = str(os.path.dirname(__file__))
        music_path = os.path.join(base_dir, "Sounds", "music.ogg")

        # Provjera postojanja datoteke prije učitavanja
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            # Parametar -1 postavlja beskonačni loop (ponavljanje)
            pygame.mixer.music.play(-1)
            # Postavka umjerene glasnoće (40%)
            pygame.mixer.music.set_volume(0.4)
    except (pygame.error, OSError):
        # Ignorisanje greške radi očuvanja stabilnosti izvršavanja
        pass


# Pokretanje audio podsistema pri startu aplikacije
start_music()

# ==============================================================================
# CONFIGURATION PANEL (EKRAN, FONTOVI, LOGIKA)
# ==============================================================================
#
# Postavke grafičkog prozora, tipografije i instanciranje kontrolera.
#
# DIMENZIJE PROZORA:
# Širina: 500px (Matrica igre zauzima 300px + 200px za UI panel i margine)
# Visina: 620px (Matrica igre 600px + gornja/donja margina)
#
title_font = pygame.font.Font(None, 60)  # Primarni font za naslove i Game Over
small_font = pygame.font.Font(None, 35)  # Sekundarni font za statistiku i UI panele

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

# Sinhronizacijski sat za ograničavanje frekvencije osvježavanja (FPS)
clock = pygame.time.Clock()

# Instanciranje glavnog menadžera gameplay logike
game = Game()

# ==============================================================================
# STATE MACHINE (UPRAVLJANJE STANJIMA)
# ==============================================================================
#
# finite State Machine (FSM) Pattern se koristi umjesto komplikovanih ugniježđenih 
# uslova. Svaki segment aplikacije je izolovan kroz jedinstveno stanje.
#
MENU = 0  # Glavni meni igre
PLAYING = 1  # Aktivni gameplay
NAME_INPUT = 2  # Unos korisničkog imena nakon poraza
HIGH_SCORES = 3  # Prikaz tabele sa najboljim rezultatima
CLEARING = 4  # Privremeno stanje za animaciju brisanja redova
PAUSE = 5  # Stanje pauzirane igre
RESULT_SCREEN = 6  # Prikaz ostvarenog ranga na ljestvici

# Početno stanje aplikacije postavlja se na Glavni Meni
game_state = MENU

# ==============================================================================
# GLOBALNE VARIJABLE STANJA
# ==============================================================================
#
# Pomoćne varijable koje prate tajminge, unose i podatke o sesiji.
#
clearing_timer = 0  # Timestamp početka animacije brisanja reda
rows_to_flash = []  # Lista indeksa redova koji trenutno trepere
player_name = ""  # String bafer za unos imena igrača
final_score = 0  # Keširani finalni rezultat postignut u tekućoj partiji
final_rank = 0  # Izračunata pozicija na tabeli nakon završetka partije

# ==============================================================================
# TAJMER DOGAĐAJA (GAME TICKER)
# ==============================================================================
#
# Koristimo Pygame Event sistem za upravljanje gravitacijom blokova.
# Umjesto nepreciznog delta-time računanja, okidamo prilagođeni korisnički događaj.
#
GAME_UPDATE = pygame.USEREVENT
speed = 500  # Inicijalna brzina padanja: 500 milisekundi
pygame.time.set_timer(GAME_UPDATE, speed)


# ==============================================================================
# HIGH SCORE SUSTAV (PERSISTENCE LAYER)
# ==============================================================================
#
# Rukovanje podacima na disku kroz JSON format.
#
# ------------------------------------------------------------------------------
# LOAD SCORES
# ------------------------------------------------------------------------------
def load_scores():
    """Učitava tabelu rezultata iz lokalne JSON datoteke."""
    if not os.path.exists("scores.json"):
        return []
    with open("scores.json", "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, IOError):
            # U slučaju korumpirane datoteke, vraća se prazna lista (anti-crash osiguranje)
            return []


# ------------------------------------------------------------------------------
# SAVE SCORE
# ------------------------------------------------------------------------------
def save_score(name, score):
    """
    Sprema novi rezultat u bazu, sortira tabelu silazno i vraća osvojeni rang.
    Ograničava tabelu na top unose radi optimizacije prostora.
    """
    scores = load_scores()
    scores.append({"name": name, "score": score})

    # Sortiranje tabele silazno prema 'score' vrijednosti ključa
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f)

    # Linearna pretraga radi utvrđivanja tačnog ranga (indeks + 1)
    for rank_index, s in enumerate(scores):
        if s["name"] == name and s["score"] == score:
            return rank_index + 1
    return len(scores)


# ==============================================================================
# GLAVNA PETLJA (MAIN GAME LOOP)
# ==============================================================================
#
# Pokreće se frekvencijom definisanom preko clock.tick() i izvršava tri osnovne faze:
# 1. Event Handling (Obrada ulaza) -> 2. Game Update (Logika) -> 3. Rendering (Crtanje)
#
while True:

    # --------------------------------------------------------------------------
    # FAZA 1: EVENT HANDLING (OBRADA ULREZNOG SUSTAVA)
    # --------------------------------------------------------------------------
    for event in pygame.event.get():

        # Globalni uslov za prekid izvršavanja i sigurno gašenje aplikacije
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ----------------------------------------------------------------------
        # KONTROLE: MENU STATE
        # ----------------------------------------------------------------------
        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Resetovanje stanja objekta igre i postavljanje meta iz baze
                    game.reset()
                    game.set_next_target(load_scores())
                    speed = 500
                    pygame.time.set_timer(GAME_UPDATE, speed)
                    game_state = PLAYING
                elif event.key == pygame.K_h:
                    game_state = HIGH_SCORES

        # ----------------------------------------------------------------------
        # KONTROLE: PLAYING STATE
        # ----------------------------------------------------------------------
        elif game_state == PLAYING:
            # DINAMIČKI LEVEL SPEED SUSTAV:
            # Formula progresivno ubrzava igru za 40ms po nivou. Granica brzine je 100ms.
            new_speed = max(100, 500 - (game.level - 1) * 40)
            if new_speed != speed:
                speed = new_speed
                pygame.time.set_timer(GAME_UPDATE, speed)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = PAUSE
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_c:
                    game.hold_block()
                if event.key == pygame.K_SPACE:
                    game.hard_drop()

            # Automatsko spuštanje bloka pod uticajem tajmera igre
            if event.type == GAME_UPDATE:
                game.move_down()

            # Dinamičko ažuriranje Target Score sistema tokom igranja
            if 0 < game.target_score <= game.score:
                game.set_next_target(load_scores())

            # Presretanje i detekcija punih redova prije nego što se zaključaju
            if game.get_full_rows():
                rows_to_flash = game.get_full_rows()
                clearing_timer = pygame.time.get_ticks()
                game_state = CLEARING

            # Provjera tranzicije u poraz (Game Over)
            if game.game_over:
                final_score = game.score
                game_state = NAME_INPUT
                player_name = ""

        # ----------------------------------------------------------------------
        # KONTROLE: CLEARING STATE
        # ----------------------------------------------------------------------
        elif game_state == CLEARING:
            # Blokira unos i čeka 300ms da završi vizuelni efekt bljeska
            if pygame.time.get_ticks() - clearing_timer > 300:
                game.clear_lines()
                game_state = PLAYING

        # ----------------------------------------------------------------------
        # KONTROLE: NAME INPUT STATE
        # ----------------------------------------------------------------------
        elif game_state == NAME_INPUT:
            if event.type == pygame.KEYDOWN:
                # Strip() onemogućava registraciju imena sastavljenih isključivo od razmaka
                if event.key == pygame.K_RETURN and player_name.strip():
                    final_rank = save_score(player_name, final_score)
                    game_state = RESULT_SCREEN
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    # Prihvatamo isključivo karaktere koji se mogu ispisati na ekranu
                    if len(player_name) < 10 and event.unicode.isprintable():
                        player_name += event.unicode

        # ----------------------------------------------------------------------
        # KONTROLE: PAUSE STATE
        # ----------------------------------------------------------------------
        elif game_state == PAUSE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game_state = PLAYING

        # ----------------------------------------------------------------------
        # KONTROLE: RESULT SCREEN STATE
        # ----------------------------------------------------------------------
        elif game_state == RESULT_SCREEN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = MENU

        # ----------------------------------------------------------------------
        # KONTROLE: HIGH SCORES STATE
        # ----------------------------------------------------------------------
        elif game_state == HIGH_SCORES:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = MENU

    # --------------------------------------------------------------------------
    # FAZA 2 & 3: RENDEROVANJE I GRAFIČKI PIPELINE
    # --------------------------------------------------------------------------
    # Čišćenje ekrana baznom bojom kako bi se izbjegao ghosting efekat prethodnog okvira
    screen.fill(Colors.dark_blue)

    # ----------------------------------------------------------------------
    # RENDERING: MENU STATE
    # ----------------------------------------------------------------------
    if game_state == MENU:
        screen.blit(title_font.render("TETRIS", True, Colors.white), (170, 250))
        screen.blit(small_font.render("ENTER to Play, H for Scores", True, Colors.white), (80, 350))

    # ----------------------------------------------------------------------
    # RENDERING: GAMEPLAY MODES (PLAYING, CLEARING, PAUSE)
    # ----------------------------------------------------------------------
    elif game_state in [PLAYING, CLEARING, PAUSE]:
        # Iscrtavanje pozadinskih kontejnera za UI panele sa zaobljenim ivicama (border_radius=10)
        pygame.draw.rect(screen, Colors.light_blue, (320, 20, 170, 100), 0, 10)  # Panel: Score/Level
        pygame.draw.rect(screen, Colors.light_blue, (320, 150, 170, 130), 0, 10)  # Panel: Next Piece
        pygame.draw.rect(screen, Colors.light_blue, (320, 320, 170, 130), 0, 10)  # Panel: Hold Piece
        pygame.draw.rect(screen, Colors.light_blue, (320, 460, 170, 130), 0, 10)  # Panel: Target Leader

        # Iscrtavanje statičnih labela unutar panela
        screen.blit(small_font.render("Next", True, Colors.white), (370, 160))
        screen.blit(small_font.render("Hold", True, Colors.white), (370, 330))
        screen.blit(small_font.render("Score", True, Colors.white), (370, 30))

        # Prikaz dinamičke statistike izvučene iz Game objekta
        screen.blit(small_font.render(str(game.score), True, Colors.white), (380, 60))
        screen.blit(small_font.render(f"Lvl: {game.level}", True, Colors.white), (365, 90))

        # Renderovanje ciljnog rezultata (Igrač iznad trenutnog ranga korisnika)
        screen.blit(small_font.render("Target:", True, Colors.white), (360, 470))
        if game.target_score > 0:
            screen.blit(small_font.render(game.target_name, True, Colors.yellow), (350, 500))
            screen.blit(small_font.render(str(game.target_score), True, Colors.white), (370, 530))
        else:
            screen.blit(small_font.render("Top player!", True, Colors.green), (350, 500))

        # Delegiranje crtanja aktivne mreže (grida) i trenutnog bloka podsistemu igre
        game.draw(screen)

        # RENDER ANIMACIJE ČIŠĆENJA:
        # Kreira se privremena transparentna površina (SRCALPHA) koja linearno
        # gubi prozirnost (fade-out efekat) kroz vrijeme trajanja animacije.
        if game_state == CLEARING:
            elapsed = pygame.time.get_ticks() - clearing_timer
            alpha = max(0, 255 - int((elapsed / 300) * 255))
            flash_surf = pygame.Surface((300, 30), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, alpha))
            for row in rows_to_flash:
                screen.blit(flash_surf, (11, row * 30 + 11))

        # Overlay tekst preko zamrznutog ekrana kada je aktivna pauza
        if game_state == PAUSE:
            screen.blit(title_font.render("PAUSED", True, Colors.white), (170, 300))

    # ----------------------------------------------------------------------
    # RENDERING: NAME INPUT STATE
    # ----------------------------------------------------------------------
    elif game_state == NAME_INPUT:
        screen.blit(title_font.render("GAME OVER", True, Colors.white), (120, 150))
        screen.blit(small_font.render(f"Score: {final_score}", True, Colors.white), (180, 210))
        screen.blit(small_font.render("Enter Name:", True, Colors.white), (180, 260))
        screen.blit(title_font.render(player_name + "|", True, Colors.yellow), (150, 300))

    # ----------------------------------------------------------------------
    # RENDERING: RESULT SCREEN STATE
    # ----------------------------------------------------------------------
    elif game_state == RESULT_SCREEN:
        # Uslovna evaluacija boje teksta u zavisnosti od ostvarenog plasmana
        color = Colors.green if final_rank <= 10 else Colors.red
        msg = "TOP 10!" if final_rank <= 10 else "Not in Top 10"
        screen.blit(title_font.render(msg, True, color), (125, 200))
        screen.blit(small_font.render(f"Your rank: {final_rank}. place", True, Colors.white), (120, 300))
        screen.blit(small_font.render("Press ENTER", True, Colors.light_blue), (170, 400))

    # ----------------------------------------------------------------------
    # RENDERING: HIGH SCORES STATE
    # ----------------------------------------------------------------------
    elif game_state == HIGH_SCORES:
        screen.blit(title_font.render("TOP 10 SCORES", True, Colors.white), (100, 50))
        # Slicing operator [:10] osigurava prikaz maksimalno top 10 rezultata
        for score_index, entry in enumerate(load_scores()[:10]):
            txt = small_font.render(f"{score_index + 1}. {entry['name']} - {entry['score']}", True, Colors.white)
            screen.blit(txt, (100, 120 + score_index * 40))
        screen.blit(small_font.render("ESC to Back", True, Colors.light_blue), (170, 560))

    # Prijenos bafera na fizički ekran računara (Double Buffering osvježavanje)
    pygame.display.update()

    # Ograničavanje brzine izvršavanja na stabilnih 60 sličica u sekundi (FPS)
    clock.tick(60)

# noinspection PyUnreachableCode
"""
====================================================================
KRAJ FILE-A
====================================================================

Ova skripta povezuje sve engine sisteme u funkcionalnu cjelinu.

====================================================================
"""