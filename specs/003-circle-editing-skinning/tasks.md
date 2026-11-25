# Tasks: Körök közvetlen szerkesztése és skinning-megjelenítés

**Input**: A `specs/003-circle-editing-skinning/` specifikációja. A `plan.md` még nem készült el; a végrehajtható feladatok a specifikációra, a meglévő `app.py`, `editor.py`, `geometry.py`, `tests/` struktúrára és a `specs/002-canvas-curves-editing/plan.md` alkalmazásszintű technikai kontextusára épülnek.

**Prerequisites**: `spec.md` szükséges; `plan.md` hiányzik. Nincs külön `research.md`, `data-model.md` vagy `contracts/`.

**Tests**: A meglévő projekt `unittest`-et használ; a viselkedéshez kapcsolódó célzott tesztek a történetek feladatai közé kerülnek.

**Organization**: A feladatok a specifikáció három, P1 prioritású felhasználói története szerint vannak rendezve.

## Formátum: `[ID] [P?] [Story] Leírás`

- **[P]**: Csak akkor szerepel, ha a feladat más, párhuzamosan végezhető feladattal eltérő fájlokon dolgozik.
- **[Story]**: A felhasználói történet azonosítója; csak a történetfázis feladatai kapják meg.
- Minden feladat megnevezi az érintett fájl útvonalát.

## Phase 1: Setup

**Cél**: A meglévő Python/Tkinter projekt használata; új függőség vagy projektbeállítás nem szükséges.

Nincs setup feladat.

## Phase 2: Foundational

**Cél**: Nincs minden felhasználói történetet blokkoló infrastruktúra-módosítás; a jelenlegi körmodell, editor és vászon már használható.

Nincs külön alapozó feladat. A méretezés és mozgatás ugyanazt a körlistát módosítja, a vászon integrációját pedig a történetfázisok vezetik be.

## Phase 3: User Story 1 - Kör méretének módosítása (Priority: P1) 🎯 MVP

**Cél**: A felhasználó egy kör két szemközti méretező pontjának húzásával állíthassa a sugarat, a kör középpontjának, a többi körnek és a sorrendnek a megőrzésével.

**Független ellenőrzés**: Hozz létre egy vagy több kört, húzd el mindkét méretező pontot, és ellenőrizd, hogy a célkör sugara változik, középpontja és a többi kör adata nem, a származtatott alakzat pedig frissül. Nagyított nézetben is ellenőrizd a megfelelő pont kiválasztását.

### Megvalósítási feladatok

- [X] T001 [P] [US1] Adj `CircleEditor`-méretezési műveletet ellenőrző teszteket a `tests/test_editor.py` fájlhoz: pozitív sugárra változtatás, középpont és sorrend megőrzése, valamint a többi kör változatlansága.
- [X] T002 [US1] Valósítsd meg a `CircleEditor` célkör-sugarat módosító műveletét az `editor.py` fájlban; cserélje az érintett `Circle` értéket úgy, hogy annak középpontja és listabeli helye megmaradjon, az érvénytelen sugár pedig ne hozhasson létre hibás kört.
- [X] T003 [P] [US1] Adj vászon-interakciós teszteket a `tests/test_app_modes.py` fájlhoz a méretező pontok megjelenítésére, nagyított/eltolt nézetben történő kiválasztására és a méretezés utáni alakzatfrissítésre.
- [X] T004 [US1] Bővítsd az `app.py` fájlt két, szemközti méretező pont rajzolásával és a bal egérgombos húzás kezelésével; a pont kiválasztása élvezzen elsőbbséget a kör belsejének kiválasztásával szemben, a sugár a kör középpontjától számítódjon, a világ-/képernyőkoordináták átalakítása működjön nagyítás és eltolás mellett, az üres vászonra kattintás kétkattintásos körfelvétele pedig maradjon meg.

**Ellenőrzési pont**: Méretező pont húzásakor csak a célkör sugara változik, az alakzat az aktuális módban újrarajzolódik, és üres területre kattintva továbbra is új kör vehető fel.

## Phase 4: User Story 2 - Kör áthelyezése (Priority: P1)

