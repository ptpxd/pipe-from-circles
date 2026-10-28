# Tasks: Nézetvezérlés és görbemód-választás

**Input**: Design documents from `specs/002-canvas-curves-editing/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`

**Tests**: A terv és a quickstart szabványos könyvtári `unittest`-ellenőrzéseket ír elő; a történetek tesztjei a kapcsolódó implementáció előtt készülnek el.

**Organization**: A feladatok a specifikáció három, P1 prioritású felhasználói története szerint csoportosulnak.

## Phase 1: Setup

**Purpose**: A meglévő, függőség nélküli Python/Tkinter-projektet használjuk; új projekt- vagy csomagkezelő-beállítás nem szükséges.

Nincs külön setup feladat.

## Phase 2: Foundational

**Purpose**: A meglévő `Circle`, `CircleEditor` és Tkinter alkalmazás biztosítja a történetek közös alapját.

Nincs minden történetet blokkoló alapozó módosítás; a történetek saját kódjukra és ellenőrzésükre támaszkodnak.

## Phase 3: User Story 1 - A rajzfelület nagyítása és mozgatása (Priority: P1) 🎯 MVP

**Goal**: A felhasználó nagyíthassa és pásztázhassa a munkaterületet a körök adatainak vagy egymáshoz viszonyított geometriájának módosítása nélkül.

**Independent Test**: Legalább két kör elhelyezése után a görgős nagyítás, a középső gombos pásztázás és az új kör megadása ellenőrizhető; a mutató alatti munkapont nagyításkor helyben marad, az alakzat nem torzul, a kattintások pedig a megfelelő világkoordinátára esnek.

### Tests for User Story 1

- [X] T001 [P] [US1] Hozz létre `unittest`-teszteket a `tests/test_app.py` fájlban a világ- és képernyőkoordináta közötti átalakításra, a kurzorközpontú nagyításra, a pásztázásra és az átalakított nézetben történő kattintási koordinátákra.

### Implementation for User Story 1

- [X] T002 [US1] Bővítsd az `app.py` fájlt egyenletes, korlátozott nagyítású nézetállapottal, oda-vissza koordináta-átalakítással, kurzor alatti pontot rögzítő `<MouseWheel>` nagyítással és középső gombos húzással; a köradatok maradjanak világkoordinátákban, és minden rajzelem együtt transzformálódjon.

**Checkpoint**: A nézet nagyítása és pásztázása nem módosítja a körlistát; a két kattintás a nézettranszformáció után is helyes körközéppontot és -sugarat eredményez.

## Phase 4: User Story 2 - Az utolsó kör újramegadása (Priority: P1)

**Goal**: A felhasználó a legutolsó teljes kört eltávolíthassa és újra megadhassa, a korábbi körök sorrendjének megőrzésével.

**Independent Test**: Több kör megadása után a Backspace pontosan a legutolsó teljes kört távolítja el, az előző körök sorrendje megmarad, az alakzat frissül, majd egy új kör hozzáadható; üres körlistán sem történik hiba.

### Tests for User Story 2

- [X] T003 [P] [US2] Hozz létre `unittest`-teszteket a `tests/test_editor.py` fájlban az utolsó kör eltávolítására, a megmaradó körök sorrendjére, az üres listára és a függőben lévő középpont megszakítására.

### Implementation for User Story 2

- [X] T004 [US2] Bővítsd az `editor.py` fájlt az utolsó teljes kör visszavonására szolgáló művelettel; függőben lévő középpont esetén azt szakítsa meg először, üres állapotban legyen hatástalan, és más kör sorrendjét ne változtassa meg.
- [X] T005 [US2] Kösd a Backspace billentyűt a vászon fókuszához az `app.py` fájlban; a billentyűművelet használja az `editor.py` visszavonását, állítsa vissza a középpont-megadási állapotot, frissítse az alakzatot és a felületi visszajelzést.

**Checkpoint**: Backspace után a teljes körök száma legfeljebb eggyel csökken, az adatsorrend megmarad, és új kör adható meg.

## Phase 5: User Story 3 - A két körből képzett görbemódszer használata (Priority: P1)

**Goal**: A felhasználó ugyanazon rendezett körsorozaton válthasson a Disk-Bézier és a kör-bőrözési cső között; a bőrözés az elfogadhatatlan geometriát világos hibával utasítsa el.

**Independent Test**: Legalább két körből mindkét módszer kiválasztható és az alakzat frissül. Megengedett konfigurációnál a bőrözés érinti a bemeneti köröket, érintőiránya merőleges a sugárra, és a csatlakozó Hermite-szakaszok folytonosak. Nem megengedett konfigurációnál a felhasználó hibaüzenetet kap, a körök megmaradnak, és hibás kontúr nem jelenik meg.

### Tests for User Story 3

- [X] T006 [P] [US3] Hozz létre `unittest`-teszteket a `tests/test_geometry.py` fájlban a kétkörös és elfogadható többkörös bőrözés érintési pontjaira, érintőire, Hermite-szakaszaira, geometriai transzformáció-invarianciájára és az elutasított bemenetekre.

### Implementation for User Story 3

