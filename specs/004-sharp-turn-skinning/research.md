# Kutatási döntések: Robusztus kör-bőrözés éles kanyarokban

## 1. A bőrözés geometriai jelentése

**Döntés**: A bőrözés a körök megadási sorrendje által meghatározott, változó sugarú csőszerű
alakzatot jelent. Nem a bemeneti körkorongok halmazának egyszerű egyesítése, és nem az egész
körsorozatot elfedő konvex burok.

**Indoklás**: A körök rendezett vezérlőadatok, a meglévő algoritmus pedig a szomszédos körök
közötti oldalgörbékkel és a középpontok útvonalával dolgozik. A körkorongok pontos uniója
eltakarhat egy bemeneti kört, tartalmazhat lyukakat, és nem feltétlenül egyetlen egyszerű
határból áll. A konvex burok mindig ad befoglaló alakzatot, de eltüntetheti a kanyarok
konkáv részeit és a cső útvonalát.

**Elvetett alternatívák**:

- A pontos kör-unió nem őrzi meg önmagában a körsorrend szerinti útvonalat.
- A konvex burok nem követi hűen az útvonalat, és a távoli szakaszokat is összekötheti.

## 2. Kanyarok és határképzés

**Döntés**: A már érvényes, szokásos konfigurációknál maradjon meg a jelenlegi érintőalapú
Hermite-konstrukció. A szélső esetekben a helyi irányvektorok összeadásán alapuló,
közel-kollineáris vagy éles kanyarokat elutasító szabályok helyett stabil kanyarátmenet
szükséges; a teljes kontúrt globálisan is ellenőrizni kell.

**Indoklás**: A lokális, szomszédos körök közötti érintők önmagukban nem garantálják, hogy a
teljes körsorozat határa egyszerű marad. A 150 fokos irányváltozásnál a sima/miter jellegű
átmenetek hosszú túlnyúlást okozhatnak; kerekített átmenet korlátozza ezt a jelenséget.
Majdnem kollineáris szakaszoknál az önkényes szögküszöb helyett a geometriai határesetet kell
kezelni.

**Elvetett alternatívák**:

- Egyetlen globális konvex burok feloldaná az önmetszést, de megváltoztatná az alakzat útvonalát.
- A kizárólag helyi érintőellenőrzés nem észleli az egymást nem szomszédos szakaszok ütközését.

## 3. Numerikus robusztusság

**Döntés**: A távolság- és orientációs döntések léptékarányos tűréssel történjenek; a
közel-nullás eseteket explicit határesetként kell kezelni, nem egyetlen abszolút epsilon alapján
elutasítani. A végleges, mintavételezett határ nem szomszédos éleinek metszésvizsgálata maradjon
kötelező.

**Indoklás**: A fix abszolút küszöbök ugyanazt a geometriát eltérő méretarányokban eltérően
kezelhetik. A robusztus orientációs predikátumok adaptív pontossággal oldják meg azokat a
határeseteket, ahol a lebegőpontos kerekítés megfordíthat egy geometriai döntést.

**Források**:

- [Shewchuk: Adaptive Precision Floating-Point Arithmetic and Fast Robust Predicates](https://www.cs.cmu.edu/~quake/robust.html)
- [CGAL: Kernel robustness](https://doc.cgal.org/latest/Kernel_23/index.html)

**Elvetett alternatíva**: Új külső geometriai függőség bevezetése. A projekt jelenleg Python
standard library-ra épül, nincs függőségi manifestje, és a kért határ a meglévő szerkesztő
közepes méretű körsorozatainak kezelése; először a meglévő, tiszta geometriai modulban érdemes
megoldani a határeseteket.

## 4. Érvénytelenség és visszajelzés

**Döntés**: Az „érvénytelen” az alkalmazás által elvárt, körsorrendet követő egyszerű
csőhatár-konstrukcióra vonatkozzon, nem arra, hogy egyáltalán nem létezhet semmilyen befoglaló
görbe. Ha a követelményeket teljesítő kontúr nem készíthető, a skinning mód adjon visszajelzést,
ne rajzoljon hibás alakzatot, és hagyja érintetlenül a bemeneti köröket.

**Indoklás**: Véges körhalmaz körül mindig készíthető valamilyen befoglaló görbe, például konvex
burok; ez azonban nem feltétlenül követi a felhasználó által megadott útvonalat. A hibajelzés
ezért az útvonalat megőrző konstrukció korlátját magyarázza.

## 5. Tesztstratégia

**Döntés**: A tesztkészlet minden geometriai bemenethez előre rögzített elvárt eredményt
tartalmazzon. Érvényes eseteknél ellenőrizze a zártságot, folytonosságot, egyszerűséget,
bemeneti körök befoglalását és a körlista változatlanságát; érvénytelen eseteknél a visszajelzést
és a bemenet megőrzését.

**Indoklás**: A teszteknek külön kell választaniuk a valódi topológiai hibát az algoritmus
korábbi túlzottan szigorú szög- és kollinearitási küszöbeitől. A készlet fedje le a közel
egyenestől a 150 fokos irányváltozásig terjedő kanyarokat, eltérő sugarakat, közeli és átfedő
köröket, valamint nem szomszédos szakaszok kölcsönhatását.

## Összefoglaló források

- [CGAL: 2D Alpha Shapes](https://doc.cgal.org/latest/Alpha_shapes_2/index.html) — a súlyozott
  alakzatoknál a nem összefüggő és nem egyszerű topológia lehetősége.
- [CGAL: 2D Minkowski Sums](https://doc.cgal.org/latest/Minkowski_sum_2/index.html) — a
  konstans sugarú középvonal-söprés és a változó sugarú modell közötti különbség.
- [GEOS: Buffer parameters](https://libgeos.org/doxygen/classgeos_1_1operation_1_1buffer_1_1BufferParameters.html)
  — kerekített, levágott és miter jellegű kanyarátmenetek, valamint a miter-korlát szerepe.
- [CGAL: Regularized Boolean Set-Operations](https://doc.cgal.org/latest/Boolean_set_operations_2/index.html)
  — a reguláris halmazunió és az egyszerűbb körvonal feltételei.