**Cél**: A felhasználó a méretező pontokon kívül a kör belsejének húzásával mozgathassa a kört úgy, hogy annak sugara és listabeli helye változatlan maradjon.

**Független ellenőrzés**: Több kör közül húzz el egyet a belsejénél fogva; ellenőrizd, hogy csak a célkör középpontja változik, a sugara és sorrendje nem, és az alakzat követi a módosítást. Méretező ponton indított húzás ne mozgassa a kört.

### Megvalósítási feladatok

- [X] T005 [P] [US2] Adj körmozgatási műveletet ellenőrző teszteket a `tests/test_editor.py` fájlhoz: új középpont beállítása a sugár és sorrend megőrzésével, valamint a többi kör változatlansága.
- [X] T006 [US2] Valósítsd meg a célkör középpontját módosító műveletet az `editor.py` fájlban; az új `Circle` őrizze meg a sugarat és a listabeli helyet, és ne módosítsa a többi kört.
- [X] T007 [P] [US2] Adj vászon-interakciós teszteket a `tests/test_app_modes.py` fájlhoz: kör belsejének húzása mozgat, méretezőpont-húzás nem indít mozgatást, a kezdő kattintási eltolás megmarad, és az üres vászonra kattintás továbbra is új kört kezd.
- [X] T008 [US2] Bővítsd az `app.py` húzáskezelését úgy, hogy méretező ponton kívül, a kör belsejében indított húzás a célkört mozgassa; őrizd meg a sugár, a többi kör, a sorrend és a kattintás helye közötti eltolás értékét, a csak kattintással induló körfelvétel és a függőben lévő kör sugárának megadása pedig maradjon működőképes; minden módosítás után rajzold újra a kiválasztott mód alakzatát.

**Ellenőrzési pont**: Egy kör mozgatása nem változtatja meg annak sugarát vagy a többi kör adatait; a körök sorrendjéből számított alakzat az új helyzetet mutatja.

## Phase 5: User Story 3 - Körök teljes kitöltése skinning módban (Priority: P1)

**Cél**: Skinning módban minden bemeneti kör teljes belseje legyen egységesen kékkel kitöltve, miközben a körhatár és a szerkesztőpontok láthatók maradnak.

**Független ellenőrzés**: Válts skinning módra egy vagy több körrel, és ellenőrizd, hogy a teljes körkorong kék, a határ és a méretezőpontok felismerhetők, és a módváltás nem módosítja a köradatokat. Próbáld ki olyan körkonfigurációval is, ahol a skinning kontúr nem állítható elő.

### Megvalósítási feladatok

- [X] T009 [US3] Adj megjelenítési teszteket a `tests/test_app_modes.py` fájlhoz, amelyek skinning módban a körök teljes kitöltését, a körhatár és fogópontok láthatóságát, a Disk-Bézier megjelenés változatlanságát, valamint a köradatok megőrzését ellenőrzik.
- [X] T010 [US3] Módosítsd az `app.py` rajzolási sorrendjét és körmegjelenítését úgy, hogy skinning módban minden bemeneti kör teljes korongja kékkel legyen kitöltve, majd a körhatár és a méretező pontok láthatóan rákerüljenek; a kitöltés kontúrhiba esetén is maradjon látható, és Disk-Bézier módban őrizd meg a jelenlegi körmegjelenítést.

**Ellenőrzési pont**: Skinning módban egyetlen bemeneti kör belsejében sincs fedetlen terület; módváltáskor a körök geometriája nem változik.

## Phase 6: Polish & Cross-Cutting Concerns

**Cél**: A módosított interakciók dokumentálása és az összes történet ellenőrzése.

- [X] T011 Frissítsd a `README.md` fájlt a méretező pontok használatával, a kör belsejének húzásával, az üres vásznon történő körfelvétellel, valamint a skinning mód teljes kék körkitöltésével.
- [X] T012 Futtasd a `uv run --no-project --python 3.14 python -m unittest discover -s tests -v` parancsot a `tests/` tesztkészletre, majd kézzel ellenőrizd a `README.md`-ben leírt méretezési, mozgatási, módváltási és nagyítás/eltolás melletti szerkesztési folyamatokat; javítsd a kapcsolódó regressziókat az `app.py`, `editor.py` és a megfelelő `tests/` fájlokban.