- [X] T007 [US3] Bővítsd a `geometry.py` fájlt két kör esetén külső közös érintőkből, három vagy több kör esetén pedig a szomszédos középponti irányok biszektorából számított skinning-kontaktpontokkal.
- [X] T008 [US3] Implementáld a `geometry.py` fájlban a kontaktpontokat összekötő lokális Hermite-szakaszokat és a végkörök kontúrt lezáró íveit; adj `SkinningError` hibát legalább két kör hiányakor, lehetetlen érintőnél, egybeeső vagy kollineáris/rosszul kondicionált körhármasnál, éles irányváltásnál, másik kör belsejébe eső kontaktpontnál vagy nem biztonságosan zárható/önmetsző kontúrnál.
- [X] T009 [US3] Hozz létre `unittest`-teszteket a `tests/test_app_modes.py` fájlban a módválasztásra, a körlista változatlanságára, az aktuális módszer szerinti frissítésre és a bőrözési hiba felületi visszajelzésére.
- [X] T010 [US3] Bővítsd az `app.py` fájlt Disk-Bézier és kör-bőrözés módválasztóval; a kiválasztott mód rajzoljon, hozzáadás/törlés után frissüljön, bőrözési hibánál őrizze meg a köröket, ne rajzoljon hibás eredményt, és jelenítsen meg érthető hibaüzenetet.

**Checkpoint**: Mindkét görbemód kiválasztható; az érvénytelen bőrözési konfiguráció nem változtatja meg a bemenetet, és nem hagy félrevezető rajzot a vásznon.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: A vezérlők és a módszerválasztás dokumentálása, majd a teljes változtatás ellenőrzése.

- [X] T011 Frissítsd a `README.md` fájlt a görgős nagyítás, középső gombos pásztázás, Backspace, a két görbemód, a bőrözés korlátai, valamint a futtatási és tesztelési parancsok leírásával.
- [X] T012 Futtasd a `uv run --no-project --python 3.14 python -m unittest discover -s tests -v` parancsot, majd végezd el a `specs/002-canvas-curves-editing/quickstart.md` kézi ellenőrzéseit; javítsd a kapcsolódó regressziókat az érintett forrás- és tesztfájlokban.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Nincs inicializálásra váró új projekt vagy függőség; a meglévő Python/Tkinter projekt használható.
- **Foundational (Phase 2)**: Nincs külön alapozó feladat; a meglévő körmodell, editor és alkalmazás szolgál közös alapul.
- **User Stories (Phase 3+)**: A történetek funkcionális céljai különállók, de az `app.py` közös módosításai miatt a vászon-integrációkat egymás után kell végrehajtani.
- **Polish (Phase 6)**: A dokumentáció és az összes történet implementációja után következik.

### User Story Dependencies

- **US1 (P1)**: Nincs függősége más új történettől; a nézettranszformáció az eredeti alkalmazás meglévő körlistájával működik.
- **US2 (P1)**: A körlista-visszavonás önálló; az `app.py` integrációt US1 vászonmódosításai után kell elvégezni a fájlütközés elkerülésére.
- **US3 (P1)**: A geometriai skinning US1/US2-től függetlenül fejleszthető, de módválasztó felületi integrációja a korábbi `app.py` módosítások után történjen.

### Task Dependencies

- `T002` függ `T001`-től; `T004` függ `T003`-tól.
- `T005` függ `T002`-től és `T004`-től.
- `T007` függ `T006`-tól; `T008` függ `T007`-től.
- `T009` a geometriai implementáció (`T008`) után készül; `T010` függ `T009`-től és US2 vászon-integrációjától (`T005`).
- `T011` és `T012` a funkciók elkészülte után következik; `T012` függ `T011`-től.

### Parallel Opportunities

- Az `app.py`, `editor.py` és `geometry.py` különböző tesztfájljai miatt `T001`, `T003` és `T006` párhuzamosan előkészíthető.
- `T007`–`T008` ugyanazt a `geometry.py` fájlt módosítja, ezért egymás után végzendő el.
- `T005` és `T010` ugyanazt az `app.py` fájlt módosítja, ezért nem futhatnak párhuzamosan; a történetek geometriai és editor-alapfeladatai viszont külön fájlokban dolgoznak.
- `T011` dokumentációs módosítás; a végső `T012` ellenőrzés előtt kell befejezni.

## Parallel Example: Independent Story Tests

```text
T001: nézettranszformációs tesztek a tests/test_app.py fájlban
T003: editor-visszavonási tesztek a tests/test_editor.py fájlban
T006: geometriai skinning-tesztek a tests/test_geometry.py fájlban
```

## Implementation Strategy

### MVP First (User Story 1)

1. Készítsd el és ellenőrizd a nézettranszformációs teszteket (`T001`).
2. Valósítsd meg a nagyítást, pásztázást és a világkoordinátás kattintásokat (`T002`).
3. **Állj meg és ellenőrizd** az US1 önálló tesztkritériumát.

### Incremental Delivery

1. US1 hozzáadja a nézet navigációját és koordinátahelyes körbevitelt.
2. US2 hozzáadja az utolsó kör biztonságos eltávolítását és újramegadását.
3. US3 hozzáadja a bőrözési geometriát, módválasztást és hiba-visszajelzést a meglévő Disk-Bézier megőrzésével.
4. Frissítsd a README-t, majd futtasd az összes automatizált és kézi ellenőrzést.

## Phase 7: Convergence

- [X] T013 Add alkalmazásszintű regressziós teszteket a `tests/test_app_modes.py` fájlba, amelyek a Backspace callback és a két kattintásos körbevitel után ellenőrzik a körök számát/sorrendjét és az éppen kiválasztott mód frissített megjelenítését per FR-006, FR-011, US2/AC1, US3/AC3 (partial).

## Phase 8: Convergence

- [X] T014 Adj visszajelzést az `app.py` fájlban, ha a kör-bőrözés mód kiválasztásakor még nincs elegendő kör a kontúr előállításához, és teszteld a `tests/test_app_modes.py` fájlban per FR-010, US3/AC4, SC-005 (partial).
