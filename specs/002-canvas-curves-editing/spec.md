# Feature Specification: Nézetvezérlés és görbemód-választás

**Feature Branch**: `002-canvas-curves-editing`

**Created**: 2026-10-28

**Status**: Draft

**Input**: User description: "A már elkészült kör-tube programban lehessen a táblán görgővel
kizoomolni, egérrel húzogatva mozgatni a nézetet, Backspace használatával az utolsó kört
eltávolítani és újra megadni. A körökből a körök bőrözése és Disk-Bézier módszer közül is lehessen
választani; mindkét módszer legyen használható."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A rajzfelület nagyítása és mozgatása (Priority: P1)

A felhasználó nagyobb munkaterületet szeretne bejárni anélkül, hogy az eddig lerakott körei
kitakarnák a képernyőt. Az egérgörgővel közelít vagy távolít, a rajzfelületet pedig húzással
mozgatja úgy, hogy a körök és a cső egymáshoz viszonyított helye változatlan maradjon.

**Why this priority**: A jelenlegi, rögzített nézetben a nagy körök és hosszú alakzatok
elfoglalhatják a teljes rajzfelületet; a navigáció a használhatóság alapfeltétele.

**Independent Test**: Helyezzünk el legalább két kört, nagyítsunk és kicsinyítsünk a görgővel,
majd húzzuk el a nézetet; ellenőrizzük, hogy a geometria láthatóan követi a nézetet, az alakzat
nem torzul, és új kör továbbra is megadható.

**Acceptance Scenarios**:

1. **Given** egy rajzfelületen megjelenített alakzat, **When** a felhasználó az egérgörgőt
   megforgatja a rajzfelület fölött, **Then** a nézet nagyítása megváltozik, és az alakzatok
   arányai változatlanok maradnak.
2. **Given** egy nagyított vagy kicsinyített rajzfelület, **When** a felhasználó az egérrel
   elhúzza a nézetet, **Then** a meglévő körök és alakzatok együtt, egymáshoz képest változatlan
   helyzetben mozdulnak el.
3. **Given** egy elmozgatott vagy nagyított nézet, **When** a felhasználó új kört helyez el,
   **Then** a kattintási koordináták a látható rajzfelület megfelelő pontjához tartoznak.

---

### User Story 2 - Az utolsó kör újramegadása (Priority: P1)

A felhasználó észreveszi, hogy az utolsóként lerakott kör nem megfelelő helyen vagy méretű.
Backspace lenyomásával eltávolítja ezt a kört, majd a szokásos két kattintással újra megadja.
Az új kör az előző helyére kerül a sorrendben, és a cső azonnal frissül.

**Why this priority**: A körök sorrendje határozza meg a görbét; a legutolsó kör gyors
újramegadása lehetővé teszi a hibák javítását anélkül, hogy a teljes alakzatot újra kellene rajzolni.

**Independent Test**: Adjunk meg legalább két kört, nyomjuk meg a Backspace billentyűt, majd
helyezzünk el új kört; ellenőrizzük a körök számát, sorrendjét és a cső frissülését.

**Acceptance Scenarios**:

1. **Given** legalább egy teljes kör és nincs függőben lévő körközéppont, **When** a felhasználó
   lenyomja a Backspace billentyűt, **Then** az utolsóként megadott kör eltűnik, és a felület
   középpont megadására vár.
2. **Given** legalább két kör, **When** a felhasználó eltávolítja az utolsó kört, **Then** a
   megmaradó körök sorrendje nem változik, és a megjelenített cső azonnal azokból frissül.
3. **Given** az utolsó kör eltávolítása után a felhasználó új kört ad meg, **When** befejezi a
   kör kétkattintásos megadását, **Then** az új kör a sor végére kerül, és a cső az új sorrend
   alapján frissül.
4. **Given** még nincs teljes kör, **When** a felhasználó lenyomja a Backspace billentyűt,
   **Then** a program nem hibázik, és az üres rajzfelület használható marad.

---

### User Story 3 - A két körből képzett görbemódszer használata (Priority: P1)

A felhasználó kiválaszthatja, hogy a megadott körökből Disk-Bézier alakzat vagy a körök
bőrözésével kapott csőszerű alakzat készüljön. A választott módszer ugyanazt a rendezett
körsorozatot használja, és új kör hozzáadásakor frissül.

**Why this priority**: A feladat mindkét konstrukció használatát kéri; a választható megjelenítés
érthetővé teszi a különbségeket anélkül, hogy az eredmények egymásra rajzolódnának.

**Independent Test**: Adjunk meg legalább két kört, váltsunk mindkét módszerre, és ellenőrizzük,
hogy mindkét választás ad egy csőszerű eredményt a körsorozatból, a bőrözés pedig érinti a
megadott köröket, amikor a konfiguráció megengedett.

**Acceptance Scenarios**:

1. **Given** legalább két kör és a Disk-Bézier módszer van kiválasztva, **When** a felhasználó a
   kör-bőrözés módszerére vált, **Then** a megjelenített alakzat a bőrözési módszer eredményére
   cserélődik, a körök és sorrendjük változatlanul megmarad.
2. **Given** legalább két kör és a kör-bőrözés módszere van kiválasztva, **When** a felhasználó a
   Disk-Bézier módszerre vált, **Then** a megjelenített alakzat a Disk-Bézier eredményére cserélődik.
3. **Given** egy kiválasztott módszer és legalább két kör, **When** a felhasználó új kört ad meg,
   **Then** az éppen kiválasztott módszer alakzata frissül a teljes körsorozatból.
