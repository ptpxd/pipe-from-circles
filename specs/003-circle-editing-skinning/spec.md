# Feature Specification: Körök közvetlen szerkesztése és skinning-megjelenítés

**Feature Branch**: `003-circle-editing-skinning`

**Created**: 2026-11-25

**Status**: Draft

**Input**: User description: "Lehessen a körök méretét két húzható ponttal módosítani, lehessen mozgatni a köröket, és skinning módban a kék fedje be az egész kört."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Kör méretének módosítása (Priority: P1)

A felhasználó egy már megadott kör méretét közvetlenül szeretné állítani. A kör két, egymással
szemben lévő húzható pontja jelzi az átmérőt; bármelyik pont elhúzásával a felhasználó
növelheti vagy csökkentheti a kört anélkül, hogy újra megadná azt.

**Why this priority**: A méret közvetlen módosítása gyorsabbá teszi a körök finomhangolását,
és nem igényli a kör újbóli felvételét.

**Independent Test**: Hozzunk létre egy kört, húzzuk el felváltva mindkét méretező pontját,
majd ellenőrizzük, hogy a sugár a húzásnak megfelelően változott, a középpont és a többi kör
pedig változatlan maradt.

**Acceptance Scenarios**:

1. **Given** egy megadott kör két, egymással szemben lévő méretező ponttal, **When** a
   felhasználó valamelyik pontot kifelé húzza, **Then** a kör sugara nő, a középpontja nem
   változik, és a másik pont a kör túloldalán marad.
2. **Given** egy megadott kör, **When** a felhasználó valamelyik méretező pontot a középpont
   felé húzza, **Then** a kör sugara csökken, de pozitív marad.
3. **Given** több megadott kör, **When** a felhasználó egy kör méretező pontját húzza,
   **Then** kizárólag a célzott kör mérete változik, a többi kör adata és sorrendje megmarad.

---

### User Story 2 - Kör áthelyezése (Priority: P1)

A felhasználó a kör helyét szeretné megváltoztatni úgy, hogy a mérete és a körsorozatban
elfoglalt helye ne módosuljon. A kör belsejének húzásával a kör és a hozzá tartozó vezérlőpontok
együtt mozdulnak el.

**Why this priority**: A már megadott körök helyének javítása szükséges az alakzat útvonalának
közvetlen szerkesztéséhez, és elkerüli a kör újramegadását.

**Independent Test**: Adjunk meg legalább két kört, húzzuk el az egyiket, és ellenőrizzük, hogy
csak annak középpontja változik, a sugara és sorrendje megmarad, valamint a belőle képzett
alakzat frissül.

**Acceptance Scenarios**:

1. **Given** egy kör és annak méretező pontjai, **When** a felhasználó a kör belsejét a
   méretező pontokon kívülről elhúzza, **Then** a kör a mutató elmozdulásának megfelelően
   áthelyeződik, miközben a sugara változatlan marad.
2. **Given** több körből álló alakzat, **When** a felhasználó az egyik kört áthelyezi,
   **Then** a többi kör helye és a körök sorrendje változatlan marad, az alakzat pedig az új
   körhelyzetek alapján frissül.
3. **Given** nagyított vagy eltolással megjelenített munkaterület, **When** a felhasználó egy
   kört vagy méretező pontot húz, **Then** a szerkesztés a látható helyhez igazodik, és a nézet
   nagyítása vagy eltolása nem változtatja meg a körök adatait önmagában.

---

### User Story 3 - Körök teljes kitöltése skinning módban (Priority: P1)

A felhasználó skinning módot választ, és azt szeretné, hogy a körök belseje egységesen kékkel
legyen kitöltve. A kör teljes belső területe fedett marad, miközben a kör határa és a méretező
pontok továbbra is felismerhetők.

**Why this priority**: A teljes kitöltés vizuálisan egyértelművé teszi a skinning módhoz tartozó
köröket, és megszünteti a körök belsejében látható fedetlen területeket.

**Independent Test**: Válasszuk ki a skinning módot egy vagy több körnél, és vizuálisan
ellenőrizzük, hogy minden kör teljes belseje kék, a határvonala és szerkesztőpontjai pedig
láthatók maradnak. Váltsunk másik módra, és ellenőrizzük, hogy a körgeometria nem változik.

**Acceptance Scenarios**:

1. **Given** legalább egy megadott kör, **When** a felhasználó skinning módra vált,
   **Then** a kör teljes belső területe egységes kék kitöltést kap, látható fedetlen folt nélkül.
2. **Given** skinning mód és több kör, **When** a felhasználó megtekinti vagy szerkeszti a
   köröket, **Then** minden kör teljes belseje kék marad, és a körhatár, valamint a
   méretezőpontok továbbra is megkülönböztethetők.
3. **Given** egy kiválasztott görbemód, **When** a felhasználó módot vált, **Then** csak a
   megjelenítés módja változik; a körök középpontja, sugara és sorrendje nem.