## Függőségek és végrehajtási sorrend

### Fázisfüggőségek

- **Setup (Phase 1)**: Nincs új projekt vagy függőség.
- **Foundational (Phase 2)**: Nincs külön blokkoló alapozó feladat.
- **User Story 1 (Phase 3)**: A meglévő `CircleEditor`, körlista és nézettranszformáció alapjaira épül.
- **User Story 2 (Phase 4)**: A kör belsejének húzása a US1-ben létrehozott balgombos húzás- és kiválasztáskezelésre épül.
- **User Story 3 (Phase 5)**: Funkcionálisan önálló, de az `app.py` közös rajzolási logikája miatt a vászonmódosítások ütközésének elkerülésére a US1 és US2 után integrálandó.
- **Polish (Phase 6)**: Az implementációk után következik.

### User Story-függőségek

- **US1 (P1)**: Más új történettől nem függ; ez a javasolt MVP.
- **US2 (P1)**: A US1 húzáskezelésére épül, ezért US1 után következik.
- **US3 (P1)**: A körmozgatástól és -méretezéstől funkcionálisan független, de az `app.py` közös rajzolási kódja miatt integrációs sorrendben US2 után végzendő el.

### Feladatfüggőségek

- `T002` függ `T001`-től; `T004` függ `T002`-től és `T003`-tól.
- `T006` függ `T005`-től; `T008` függ `T006`-tól és `T007`-től, valamint a US1 húzáskezelésétől.
- `T010` függ `T009`-től.
- `T011` és `T012` a történetek implementációi után következik; `T012` függ `T011`-től.

### Párhuzamosítási lehetőségek

- A US1-ben `T001` és `T003` eltérő tesztfájlokat (`tests/test_editor.py`, `tests/test_app_modes.py`) módosít, ezért párhuzamosan előkészíthető.
- A US2-ben `T005` és `T007` külön tesztfájlokon dolgozik, ezért párhuzamosan készíthető; a vászontesztek a US1 húzáskezelése után írhatók.
- A `T002`, `T004`, `T006`, `T008` és `T010` azonos forrásfájlokat módosítanak egymást követő történetekben, ezért az implementációjukat nem szabad párhuzamosítani.

## Párhuzamos példák történetenként

```text
T001: editor-méretezési tesztek a tests/test_editor.py fájlban
T003: vászon-méretezési tesztek a tests/test_app_modes.py fájlban
```

```text
T005: editor-mozgatási tesztek a tests/test_editor.py fájlban
T007: vászon-mozgatási tesztek a tests/test_app_modes.py fájlban
```

US3-ban nincs párhuzamosítható történetspecifikus feladat: a teszt és a megjelenítés ugyanazt
az alkalmazásmód-tesztfájlt, illetve rajzolási útvonalat érinti.

## Megvalósítási stratégia

### MVP először (csak User Story 1)

1. Készítsd el a méretező művelet és vászonhúzás célzott tesztjeit (`T001`, `T003`).
2. Valósítsd meg a kör sugarának módosítását és a méretezőpont-húzást (`T002`, `T004`).
3. **Állj meg és ellenőrizd** a US1 független ellenőrzési feltételét.

### Fokozatos szállítás

1. US1: kétpontos körméretezés és az alakzat frissítése.
2. US2: körmozgatás a már elkészült húzáskezelés használatával.
3. US3: teljes kék körkitöltés skinning módban.
4. README-frissítés és végső automatizált, valamint kézi ellenőrzés.

## Megjegyzések

- A `[P]` feladatok csak eltérő, egymással nem ütköző fájlokon dolgozhatnak.
- A `[US#]` címke a specifikáció megfelelő felhasználói történetére hivatkozik.
- A köradatokat a meglévő világkoordináta-rendszerben kell tartani; a nézettranszformáció csak a kiválasztást és megjelenítést befolyásolja.
- A `setup-tasks.ps1 -Json` futtatása a hiányzó `specs/003-circle-editing-skinning/plan.md` miatt hibával leállt. A feladatlista ezért a rendelkezésre álló specifikáció és a meglévő alkalmazás/előző terv alapján készült; új tervfájl nem készült.