4. **Given** olyan körkonfiguráció, amelyhez bőrözési alakzat nem állítható elő, **When** a
   felhasználó a bőrözési módszert választja, **Then** a rendszer érthető visszajelzést ad,
   megőrzi a köröket, és nem jelenít meg érvénytelen bőrözési eredményt.

### Edge Cases

- A görgős nagyításnak és a nézet húzásának a rajzfelület határainál sem szabad módosítania a
  körök adatait vagy sorrendjét.
- A Backspace egy üres listánál nem okozhat hibát.
- A Backspace a függőben levő, még be nem fejezett középpontot nem kezeli teljes körként; a
  megkezdett kör állapotát törölheti, de teljes körből nem távolít el többet egynél.
- A bőrözési módszer nem minden körkonfigurációnál lehetséges; ilyen esetben a hiba
  visszajelzése nem törölheti a felhasználó által megadott köröket.
- A módszerváltás a körök középpontját, sugarát és megadási sorrendjét nem módosíthatja.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A rendszer MUST lehetővé tegye a rajzfelület nagyítását és kicsinyítését az
  egérgörgővel.
- **FR-002**: A rendszer MUST lehetővé tegye a rajzfelület nézetének egérrel történő húzását.
- **FR-003**: Nagyítás és húzás közben a rendszer MUST őrizze meg a körök és az alakzat
  egymáshoz viszonyított méretét és helyzetét.
- **FR-004**: A rendszer MUST a nézet átalakítását figyelembe véve értelmezze az új körök
  középpont- és sugárkattintásait.
- **FR-005**: A rendszer MUST a Backspace lenyomásakor eltávolítsa az utolsó teljes kört, ha van
  ilyen, és állítsa vissza a középpont megadásának állapotát.
- **FR-006**: Backspace után a megmaradt körök sorrendje MUST maradjon változatlan, és a
  megjelenített alakzat MUST frissüljön a megmaradt körök alapján.
- **FR-007**: A rendszer MUST tegye lehetővé a Disk-Bézier és a kör-bőrözési módszer közötti
  választást.
- **FR-008**: Disk-Bézier módban a rendszer MUST a körök középpontjából és sugaraiból a
  Disk-Bézier definíciójának megfelelő változó vastagságú alakzatot készítsen.
- **FR-009**: Kör-bőrözési módban a rendszer MUST a megengedett bemeneti konfiguráció esetén
  olyan csőszerű határt jelenítsen meg, amely érinti a bemeneti köröket.
- **FR-010**: Ha a kiválasztott bőrözési módszer a megadott körkonfigurációra nem alkalmazható,
  a rendszer MUST adjon egyértelmű visszajelzést, őrizze meg a bemenetet, és ne jelenítsen meg
  érvénytelen eredményt.
- **FR-011**: Új kör hozzáadása vagy az utolsó kör eltávolítása MUST frissítse az éppen
  kiválasztott módszer eredményét.
- **FR-012**: A módszerváltás MUST ne módosítsa vagy rendezze át a megadott köröket.

### Key Entities

- **Nézetállapot**: A rajzfelület nagyítása és eltolása, amely a köradatok megváltoztatása nélkül
  határozza meg, hogy a munkaterület mely része látható.
- **Körsorozat**: A felhasználó által megadott körök középponttal, pozitív sugárral és rögzített
  sorrenddel.
- **Görbemódszer**: A Disk-Bézier vagy kör-bőrözési eljárás kiválasztása.
- **Származtatott alakzat**: A kiválasztott módszer és a teljes körsorozat alapján előállított
  csőszerű vizuális forma.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A felhasználó a körök törlése vagy újramegadása nélkül képes a munkaterület
  legalább két különböző nagyítási szintje között váltani és a nézetet eltolni.
- **SC-002**: A nagyítás és az eltolás után azonos kattintási minta a munkaterület ugyanazon
  helyére helyez köröket, és a már megadott körök aránya, sorrendje változatlan marad.
- **SC-003**: Backspace után a teljes körök száma pontosan eggyel csökken (ha volt teljes kör),
  és a következő kör megadható.
- **SC-004**: A felhasználó mindkét görbemódot ki tudja választani; módváltáskor a körök
  változatlanok maradnak, az alakzat pedig a választott módszer szerint frissül.
- **SC-005**: Nem alkalmazható bőrözési bemenet esetén a felhasználó visszajelzést kap, a
  bemeneti körök megmaradnak, és nem jelenik meg hibás bőrözési alakzat.

## Assumptions

- A görgő a kurzor pozíciója körül nagyít vagy kicsinyít; középső egérgombbal történő húzás
  mozgatja a nézetet.
- A Backspace az utolsó teljes kört törli, így a felhasználó újrakattinthatja azt; nem teszi
  lehetővé a már megadott kör középpontjának vagy sugarának közvetlen, fogópontokkal történő
  szerkesztését.
- A két görbemódszer választható, és egyszerre csak a kiválasztott eredmény látszik.
- A Disk-Bézier a jelenlegi alapértelmezett módszer marad.
- A kör-bőrözés a megengedett bemeneti konfigurációkban érinti a megadott köröket; nem
  megengedett konfiguráció esetén hibaüzenet jelenik meg.
- A nézet nagyítása és eltolása munkamenet alatti állapot; mentés és későbbi munkamenetben
  történő visszaállítás nem része a funkciónak.
- A változtatás a már elkészült kör-tube alkalmazást bővíti; az eredeti alkalmazás működése
  változatlan marad az új vezérlők használata nélkül.
