# Feature Specification: Robusztus kör-bőrözés éles kanyarokban

**Feature Branch**: `004-sharp-turn-skinning`

**Created**: 2026-11-25

**Status**: Draft

**Input**: User description: "szeretném ha javítanál rajta és minél szélsőségesebb esetekben működjön, tehát éles kanyaroknál ilyeneknél."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bőrözés éles kanyaroknál (Priority: P1)

A felhasználó egy éles irányváltású, rendezett körsorozatból is szeretne folytonos, jól
használható skinning alakzatot kapni. A körök sorrendje és mérete meghatározza az alakzatot;
a rendszernek a megengedhető konfigurációknál nem szabad pusztán az éles kanyar miatt
elutasítania az alakzat előállítását.

**Why this priority**: Az éles kanyarok jelenleg gyakori okai annak, hogy a skinning mód nem
tud alakzatot megjeleníteni, így a funkció alapvető használatát korlátozzák.

**Independent Test**: Adjunk meg olyan körsorozatot, amelyben a szomszédos szakaszok iránya
akár 150 fokkal változik, és ellenőrizzük, hogy ha a konfigurációból érvényes, egyszerű
kontúr készíthető, a skinning mód folytonos, nem önmetsző alakzatot jelenít meg.

**Acceptance Scenarios**:

1. **Given** egy olyan körsorozat, amelynek kanyarja éles, de körülötte érvényes, egyszerű
   kontúr alakítható ki, **When** a felhasználó skinning módot választ, **Then** a rendszer
   megjeleníti az alakzatot hibaüzenet nélkül.
2. **Given** egy éles kanyart tartalmazó körsorozat, **When** a felhasználó az egyik kör helyét
   vagy sugarát módosítja, **Then** az alakzat frissül, a körök sorrendje és nem célzott adatai
   pedig változatlanok maradnak.

---

### User Story 2 - Különböző méretű és közelségű körök kezelése (Priority: P2)

A felhasználó eltérő sugarú, egymáshoz közeli vagy részben átfedő körökkel is szeretne
használható, a körök megadási sorrendjét követő skinning alakzatot kapni, amennyiben a
körsorozatból egyértelmű, egyszerű kontúr alakítható ki.

**Why this priority**: A körök sűrűsége és méretkülönbsége a valós szerkesztésben változó;
ezek miatt nem szükséges elutasítani az egyébként értelmezhető alakzatokat.

**Independent Test**: Próbáljunk ki egyenletes és erősen eltérő sugarú, közeli és átfedő
köröket tartalmazó, érvényes konfigurációkat, és ellenőrizzük, hogy az alakzat folytonos és
nem önmetsző marad.

**Acceptance Scenarios**:

1. **Given** egy eltérő sugarú, közeli körökből álló, érvényesen körülvehető sorozat,
   **When** a felhasználó skinning módot választ, **Then** a rendszer a körök sorrendjét
   megtartva jelenít meg folytonos alakzatot.
2. **Given** egy olyan konfiguráció, amelyből nem alakítható ki a sorrendet követő, érvényes,
   egyszerű kontúr, **When** a felhasználó skinning módot választ, **Then** a rendszer érthetően
   jelzi az akadályt, és a köröket változatlanul, szerkeszthetően megőrzi.

---

### User Story 3 - Stabil eredmény határhelyzetekben (Priority: P3)

A felhasználó majdnem egyenes, nagyon szűk kanyarú vagy jelentősen eltérő léptékű
körkonfigurációkat vizsgál, és azt várja, hogy az alkalmazás vagy stabil alakzatot készítsen,
vagy az okot érthetően jelezze, összeomlás és adatvesztés nélkül.

**Why this priority**: A kis geometriai változások nem vezethetnek kiszámíthatatlan
megjelenítéshez vagy a szerkesztési munkamenet elvesztéséhez.

**Independent Test**: Változtassunk fokozatosan a kanyar szögén, a körök távolságán és
sugarán, majd ellenőrizzük, hogy az eredmény minden esetben vagy érvényes alakzat, vagy
érthető elutasítás, a körök megőrzésével.

**Acceptance Scenarios**:

1. **Given** egy majdnem egyenes vagy fokozatosan élesedő kanyar, **When** a felhasználó
   módosítja valamelyik kör helyét vagy sugarát, **Then** a megjelenítés stabilan frissül, vagy
   a rendszer egyértelműen jelzi, ha az új konfiguráció érvénytelen.
2. **Given** olyan szélsőséges konfiguráció, amelyből egyszerű kontúr nem készíthető,
   **When** a rendszer ezt észleli, **Then** nem jelenít meg hibás vagy önmetsző skinning
   alakzatot, és a megadott körök, sorrendjük és szerkeszthetőségük megmarad.

### Edge Cases

- A majdnem egyenes és a közel 150 fokos irányváltozás közötti kanyarok nem okozhatnak
  indokolatlan elutasítást, ha érvényes kontúr létezik.
- Egymást követő, azonos vagy közel azonos középpontú körök esetén a rendszer ne számítson
  érvénytelen érintési irányokkal.
- A nagyon eltérő sugarú, egymást átfedő vagy csaknem érintkező köröket ne utasítsa el
  kizárólag az átfedésük vagy közelségük miatt.
