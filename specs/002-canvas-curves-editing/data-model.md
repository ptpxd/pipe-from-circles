# Adatmodell: Nézetvezérlés és görbemód-választás

## Kör

A meglévő, változatlanul megőrzendő vezérlőadat.

| Mező | Jelentés | Érvényesség |
|---|---|---|
| `center_x`, `center_y` | Középpont a munkaterület világkoordinátáiban | Véges számok |
| `radius` | Sugár világkoordinátában | Véges, pozitív szám |
| sorrend | A kör helye a körlistában | Felhasználói megadási sorrend |

## Nézetállapot

| Mező | Jelentés | Érvényesség |
|---|---|---|
| `scale` | Egyenletes képernyő-/világkoordináta arány | Pozitív, korlátozott tartomány |
| `offset_x`, `offset_y` | Világkoordináta-rendszer kezdőpontjának képernyőbeli eltolása | Véges számok |

- Előretranszformáció: \(s_x=o_x+s\cdot w_x\), \(s_y=o_y+s\cdot w_y\).
- Inverz transzformáció: \(w_x=(s_x-o_x)/s\), \(w_y=(s_y-o_y)/s\).
- A sugárkattintás és a középpont egyaránt inverz transzformációval alakul át, ezért a
  körvilágban mért távolság a nagyítástól független.

## Görbemód

- **Disk-Bézier**: a meglévő, rendezett `Circle` listán alapuló középpont- és sugárgörbe.
- **Kör-bőrözés**: a rendezett körlistához számított két érintő határgörbe, lokális Hermite
  szakaszokkal; egyes bemeneteknél `SkinningError` jelzi, hogy nem alkalmazható.
- A módválasztó alapértéke Disk-Bézier. A kiválasztott módszer önmagában nem módosítja a
  körlistát.

## Beviteli állapot

- **Középpontra vár**: nincs ideiglenes középpont; a következő bal kattintás világkoordinátában
  eltárolódik.
- **Sugárra vár**: a sugárkattintás a középponttól eltérő világpontot jelöl ki.
- **Húzás**: középső gombbal indított, képernyőpixelben mért eltolásmódosítás; nem helyez le
  kört.
- **Backspace**: ideiglenes középpont esetén azt törli; egyébként a lista utolsó teljes körét
  távolítja el, ha létezik.
