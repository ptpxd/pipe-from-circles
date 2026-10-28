# Adatmodell: Interaktív kör-tube szerkesztő

## Kör

Az egérrel létrehozott vezérlőkorong.

| Mező | Jelentés | Érvényesség |
|---|---|---|
| `center_x` | A középpont vízszintes koordinátája a rajzfelületen | Véges szám |
| `center_y` | A középpont függőleges koordinátája a rajzfelületen | Véges szám |
| `radius` | A középpont és a sugárkattintás távolsága | Véges, pozitív szám |
| sorrend | A kör helye az alkalmazás körlistájában | Megadási sorrend szerint növekvő |

## Disk-Bézier alakzat

Az alakzat a körök rendezett vezérlősorából számolt változó sugarú korongok uniójának
megjelenített közelítése.

| Adat | Jelentés |
|---|---|
| vezérlőkörök | A felhasználó által megadott körök sorrendje |
| paraméter | \(t\in[0,1]\), a görbe helye |
| középpont | A vezérlőközéppontok Bernstein-súlyozott összege \(C(t)\) |
| sugár | A vezérlősugarak azonos Bernstein-súlyokkal képzett összege \(R(t)\) |
| mintakorong | A \(t\) paraméternél középpontú és \(R(t)\) sugarú korong |

Két vagy több érvényes vezérlőkör esetén az alkalmazás megjeleníti a korongunió közelítését.
Egy kör önmagában csak vezérlőkörként látható, tube még nem jön létre.

## Bemeneti állapot

- **Középpont megadására vár**: nincs függő pont; az egér következő kattintása eltárolja a
  középpontot.
- **Sugár megadására vár**: van függő középpont; a következő, attól eltérő kattintás létrehozza
  és a körlista végére fűzi a kört.
- **Érvénytelen sugárkattintás**: a sugár nulla; a rendszer nem hoz létre kört, megtartja a
  függő középpontot, és továbbra is sugárkattintásra vár.
