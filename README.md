TETRIS GAME (PYTHON)
====================

Autor: Josip Kapular
Platforma: Python (Pygame)
Tip: 2D igra (Tetris klon)

---

## 📌 OPIS PROJEKTA

Ovo je implementacija klasične Tetris igre napravljena u Pythonu koristeći Pygame biblioteku.

Cilj igre je slagati padajuće blokove (tetrominoe) tako da se popune horizontalne linije. Kada se linija popuni, ona nestaje, a igrač dobiva bodove.

Igra uključuje:

* Menu sustav
* Glavni gameplay loop
* Score sustav
* Next block preview
* HOLD funkcionalnost
* Game Over screen

---
📌 UVOD
=======

Ovaj dokument opisuje razvoj projekta kroz više iteracija.
Svaka iteracija predstavlja poboljšanje funkcionalnosti, dizajna ili stabilnosti igre.

----

## 🎮 KAKO POKRENUTI IGRU

1. Instalirati Python

2. Instalirati Pygame:

   pip install pygame

3. Pokrenuti:

   python main.py

---

## 🎮 KONTROLE

LEFT ARROW   → lijevo
RIGHT ARROW  → desno
DOWN ARROW   → brže dolje
UP ARROW     → rotacija

C ili SHIFT → HOLD

ESC → izlaz

---


## 🎮 GAMEPLAY MEHANIKA

* Gravity: blok automatski pada
* Lock system: blok se zaključava
* Line clear: puni redovi nestaju
* Spawn system: novi blok dolazi

---

## 🎯 KAKO IGRATI (TUTORIAL)

1. Slagati blokove u linije
2. Popunjene linije nestaju
3. Izbjegavati rupe
4. Planirati unaprijed koristeći NEXT blok

---

## 🧠 STRATEGIJA

* Drži površinu ravnom
* Koristi I-blok za velike bodove
* Pametno koristi HOLD
* Ne rotiraj blokove prekasno

---

## 📈 SCORE SISTEM

Bodovi se dobivaju za:

* brisanje linija
* više linija odjednom

---
======================================
🔹 ITERACIJA 1 - OSNOVNA STRUKTURA
==================================

OPIS:

* Kreiran osnovni Python projekt
* Implementiran Pygame prozor
* Postavljen game loop

DODANO:

* inicijalizacija pygame
* osnovni render screen-a

PROBLEM:

* nema gameplay logike

NAUČENO:

* kako radi game loop (while loop + FPS)

---

# 🔹 ITERACIJA 2 - GRID I BLOKOVI

OPIS:

* Implementiran grid sustav (matrica)
* Dodani prvi blokovi

DODANO:

* 2D lista za grid
* prikaz blokova na ekranu

PROBLEM:

* blokovi ne reagiraju na input

NAUČENO:

* rad s matricama

---

# 🔹 ITERACIJA 3 - KONTROLE

OPIS:

* Dodane kontrole za pomicanje blokova

DODANO:

* lijevo/desno kretanje
* rotacija

PROBLEM:

* blokovi prolaze kroz zid

NAUČENO:

* event handling u pygame

---

# 🔹 ITERACIJA 4 - KOLIZIJA

OPIS:

* Implementirana detekcija sudara

DODANO:

* provjera granica
* provjera sudara s drugim blokovima

PROBLEM:

* bugovi pri rotaciji

NAUČENO:

* logika sudara

---

# 🔹 ITERACIJA 5 - LINE CLEAR

OPIS:

* Dodano brisanje linija

DODANO:

* provjera punih redova
* uklanjanje reda

PROBLEM:

* pomicanje grid-a nakon brisanja

NAUČENO:

* manipulacija listama

---

# 🔹 ITERACIJA 6 - SCORE

OPIS:

* Implementiran score sustav

DODANO:

* bodovi za linije

---

# 🔹 ITERACIJA 7 - NEXT BLOK

OPIS:

* Prikaz sljedećeg bloka

