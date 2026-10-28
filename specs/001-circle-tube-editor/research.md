# Research: Interaktív kör-tube szerkesztő

## Döntések

### Rajzfelület

- **Decision**: A Python beépített Tkinter `Canvas` szolgál az ablak és a 2D rajzfelület
  megjelenítésére.
- **Rationale**: Közvetlenül támogatja az egérkattintásokat, a körök és alakzatok rajzolását,
  Windows alatt széles körben elérhető, és nem igényel harmadik féltől származó csomagot.
- **Alternatives considered**: PySide6/Qt és Pygame. Mindkettő alkalmas, de ehhez az egyszerű,
  egyablakos rajzfeladathoz telepítési és tanulási többletet jelent.

### Körökből származtatott alakzat

- **Decision**: Disk-Bézier görbe. Minden megadott kör egy vezérlőkorong; a középpont és a sugár
  ugyanazzal a Bernstein-súlyozással interpolálódik. A megjelenítés a változó sugarú korongok
  burkolóját közelíti a paraméter mentén mintavételezett alakzattal.
- **Rationale**: Ez közvetlenül használja a körök sorrendjét, középpontját és sugarát, miközben
  nem követeli meg a kör-bőrözési módszer speciális bemeneti feltételeit és érintési pontok
  megoldását. A diszkek uniója koncepcionálisan kezeli azokat az eseteket is, amikor egy szakasz
  lokális differenciál burkolója degenerálódik.
- **Important behavior**: A Disk-Bézier alakzat a szélső vezérlőkorongokhoz illeszkedik; a belső
  körök vezérlőadatok, és nem feltétlenül érintik az alakzatot.
- **Alternatives considered**:
  - **Körök bőrözése**: két legalább G1 folytonos, a köröket érintő görbét állít elő, de megengedett
    bemeneti elrendezésekre támaszkodik, és a geometriai konstrukció bonyolultabb.
  - **Egyedi lokális Hermite-ívek**: pontos körérintési feltételekhez érintési pontok és
    érintővektorok megválasztását igényli, ami a kis kezdeti változathoz több szabályt jelent.

## Geometriai modell

Legyen a bemeneti korongok sora \(D_i=(c_i,r_i)\), ahol \(c_i\) a 2D középpont és \(r_i>0\) a
sugár. A \(t\in[0,1]\) paraméternél:

\[
C(t)=\sum_{i=0}^{n} {n\choose i}(1-t)^{n-i}t^i c_i,\qquad
R(t)=\sum_{i=0}^{n} {n\choose i}(1-t)^{n-i}t^i r_i.
\]

A változó sugarú görbe korongja \(D(t)=\{x:\|x-C(t)\|\le R(t)\}\), az alakzat pedig ezek uniója.
Az alkalmazás ennek a burkolóját rajzolja közelítő mintavételezéssel. A nemnegatív vezérlősugarak
nemnegatív interpolált sugarat eredményeznek.

Az analitikus oldalsó burkoló csak ott valós, ahol
\(\|C'(t)\|>|R'(t)|\); álló középvonal, gyorsan változó sugár, illetve egymásba ágyazott
korongok külön kezelést igényelnek. Ezért a kezdeti megjelenítés mintavételezett koronguniót
használ, nem feltételezi, hogy az analitikus oldalsó burkoló minden bemenetre létezik.

## Felületi interakció

- Az első kattintás eltárolja a függőben lévő kör középpontját.
- A következő kattintás távolsága adja a sugarat.
- Nulla távolságnál a felhasználó új sugárkattintást adhat meg; a függő középpont nem vész el.
- Érvényes kör esetén a körsorozat bővül, majd a vezérlőkorongok és a származtatott alakzat
  újrarajzolódik.

## Források

- `Task_2_Disk_Bezier_paper.pdf`, különösen a Disk-Bézier definíciója és burkolóképlete.
- `Task_2_Skinning_of_circles_paper.pdf`, a bőrözés bemeneti feltételei és folytonossági
  tulajdonságai.
- Python dokumentáció: Tkinter Canvas alkalmas körök, sokszögek és egér-események rajzolására;
  a Tkinter elérhetőségét a `python -m tkinter` paranccsal lehet ellenőrizni.
