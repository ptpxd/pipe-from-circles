# Implementation Plan: Robusztus kör-bőrözés éles kanyarokban

**Branch**: `004-sharp-turn-skinning` | **Date**: 2026-11-25 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-sharp-turn-skinning/spec.md`

## Summary

Javítsuk a meglévő kör-bőrözést úgy, hogy a körök megadási sorrendjét követő csőalakzat
éles kanyaroknál, majdnem kollineáris szakaszoknál, eltérő sugaraknál és közeli vagy átfedő
köröknél is előálljon, ha a specifikáció szerinti egyszerű kontúr kialakítható. A meglevő,
szokásos esetekben az érintőalapú Hermite-konstrukció viselkedése maradjon meg; a geometriát
előállító és ellenőrző logika a tiszta `geometry.py` modulban marad. A teljes határ zártságát,
önmetszésmentességét és a bemeneti körök befoglalását ellenőrizni kell. Az érvénytelen
konfigurációkat a meglévő `SkinningError`-alapú felületi visszajelzés kezelje, a Disk-Bézier mód
és a köradatok módosítása nélkül.

## Technical Context

**Language/Version**: Python 3.10+ nyelvi elemek; a dokumentált futtatási környezet Python 3.14

**Primary Dependencies**: Tkinter és Python standard library (`math`, `dataclasses`, `typing`);
nincs külső futásidejű függőség

**Storage**: N/A; a körlista és a megjelenítési mód csak az alkalmazás munkamenetében él

**Testing**: Standard-library `unittest`; geometriai regressziók `tests/test_geometry.py`-ban,
felületi hibakezelés és módváltás `tests/test_app_modes.py`-ban

**Target Platform**: Windows asztali alkalmazás Tkinter-támogatású Python-környezetben

**Project Type**: Meglévő, egyprojektű Python asztali alkalmazás

**Performance Goals**: A körmódosítás utáni újrarajzolás maradjon használható a szerkesztő
szokásos, mérsékelt méretű körsorozatainál; a specifikáció nem ad számszerű késleltetési célt

**Constraints**: A bemeneti körök értékei és sorrendje változatlanul megőrzendő; a határnak
követnie kell a rendezett útvonalat, körül kell vennie a bemeneti köröket, és egyszerűnek kell
maradnia. A Disk-Bézier működését nem szabad módosítani. A külső geometriai függőség bevezetése
nem indokolt a jelenlegi követelményekhez.

**Scale/Scope**: Egy felhasználó, egy munkamenet, mérsékelt számú rendezett kör; nincs
adatmentés, exportálás vagy új felhasználói vezérlő

## Constitution Check

- **Clarity and Understandability**: A körsorrend az útvonalat adja; a származtatott skinning
  kontúr és az érvénytelen bemenet állapota külön fogalom marad.
- **Simplicity**: A meglévő `geometry.py`-t és standard library-t használjuk; nem vezetünk be
  új függőséget vagy párhuzamos geometriamodellt.
- **Efficiency**: A kontúr csak szerkesztési/módváltási újrarajzoláskor készül; a mintavételezés
  és metszésvizsgálat költségét a jelenlegi mérsékelt körsorozatokhoz kell igazítani, indokolatlan
  mintaszám-növelés nélkül.
- **Correctness and Validation**: Előre elvárt eredménnyel rögzített stressztesztek mérik a
  kanyarhatárokat, lefedést, zártságot, önmetszést, bemenetmegőrzést és a Disk-Bézier regressziót.
- **Focused, Maintainable Changes**: A funkció a skinning geometriára és annak közvetlen
  felületi hibajelzésére, célzott tesztjeire és futtatási útmutatójára korlátozódik.

**Gate result before research**: PASS. A funkció a meglévő projektben, új függőség és tárolási
változtatás nélkül valósítható meg. A kanyarátmenet és a teljes kontúr validálása a kért
robosztussághoz szükséges, nem spekulatív bővítés.

## Phase 0: Research

A kutatási döntések a [research.md](research.md) fájlban találhatók. A választott geometriai
szerződés a sorrendet követő, változó sugarú csőhatár; nem a bemeneti korongok egyszerű uniója
és nem konvex burok. Az érvényes, szokásos esetek Hermite-konstrukciója megmarad, míg a kanyarok
és degenerált átmenetek kezelése stabil határképzéssel és teljes kontúr-ellenőrzéssel bővül.
Nincs feloldatlan technikai tisztázás.

## Phase 1: Design & Contracts

### Adatmodell

A [data-model.md](data-model.md) dokumentálja a változatlan, rendezett körsorozatot, a
származtatott skinning kontúrt és az érvényes/hibás megjelenítési állapotot.

### Interfészszerződések

Nincs `contracts/` könyvtár: az alkalmazás nem tesz közzé külső API-t, hálózati végpontot vagy
CLI-szerződést. A geometriai függvények belső modulhatáron működnek; ezeket a tesztek fedik le.

### Quickstart

A [quickstart.md](quickstart.md) célzott geometriai és felületi teszteket, teljes regressziós
tesztfuttatást és kézi, éles kanyart lefedő ellenőrzést ír le.

### Constitution Check a tervezés után

- **Clarity and Understandability**: PASS — a kutatás tisztázta, hogy az útvonal sorrendje a
  középvonalhoz tartozik, nem a kontúr határpontjainak sorrendjéhez.
- **Simplicity**: PASS — nincs új függőség, API vagy tartós adatmodell.
- **Efficiency**: PASS — a geometriai számítás szinkron, csak szükség szerinti újrarajzoláskor
  fut; nincs animáció vagy háttérfolyamat.
- **Correctness and Validation**: PASS — a validálás a teljes zárt kontúrra, ne csak a helyi
  szomszédos érintőkre terjedjen ki; a stresszteszt-bemenetek elvárt eredménye előre rögzített.
- **Focused, Maintainable Changes**: PASS — a változtatás a skinning útvonalra korlátozott;
  a körszerkesztés és Disk-Bézier meglévő viselkedése regressziós ellenőrzést kap.

**Gate result after design**: PASS. Nem maradt alkotmányos eltérés vagy feloldatlan
követelményértelmezés.

## Project Structure

### Documentation (this feature)

```text
specs/004-sharp-turn-skinning/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── checklists/
│   └── requirements.md
└── tasks.md              # A /speckit-tasks parancs hozza létre
```

### Source Code (repository root)

```text
geometry.py               # Skinning kontúr, átmenetek és geometriai validálás
app.py                    # Skinning megjelenítése és hibaállapot visszajelzése
tests/
├── test_geometry.py      # Határgeometria, szélső esetek és Disk-Bézier regresszió
└── test_app_modes.py     # Felületi hibakezelés, inputmegőrzés és módváltás
README.md                 # Skinning korlátainak és használatának frissített leírása
```

**Structure Decision**: A jelenlegi gyökérmodulokat használjuk. Új csomag, külső geometriai
könyvtár, adatbázis vagy felhasználói felület nem szükséges.

## Complexity Tracking

Nincs alkotmányos eltérés. A teljes kontúr ellenőrzése a kért geometriai megbízhatóság
közvetlen része; az eredmény továbbra is egy tiszta, tesztelhető geometriai függvényből származik.
