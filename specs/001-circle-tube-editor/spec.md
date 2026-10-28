# Feature Specification: Interaktív kör-tube szerkesztő

**Feature Branch**: `001-circle-tube-editor`

**Created**: 2026-10-28

**Status**: Draft

**Input**: User description: "A felhasználó számára lehetővé kell tenni, hogy egér kattintásokkal köröket rakjon le a képernyőre (a középpontot, majd a sugarat megválasztva). A köröket a megadás sorrendjében felhasználva egy csőszerű alakzatot kell létrehozni, amely figyelembe veszi a körök középpontját és sugarát."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Csőszerű alakzat létrehozása körökből (Priority: P1)

A felhasználó egy üres rajzfelületen egymás után köröket helyez el. Minden körhöz először a középpontot, majd egy második kattintással a sugarat adja meg. A rendszer a köröket a megadás sorrendjében veszi figyelembe, és a második érvényes kör után megjeleníti az azokhoz igazodó csőszerű alakzatot. További körök megadásakor az alakzat automatikusan frissül.

**Why this priority**: Ez a feladat központi célja: közvetlenül a felhasználó által meghatározott körökből látható, folytonos alakzatot létrehozni.

**Independent Test**: Üres felületről indulva adjunk meg legalább két kört, majd ellenőrizzük, hogy mindkét kör látható, és létrejön a sorrendjükhöz és méretükhöz igazodó csőszerű alakzat. Adjunk hozzá további kört, és ellenőrizzük, hogy az alakzat külön frissítési művelet nélkül módosul.

**Acceptance Scenarios**:

1. **Given** egy üres rajzfelület, **When** a felhasználó egy helyre kattint, majd attól eltérő helyre kattint, **Then** a két kattintás távolságának megfelelő sugarú kör jelenik meg az első kattintás középpontjával.
2. **Given** egy már megadott kör, **When** a felhasználó megadja a második érvényes kört, **Then** mindkét kör megmarad a felületen, és megjelenik az ő sorrendjükből és adataikból létrehozott csőszerű alakzat.
3. **Given** egy legalább két körből álló alakzat, **When** a felhasználó további érvényes kört ad meg, **Then** az alakzat automatikusan frissül, figyelembe véve az új kör helyét, sugarát és sorrendjét.
4. **Given** a felhasználó éppen egy kör sugarát adja meg, **When** a sugár kattintása a középponttal azonos helyre esik, **Then** nulla sugarú kör és ahhoz tartozó alakzat nem jön létre, a felület pedig lehetővé teszi a sugár újbóli megadását.

### Edge Cases

- Egyetlen érvényes kör megadása után a kör látható marad, de csőszerű alakzat csak legalább két kör esetén jelenik meg.
- Ha a körök sugarai eltérnek, az alakzat vastagsága a megfelelő körök sugaraitól függően változik.
- Egymást átfedő vagy egymástól távoli körök megadása esetén a rendszer a megadási sorrendet tartja meg, és a csőszerű alakzatot ezekből állítja elő.
- A középponttal azonos helyre eső sugárkattintás érvénytelen; érvényes kör nem keletkezik belőle.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A rendszer MUST üres rajzfelületet jelenítsen meg új munkamenet kezdetén.
- **FR-002**: A rendszer MUST tegye lehetővé kör megadását két egymást követő egérkattintással: az első jelöli ki a középpontot, a második a sugár hosszát és irányát.
- **FR-003**: A rendszer MUST jelenítse meg az érvényesen megadott köröket a rajzfelületen.
- **FR-004**: A rendszer MUST őrizze meg a körök megadásának sorrendjét.
- **FR-005**: Legalább két érvényesen megadott kör után a rendszer MUST jelenítsen meg egy folytonos, csőszerű alakzatot, amely a körök sorrendjét, középpontját és sugarát figyelembe veszi.
- **FR-006**: Újabb érvényes kör megadásakor a rendszer MUST automatikusan frissítse a csőszerű alakzatot a teljes körsorozat alapján.
- **FR-007**: A rendszer MUST utasítsa el a nulla sugarú kört, és tegye lehetővé a sugár megadásának megismétlését.

### Key Entities

- **Kör**: A felhasználó által megadott vezérlőadat, amelynek középpontja, pozitív sugara és megadási sorrendje van.
- **Csőszerű alakzat**: A megadott körök sorrendjéből, középpontjaiból és sugaraiból származtatott folytonos, változó vastagságú vizuális forma.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Az érvényes középpont- és sugárkattintások mindegyikéből egy látható kör jön létre, amelynek középpontja és sugara a kattintások által megadott értékeknek felel meg.
- **SC-002**: Két érvényes kör megadása után minden esetben megjelenik a körsorrendből származó csőszerű alakzat; további kör megadásakor az alakzat további felhasználói művelet nélkül frissül.
- **SC-003**: Azonos körközéppontokhoz eltérő sugarakat megadva az alakzat vastagsága megváltozik; eltérő középpontok pedig az alakzat útvonalát módosítják.
- **SC-004**: A nulla sugarú kör megadása nem hoz létre érvénytelen kört, és nem akadályozza meg a felhasználót a következő sugár megadásában.

## Assumptions

- A felület kétdimenziós rajzfelület, és a felhasználó egérrel adja meg a köröket.
- A sugár megadása a középpont után következő második kattintással történik; a sugár a két kattintási hely távolsága.
- A csőszerű alakzat az első két érvényes kör megadása után jelenik meg, és új kör hozzáadásakor frissül.
- A specifikáció nem választ a körök burkolásán alapuló illesztés és a körökből származtatott Bézier-alapú megközelítés között.
- A körök és az alakzat a munkamenet során a rajzfelületen maradnak; mentés, exportálás, körök törlése és visszavonás nem része ennek a funkciónak.
