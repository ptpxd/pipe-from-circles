# Tasks: Robusztus kör-bőrözés éles kanyarokban

**Input**: Tervezési anyagok a `/specs/004-sharp-turn-skinning/` könyvtárból

**Előfeltételek**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`

**Tesztelés**: A terv és a quickstart automatizált stressz- és regressziós teszteket ír elő;
ezek külön, felhasználói történetekhez rendelt feladatok.

**Szervezés**: A feladatok történetenként csoportosulnak. A P1 történet önálló MVP-ként
ellenőrizhető; a további történetek ugyanazt a geometriai modult bővítik.

## Formátum

Minden feladat a `- [ ] T### [P?] [US#] Leírás fájlútvonallal` formátumot követi.
A `[P]` jelölés csak külön fájlokon, függőség nélkül párhuzamosítható feladatokat jelöl.

## Phase 1: Setup

**Cél**: A projekt inicializálása.

Új projekt-inicializálás nem szükséges: a Python-alkalmazás, a `unittest` tesztfuttatás és a
geometriai modul már létezik. Nincs Setup-feladat.

---

## Phase 2: Foundational

**Cél**: Minden történet előtt szükséges közös infrastruktúra.

A meglévő `Circle`, `SkinningError` és `sample_skinning` belső interfészek elegendők; nincs új
függőség, tárolási réteg vagy közös adatmodell. Nincs blokkoló Foundational-feladat.

---

## Phase 3: User Story 1 - Bőrözés éles kanyaroknál (Priority: P1) 🎯 MVP

**Cél**: Az éles, akár 170 fokos irányváltozású, érvényesen körülvehető sorozatok
folytonos, zárt skinning kontúrt adjanak, miközben a normál konfigurációk viselkedése és a
köradatok megmaradnak.

**Független ellenőrzés**: A `tests/test_geometry.py` éles kanyart tartalmazó bemeneteken
ellenőrzi a zárt, folytonos, önmetszésmentes határt és a körök befoglalását; a
`tests/test_app_modes.py` ellenőrzi a skinning megjelenítését, a körlista változatlanságát és a
Disk-Bézier mód regresszióját.

### Megvalósítási feladatok

- [X] T001 [P] [US1] Rögzíts elvárt eredményű, akár 170 fokos éles kanyarú geometriateszteket a `tests/test_geometry.py` fájlban.
- [X] T002 [P] [US1] Adj hozzá felületi regressziós tesztet, amely érvényes éles kanyarnál kontúrt rajzol, és megőrzi a körlistát a `tests/test_app_modes.py` fájlban.
- [X] T003 [P] [US1] Cseréld le a `geometry.py` fájlban az éles kanyarokat általánosan elutasító logikát stabil kanyarátmenetre, miközben a már érvényes, szokásos Hermite-esetek viselkedése megmarad.
- [X] T004 [US1] Ellenőrizd a teljes skinning határt a `geometry.py` fájlban: legyen zárt, folytonos, önmetszésmentes és fogja körül a bemeneti köröket.

**Ellenőrzési pont**: A P1 történet a fenti geometriatesztekkel és felületi ellenőrzéssel
önállóan működik; a körlista és a Disk-Bézier eredménye változatlan.

---

## Phase 4: User Story 2 - Különböző méretű és közelségű körök kezelése (Priority: P2)

**Cél**: Az eltérő sugarú, közeli és részben átfedő körökből is készüljön érvényes, sorrendet
követő kontúr, amikor a konfiguráció megfelel a kontúr feltételeinek.

**Független ellenőrzés**: Előre érvényesnek és érvénytelennek jelölt esetek ellenőrzik a
kontúr topológiáját, a körök lefedését, az érthető hibajelzést és a bemenet változatlanságát.

### Megvalósítási feladatok

- [X] T005 [P] [US2] Adj hozzá előre besorolt teszteseteket eltérő sugarakra, közeli, csaknem érintkező és átfedő körökre a `tests/test_geometry.py` fájlban.
- [X] T006 [P] [US2] Kezeld a `geometry.py` fájlban a változó sugarak, a degenerálódó közös érintők és a körök közötti átfedések érvényes átmeneteit úgy, hogy a sorrendet követő kontúr megmaradjon.
- [X] T007 [P] [US2] Ellenőrizd a `tests/test_app_modes.py` fájlban, hogy sikeres és elutasított átfedő-kör konfigurációnál a körök szerkeszthetők és változatlan sorrendűek maradnak.

**Ellenőrzési pont**: Minden előre érvényesnek jelölt P2 eset érvényes kontúrt ad; az
elutasított esetek nem módosítják a bemenetet.

---

## Phase 5: User Story 3 - Stabil eredmény határhelyzetekben (Priority: P3)

**Cél**: A majdnem egyenes, közel egybeeső, jelentősen eltérő léptékű vagy valóban
önmetsző konfigurációk kezelése stabil eredményt vagy érthető elutasítást adjon összeomlás
nélkül.

**Független ellenőrzés**: A geometriatesztek közel kollineáris, ismétlődő középpontú,
méretarányban eltérő és visszaforduló körsorozatokat futtatnak; a felületi tesztek igazolják,
hogy hibánál nem jelenik meg érvénytelen kontúr, és minden kör megmarad.

### Megvalósítási feladatok