DODANO:

* preview sustav

---

# 🔹 ITERACIJA 8 - HOLD SISTEM

OPIS:

* Implementiran HOLD blok

DODANO:

* spremanje bloka
* zamjena

PROBLEM:

* HOLD i NEXT UI se preklapaju

---

# 🔹 ITERACIJA 9 - UI POPRAVCI

OPIS:

* Popravljen layout

DODANO:

* razdvojeni UI elementi

---

# 🔹 ITERACIJA 10 - GAME OVER

OPIS:

* Implementirana detekcija kraja igre

DODANO:

* provjera spawn pozicije

---

# 🔹 ITERACIJA 11 - FINALNA VERZIJA

OPIS:

* Stabilizacija projekta

DODANO:

* bug fix
* poboljšanja performansi

======================================
🧠 ZAKLJUČAK RAZVOJA
====================

Projekt je razvijan iterativno kroz:

* testiranje
* detekciju grešaka
* optimizaciju

Svaka iteracija je unaprijedila:

* funkcionalnost
* stabilnost
* korisničko iskustvo

---

## 🧠 LOGIKA IGRE

Igra radi na principu:

1. Blok (tetromino) pada s vrha
2. Igrač ga može:

   * pomaknuti lijevo/desno
   * rotirati
   * ubrzati pad
3. Kada blok dotakne dno ili drugi blok → "zaključava" se
4. Ako se popuni red → briše se
5. Igra završava kada nema mjesta za novi blok

---
## ⚙️ STRUKTURA PROJEKTA

Glavne datoteke:

* main.py
  -> upravlja game state-ovima (MENU, PLAYING, GAME OVER)

* game.py
  -> glavna logika igre (grid, blokovi, kolizije)

* colors.py
  -> definicija boja

* ostale datoteke:
  -> mogu sadržavati logiku za score, blokove itd.

---

## 🔄 ITERACIJE I POBOLJŠANJA

Tijekom razvoja napravljene su sljedeće izmjene:

1. ✅ Dodan GAME STATE sustav

   * MENU
   * PLAYING
   * GAME OVER

2. ✅ Poboljšan UI

   * naslov igre
   * score prikaz
   * "Next" blok prikaz

3. ✅ Implementiran HOLD sistem

   * igrač može spremiti jedan blok
   * zamjena se može koristiti strateški

4. ⚠️ Problem (ispravljen):
   HOLD i NEXT blok su se vizualno preklapali

   ✔ RJEŠENJE:

   * razdvojene pozicije renderiranja
   * dodan padding između UI elemenata

5. ✅ Poboljšan layout

   * jasnije odvojeni elementi:

     * grid
     * next
     * hold
     * score

6. ✅ Game Over logika

   * detekcija kada blok više ne može spawnati

---

## 🎮 KAKO POKRENUTI IGRU

1. Instaliraj Python

2. Instaliraj Pygame:

   pip install pygame

3. Pokreni:

   python main.py

---

## 🎮 KONTROLE

TIPKE:

⬅️ LEFT ARROW   → pomak lijevo
➡️ RIGHT ARROW  → pomak desno
⬇️ DOWN ARROW   → brži pad
⬆️ UP ARROW     → rotacija

C ili SHIFT → HOLD blok

ESC → izlaz iz igre

---

## 🎯 KAKO IGRATI (TUTORIAL)

1. Blokovi padaju s vrha ekrana
2. Tvoj cilj je slagati ih u pune linije
3. Kada napraviš pun red → nestaje
4. Što više redova očistiš → veći score

💡 SAVJETI:

* Ne ostavljaj "rupe" (praznine)
* Drži ravnu površinu
* Koristi HOLD pametno
* Planiraj unaprijed gledajući NEXT blok

---

## 🧩 HOLD MEHANIKA (VAŽNO)

* Možeš spremiti trenutni blok
* Možeš ga zamijeniti kasnije
* Ne možeš spamati HOLD bez postavljanja bloka