- Egy hurok, visszafordulás vagy több kör kölcsönhatása megakadályozhatja a sorrendet követő,
  egyszerű skinning határt; ilyenkor egyértelmű visszajelzés szükséges, nem pedig a görbe
  önkényes kiegyenesítése vagy a körök átrendezése.
- A határesetek vizsgálata nem módosíthatja és nem rendezheti át a felhasználó körsorozatát.
- A skinning mód hibája vagy érvénytelen konfigurációja nem akadályozhatja a körök további
  szerkesztését és másik görbemód használatát.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A rendszer MUST skinning alakzatot készítsen éles kanyarokat tartalmazó
  körsorozatokból, ha az alakzat a megadási sorrendet követve érvényes, folytonos és egyszerű
  kontúrral körülvehető.
- **FR-002**: A rendszer MUST támogassa a szomszédos körközéppontok iránya közötti legfeljebb
  150 fokos irányváltozást, amennyiben az alakzatból érvényes, egyszerű kontúr készíthető.
- **FR-003**: A rendszer MUST kezelje a közel egyenes átmeneteket és az eltérő sugarú,
  egymáshoz közeli vagy részben átfedő köröket, amennyiben ezekből egyértelmű, egyszerű
  kontúr alakítható ki.
- **FR-004**: A skinning eredménye MUST egyetlen folytonos, zárt és önmetszésmentes határt
  alkosson, amely körülveszi a bemeneti köröket, és az alakzat útvonala MUST kövesse a körök
  megadási sorrendjét.
- **FR-005**: A rendszer MUST csak akkor utasítsa el a konfigurációt, ha a körök megadási
  sorrendjét követő, folytonos és egyszerű skinning kontúr nem állítható elő az alakzat
  szándékának megváltoztatása nélkül; az elutasítást érthető visszajelzés kísérje.
- **FR-006**: Elutasítás esetén a rendszer MUST őrizze meg az összes megadott kört és azok
  sorrendjét, és tegye lehetővé a további szerkesztést.
- **FR-007**: A kör hozzáadása, mozgatása vagy átméretezése MUST frissítse a skinning
  megjelenítését, vagy érvénytelen eredmény esetén a visszajelzést.
- **FR-008**: A skinning robusztusságának javítása MUST ne módosítsa a Disk-Bézier mód
  eredményét vagy a közös köradatokat.

### Key Entities

- **Rendezett körsorozat**: A felhasználó által megadott, középponttal és pozitív sugárral
  rendelkező körök sorozata, amelynek sorrendje az alakzat útvonalát meghatározza.
- **Skinning kontúr**: A körsorozatot körülvevő folytonos, zárt határ; érvényes eredmény esetén
  egyszerű, önmetszésmentes alakzat.
- **Geometriai határeset**: Olyan kanyar-, távolság- vagy sugárkonfiguráció, amely a kontúr
  előállítását instabillá vagy lehetetlenné teheti.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Egy előre rögzített, esetenként elvárt eredménnyel megjelölt geometriai
  stresszteszt-készlet minden érvényes esetéhez folytonos, zárt és önmetszésmentes skinning
  alakzat jelenik meg; a készlet legalább egy 150 fokos irányváltozást, majdnem egyenes
  átmenetet, jelentősen eltérő sugarakat, valamint közeli és átfedő köröket tartalmaz.
- **SC-002**: A stresszteszt-készlet minden érvénytelennek megjelölt eseténél érthető
  visszajelzés jelenik meg, és a körök, valamint a sorrendjük változatlan marad.
- **SC-003**: A körök helyének vagy sugarának módosítása után a következő megjelenítés már az
  új adatokból származik; érvényes kontúr nem marad elavult visszajelzés vagy korábbi alakzat
  miatt.
- **SC-004**: A Disk-Bézier mód megjelenítése és a körsorozat adatai változatlanok maradnak a
  skinning szélső eseteinek kezelése során.

## Assumptions

- A funkció a meglévő skinning mód geometriájának szélső konfigurációk melletti kezelésére
  vonatkozik; új görbemód vagy körszerkesztési folyamat nem része.
- A skinning egy, a körök megadási sorrendjét követő csőszerű alakzatot jelent, nem a bemeneti
  körkorongok halmazának egyszerű egyesítését vagy a teljes sorozatot elfedő konvex burkot.
- A körsorrend a középvonal útvonalát határozza meg; a határvonal bejárási sorrendje nem
  azonos a körlista sorrendjével.
- Az irányváltozás a szomszédos körközéppontokat összekötő szakaszok iránya közötti szöget
  jelenti; a 150 fokos támogatás célzott alsó határ a majdnem visszaforduló kanyarokra.
- A rendszernek a sorrendet követő, önmetszésmentes skinning határral nem rendelkező
  konfigurációkat nem kell mesterségesen átalakítania; ezeknél a visszajelzés és a bemenet
  megőrzése az elvárt viselkedés.
- A körök megadási sorrendje a felhasználó szándékát fejezi ki, ezért a rendszer nem rendezheti
  át és nem módosíthatja automatikusan a köröket a kontúr létrehozásához.