### Edge Cases

- Ha egy méretező pontot a kör középpontja felé húznak, a kör sugara nem válhat nullává vagy
  negatívvá.
- Ha több kör vagy fogópont egymásra esik, a húzás kezdetekor egyértelműen azonosítható legyen,
  hogy melyik kör melyik pontja vagy belső területe szerkesztődik; a fogópont elsőbbséget élvez
  a kör belsejének húzásával szemben.
- A rajzfelület határán túlra húzás nem okozhat hibás köradatot, és nem módosíthatja a nem
  célzott köröket.
- A nagyítás és eltolás nem változtathatja meg a húzás által elért munkaterületi helyet vagy a
  körök tárolt sorrendjét.
- Ha a skinning mód az adott körkonfigurációhoz nem tud alakzatot készíteni, a körök szerkeszthetők
  és láthatók maradnak; a teljes kék körkitöltés ettől függetlenül a kiválasztott módhoz tartozik.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A rendszer MUST minden megadott körön két, egymással szemben lévő húzható
  méretező pontot jelenítsen meg.
- **FR-002**: A rendszer MUST lehetővé tegye bármelyik méretező pont húzásával a kör sugarának
  módosítását úgy, hogy a középpont változatlan maradjon, a másik pont pedig az átmérő
  szemközti végpontjaként kövesse a méretváltozást.
- **FR-003**: A rendszer MUST a kör belsejének húzásával lehetővé tegye a kör áthelyezését
  úgy, hogy annak sugara változatlan maradjon.
- **FR-004**: A kör mozgatása vagy átméretezése MUST ne módosítsa a többi kör középpontját,
  sugarát vagy sorrendjét.
- **FR-005**: A kör mozgatása vagy átméretezése MUST frissítse a kiválasztott módban
  megjelenített, körökből származtatott alakzatot.
- **FR-006**: Skinning módban a rendszer MUST a megadott körök teljes belső területét
  egységes kékkel fedje le, miközben a körhatár és a szerkesztőpontok felismerhetők maradnak.
- **FR-007**: A rendszer MUST a teljes kék körkitöltést csak skinning módban alkalmazza; a
  módváltás nem módosíthatja a körök geometriai adatait vagy sorrendjét.
- **FR-008**: A rendszer MUST a nagyított vagy eltolással megjelenített nézetben is a megfelelő
  kört és méretező pontot válassza ki, valamint a húzást a munkaterület megfelelő helyére
  értelmezze.
- **FR-009**: A kör méretezése MUST pozitív sugarat tartson fenn, és a kör középpontjától
  mért távolságként értelmezze az új méretet.

### Key Entities

- **Szerkeszthető kör**: A körsorozat egyik eleme, középponttal, pozitív sugárral és rögzített
  sorrenddel.
- **Méretezőpont-pár**: A kör átmérőjének két szemközti, húzható végpontja; bármelyik mozgatása
  a kör sugarát állítja.
- **Görbemód**: A körökből származtatott alakzat megjelenítési módja; ebben a funkcióban a
  skinning mód vált ki teljes kék körkitöltést.
- **Származtatott alakzat**: A szerkeszthető körsorozatból és a kiválasztott görbemódból
  megjelenített csőszerű forma.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Minden megadott kör mérete mindkét méretező pont húzásával megváltoztatható úgy,
  hogy a kör középpontja és minden másik kör adata változatlan marad.
- **SC-002**: Egy kör áthelyezése után annak sugara és a körök sorrendje változatlan marad, a
  többi kör helye pedig nem változik.
- **SC-003**: Skinning módban minden megadott kör teljes belső területe kék; a körök teljes
  listájának vizuális ellenőrzése során nincs látható fedetlen belső rész.
- **SC-004**: Minden körmozgatás és -átméretezés után a megjelenített származtatott alakzat a
  módosított köradatokat tükrözi.
- **SC-005**: Nagyított és eltolással megjelenített nézetben végzett szerkesztés a kiválasztott
  kör kívánt helyét vagy méretét módosítja, és nem változtatja meg a többi kör adatait.

## Assumptions

- A két méretező pont a kör átmérőjének két szemközti végpontja; bármelyik pont húzása a
  középpont megtartásával módosítja a sugarat.
- A kör mozgatása a kör belsejének, de nem a méretező pontoknak a húzásával történik; a kör
  sugara ekkor változatlan.
- Skinning módban a bemeneti körök teljes korongja kap kék kitöltést; a körhatár és a
  szerkesztőpontok továbbra is láthatók. A Disk-Bézier mód meglévő körmegjelenítése változatlan.
- A meglévő nagyítási és eltolási vezérlés, körsorrend és skinning mód viselkedése megmarad,
  kivéve a jelen specifikációban kifejezetten kért közvetlen szerkesztést és kitöltést.
- A szerkesztés a munkamenetben érvényes; körök mentése, exportálása vagy új munkamenetben
  történő visszaállítása nem része ennek a funkciónak.