➡ Ovo dodaje strategiju igri!

---

## 📈 SCORE SISTEM

Dobivaš bodove za:

* brisanje linija
* više linija odjednom = više bodova

---

## 🚀 MOGUĆA NADOGRADNJA

Ako želiš unaprijediti projekt:

* dodati zvukove
* dodati level system
* povećati brzinu kroz vrijeme
* dodati highscore file
* animacije brisanja linija
* ghost piece (shadow gdje blok pada)

---

## 💡 ZAKLJUČAK

Ovaj projekt je dobra demonstracija:

* rada s Pygame-om
* upravljanja game loop-om
* organizacije koda
* logike kolizija i grid sustava

Također pokazuje kako se kroz iteracije može poboljšavati:

* UI
* gameplay
* struktura koda

---
--------------------------------------
🐞 POZNATI PROBLEMI (KNOWN BUGS)
--------------------------------------

- HOLD i NEXT UI se može preklopiti u određenim rezolucijama
- Rotacija bloka uz zid ponekad ne radi (nema wall-kick logike)
- Brzina igre ne raste progresivno (nema level sistema)


--------------------------------------
🧩 TETROMINO OBLICI
--------------------------------------

Postoji 7 tipova blokova:
- I (linija)
- O (kvadrat)
- T
- S
- Z
- J
- L

Svaki blok ima svoje rotacije i ponašanje.

--------------------------------------
⚙️ TEHNIČKI DETALJI
--------------------------------------

- Grid je implementiran kao 2D lista
- Kolizije se provjeravaju prije svakog pomaka
- Blokovi se renderiraju kao matrice
- Game loop koristi FPS kontrolu (pygame.time.Clock)

--------------------------------------
🎮 GAMEPLAY MEHANIKA
--------------------------------------

- Gravity: blok automatski pada
- Lock delay: blok se zaključava nakon dodira
- Line clear: puni redovi se brišu
- Spawn system: novi blok dolazi nakon zaključavanja


--------------------------------------
🧪 TESTIRANJE
--------------------------------------

Igra je testirana kroz:
- manualno igranje
- provjeru kolizija
- testiranje UI layout-a
- edge case: pun grid

--------------------------------------
🛠️ KAKO MODIFICIRATI IGRU
--------------------------------------

- brzina igre → promjena tick rate-a
- veličina grid-a → izmjena matrice
- novi blokovi → dodavanje u listu tetrominoa

--------------------------------------
📦 VERZIJE
--------------------------------------

v1.0 - osnovna igra
v1.1 - dodan score
v1.2 - dodan NEXT blok
v1.3 - dodan HOLD
v1.4 - poboljšan UI

--------------------------------------
🧱 GRID PRIKAZ
--------------------------------------

| . . . . . . . . . . |
| . . . . X X . . . . |
| . . . X X . . . . . |
| . . . . . . . . . . |

X = blok
. = prazno

START
  ↓
SPAWN BLOK
  ↓
INPUT (player)
  ↓
CHECK COLLISION
  ↓
MOVE / LOCK
  ↓
CLEAR LINES?
  ↓
GAME OVER?

while game_running:
    handle_input()
    move_block_down()
    
    if collision:
        lock_block()
        clear_lines()
        spawn_new_block()


        --------------------------------------
⚠️ ERROR HANDLING
--------------------------------------

- sprječava izlazak bloka iz grid-a
- provjera sudara prije pomaka
- zaštita od spawn overflow-a


--------------------------------------
🚧 LIMITACIJE
--------------------------------------

- nema multiplayera
- nema AI igrača
- nema spremanja igre

## 🧮 PSEUDOKOD

while game_running:
handle_input()
move_block_down()

```
if collision:
    lock_block()
    clear_lines()
    spawn_new_block()
```

---

## 🔥 FINALNA NAPOMENA

Najvažnije:
→ projekt je rastao kroz testiranje i ispravke

To je pravi način učenja programiranja.