- [X] T008 [P] [US3] Rögzíts elvárt eredményű teszteket majdnem egyenes, közel egybeeső, több léptékű és önmetsző konfigurációkra a `tests/test_geometry.py` fájlban.
- [X] T009 [P] [US3] Válts léptékarányos geometriai döntésekre és kezeld explicit módon a közel-nullás határeseteket a `geometry.py` fájlban, hogy a méretarány ne okozzon önkényes elutasítást.
- [X] T010 [P] [US3] Teszteld, hogy elutasított skinning konfigurációnál a `tests/test_app_modes.py` fájlban érthető státuszüzenet jelenik meg, nem rajzolódik hibás cső, és a körlista szerkeszthető marad.

**Ellenőrzési pont**: A stresszteszt-készlet minden esetén az elvárt érvényes kontúr vagy
érthető hibaállapot jelenik meg; nincs összeomlás vagy adatvesztés.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Cél**: A felhasználói leírás és a végső ellenőrzés összehangolása.

- [X] T011 [P] Frissítsd a `README.md` fájl skinning-részét az éles kanyarok és határesetek új viselkedésével, az érvénytelen konfigurációk megőrzött visszajelzésével.
- [X] T012 [P] Futtasd végig a `specs/004-sharp-turn-skinning/quickstart.md` célzott és teljes tesztellenőrzéseit, és javítsd a `geometry.py`, `tests/test_geometry.py`, `tests/test_app_modes.py` vagy `README.md` fájlban az ebből eredő, funkcióhoz tartozó hibákat.

---

## Függőségek és végrehajtási sorrend

### Fázisfüggőségek

- **Setup (Phase 1)**: Nincs feladat; a meglévő projektstruktúra használható.
- **Foundational (Phase 2)**: Nincs feladat; a jelenlegi modellek és belső függvények megfelelőek.
- **US1 (Phase 3)**: Közvetlenül elkezdhető.
- **US2 (Phase 4)**: Az US1 stabil kontúrképzésére épül.
- **US3 (Phase 5)**: Az US1 és US2 kontúr- és átfedéskezelésére épül.
- **Polish (Phase 6)**: Az elkészült felhasználói történetek után következik.

### Történetfüggőségek

- **US1 (P1)**: Nincs előfeltétele; önálló MVP.
- **US2 (P2)**: US1 után, mert ugyanazt a skinning geometriát bővíti eltérő sugarakra és
  átfedésekre.
- **US3 (P3)**: US2 után, mert a degenerált esetek és a numerikus stabilitás a kanyar- és
  átfedéskezelés végleges geometriájára támaszkodik.

### Párhuzamosítási lehetőségek

- **US1**: T001 és T002 párhuzamosítható külön tesztfájlokon; T003 a geometrián dolgozik velük
  párhuzamosan. T004 T003 után következik, mert az új geometriát validálja.
- **US2**: T005, T006 és T007 párhuzamosítható; külön fájlokat érintenek.
- **US3**: T008, T009 és T010 párhuzamosítható; külön fájlokat érintenek.
- **Polish**: T011 dokumentációs munkája és T012 tesztfuttatása párhuzamosítható az
  implementáció lezárása után.

## Párhuzamos példa: User Story 1

```text
Task: "T001 éles kanyarok geometriatesztjei — tests/test_geometry.py"
Task: "T002 skinning felületi regresszió — tests/test_app_modes.py"
Task: "T003 stabil kanyarátmenet — geometry.py"
```

T004 csak T003 után végezhető el, mert a teljes határ validálásához az új kanyarátmenet
szükséges.

## Megvalósítási stratégia

### MVP először

1. Az US1 tesztjeivel és kanyarátmenetével távolítsd el az éles kanyarok indokolatlan
   elutasítását.
2. Ellenőrizd, hogy az új kontúr zárt, önmetszésmentes, körbefogja a bemenetet, és a
   Disk-Bézier viselkedés változatlan.
3. Az US1 önálló ellenőrzése után az alkalmazás már demonstrálható P1 MVP-ként.

### Fokozatos szállítás

1. US1: éles kanyarok és zárt kontúr.
2. US2: eltérő sugarak, közeli és átfedő körök.
3. US3: numerikus és topológiai határesetek, érthető elutasítás.
4. Polish: README és a quickstart teljes ellenőrzése.

## Formátumellenőrzés

Minden végrehajtható feladat `- [ ]` jelöléssel, növekvő T-sorszámmal, szükség szerint `[P]`
jelöléssel, a történetfázisokban `[US#]` címkével és konkrét fájlútvonallal szerepel.

## Phase 7: Convergence

- [X] T013 Biztosítsd, hogy a mintavételezett skinning kontúr a teljes bemeneti köröket befoglalja, ne csak a sugaruk 99,7%-áig, és rögzíts ezt ellenőrző tesztet a `geometry.py` és `tests/test_geometry.py` fájlokban per FR-004, SC-001 (partial).
- [X] T014 Mérd meg a skinning újrarajzolási idejét reprezentatív, mérsékelt körsorozatokon, és ha a 32 mintapont/szakasz vagy a páronkénti metszésvizsgálat lassú, optimalizáld a `geometry.py` fájlt a befoglalási pontosság megőrzésével per plan: efficiency goal (partial).
