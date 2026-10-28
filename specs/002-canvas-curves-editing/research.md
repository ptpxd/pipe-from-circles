# Kutatás: Nézetvezérlés és görbemód-választás

## Döntések

### Nézet és egérkoordináták

- **Decision**: A körök és görbék világkoordinátákban tárolódnak. A felület egyenletes
  méretezést és eltolást használ: képernyőpont = eltolás + nagyítás × világpont. A görgő az
  egérmutató alatti világpontot rögzíti nagyítás közben; a középső gomb húzása az eltolást
  módosítja. Mindkét kattintás világkoordinátára alakul, így a sugár mértéke nem változik
  különböző nagyítások között.
- **Rationale**: Egyszerű, invertálható transzformáció, amely a körgeometriát és meglévő
  Disk-Bézier számítást érintetlenül hagyja.
- **Alternatives considered**: A Canvas natív görgetőrégiója az alkalmazás saját rajzolási
  transzformációjával keverné a koordinátarendszereket; ezért nem használjuk.

### Kattintási bevitel és Backspace

- **Decision**: A Canvas fókuszt kap kattintás után. A Backspace először a függőben lévő
  középpontot szakítja meg; ha ilyen nincs, egy teljes legutolsó kört távolít el. Üres listán
  hatástalan. Minden változás után az aktuális görbemód szerint újrarajzolunk.
- **Rationale**: A megkezdett, de be nem fejezett kör visszavonható anélkül, hogy teljes kör
  törlődne a felhasználó várakozásával ellentétben.
- **Alternatives considered**: A Backspace globális kötése más későbbi szövegbeviteli vezérlők
  billentyűit is elfogná; ezért a vászon fókuszához kötött.

### Disk-Bézier

- **Decision**: A meglévő `evaluate_disk_bezier`, `sample_disk_bezier` és
  `disk_bridge` marad az alapértelmezett mód; csak a kiválasztott mód közös megjelenítési
  határán csatlakozik hozzá a felület.
- **Rationale**: Megőrzi a korábban ellenőrzött működést és a körök vezérlőkorongként való
  értelmezését.
- **Alternatives considered**: A meglévő geometriát újraíró közös görbeabsztrakció növelné a
  változtatás kockázatát és a szükséges architektúrát.

### Kör-bőrözés

- **Decision**: Két kör esetén a két külső közös érintő adja az oldalsó határok kontaktpontjait.
  Három vagy több kör esetén a szomszédos középpontokat összekötő egységvektorok biszektora
  határozza meg a köztes körök helyi érintőirányát, a kontaktpontokat pedig ez az irány és a
  körök sugara adja. Az oldalsó pontokat közelítőleg G1 folytonos lokális Hermite-szakaszok
  kötik össze; a végkörök Hermite-ívei zárják a kontúrt.
- **Rationale**: Ez teljesíti a második, köröket érintő módszer lényegét, és a feladatban
  megnevezett lokális Hermite-szakaszokat használja. A módszer külön marad a Disk-Bézier
  modelljétől.
- **Admissibility**: Legalább két véges, pozitív sugarú kör szükséges. A kétkörös esetben a
  külső közös érintők szükségesek. Három vagy több körnél elutasítjuk az egybeeső egymást
  követő középpontokat, a kollineáris vagy közel kollineáris egymást követő körhármast, az éles
  irányváltást, a más kör belsejébe eső kontaktpontot, az önmetsző vagy nem biztonságosan
  zárható kontúrt. A módszer nem ígér megoldást minden körkonfigurációra.
- **Error behavior**: A geometriai függvény konkrét `SkinningError` hibát ad. A felület a
  hibaüzenetet megjeleníti, megőrzi a körlistát és nem rajzol hibás eredményt. A felhasználó
  visszaválthat Disk-Bézier módra.
- **Alternatives considered**:
  - A csak páronkénti érintőhidakból összerakott alakzat egyszerűbb, de nem adja a tanulmány
    közbenső köröket érintő, kétoldali konstrukcióját.
  - A tanulmány teljes Apollonius-konstrukciója összetettebb; az első változat az iránybiszektort
    választja az egyszerűbb, követhetőbb implementáció érdekében, és elutasítja a nem támogatott
    bemeneteket.

## Geometriai ellenőrzések

- Egy érintési pont a saját körén van, és a Hermite-érintő merőleges a sugárra.
- Szomszédos Hermite-szakaszok ugyanabban az érintési pontban találkoznak, és érintőirányaik
  egy oldalon megegyeznek.
- Kétkörös módban a lehetetlen külső közös érintőt igénylő eset determinisztikus hibát ad.
- Egy nem elfogadható hármas vagy más kör belsejébe kerülő érintés nem eredményez rajzolt
  bőrözési kontúrt.
- Transzláció, forgatás és egyenletes skálázás az érintési geometriát ugyanígy transzformálja.
- A Disk-Bézier végpontjai, mintái és meglévő körhídja regressziótesztekkel változatlanok
  maradnak.

## Források

- `Task_2_Skinning_of_circles_paper.pdf`, nyomtatott 612–617. oldal: admisszibilitás,
  érintési pontok, Apollonius-konstrukció és Hermite-interpoláció; az implementáció ezek közül
  az érintőpontok és Hermite-szakaszok alapelvét követi, de egyszerűsített kontaktpont-választást
  használ.
- `Task_2_Disk_Bezier_paper.pdf`, nyomtatott 722. oldal és a cikk 721–737. oldala:
  Disk-Bézier korongmodell és változó vastagságú görbe.
- Tcl/Tk Canvas események: `<MouseWheel>`, `<ButtonPress-2>`, `<B2-Motion>`,
  `<ButtonRelease-2>`, illetve `canvasx`/`canvasy` a Canvas natív görgetése esetén.

Az implementáció egyszerűbb, lokális iránybiszektorra épülő kontaktpont-választást használ;
nem valósítja meg a tanulmány teljes Apollonius-konstrukcióját. Emiatt csak a dokumentáltan
stabil konfigurációkra ad eredményt, más esetekre egyértelmű hibával tér vissza.
