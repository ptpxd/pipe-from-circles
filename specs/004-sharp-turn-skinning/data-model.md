# Adatmodell: Robusztus kör-bőrözés éles kanyarokban

## Rendezett körsorozat

A szerkesztő által kezelt bemeneti körök listája.

| Mező | Jelentés | Szabály |
|---|---|---|
| Középpont | A kör munkaterületi X és Y koordinátája | Mindkét koordináta véges szám |
| Sugár | A kör mérete | Véges, pozitív érték |
| Sorrend | A kör helye a felhasználó által megadott sorozatban | A skinning nem rendezheti át és nem módosíthatja |

A körsorozat bőrözés közben csak olvasható bemenet. A bőrözés hibája nem távolíthat el,
nem mozgathat el és nem méretezhet át kört.

## Skinning kontúr

A körsorozatból származtatott vizuális határ.

| Tulajdonság | Érvényes eredmény |
|---|---|
| Kapcsolat | Egyetlen, folytonos és zárt határ |
| Metszés | A határ nem metszi önmagát |
| Körök lefedése | A határ egyetlen körülzárt tartományban fogja közre a bemeneti köröket |
| Útvonal | A csőszerű alakzat középvonala követi a megadási sorrendet |
| Frissesség | A legutóbbi körmódosításból származik |

A kontúr nem a körsorozat tartós adata: minden újraszámításkor az aktuális bemenetből
származik. A körlista sorrendje az útvonalat határozza meg; a kontúr határpontjainak sorrendje
ettől eltérhet. A kontúr nem a bemeneti körkorongok egyszerű halmazegyesítése, és nem
helyettesíthető a teljes útvonalat elfedő konvex burokkal.

## Bőrözési eredmény

A megjelenítés állapota a bőrözés legutóbbi kéréséhez.

- **Érvényes**: rendelkezésre áll a megjeleníthető, érvényes skinning kontúr.
- **Nem előállítható**: a konfigurációhoz nem alakítható ki a körök megadási sorrendjét
  követő, a bemeneti köröket körülvevő egyszerű határ; a felhasználó érthető visszajelzést kap,
  miközben a körsorozat megmarad.

Kör hozzáadása, mozgatása vagy átméretezése után az eredmény állapotát újra kell meghatározni.
Másik görbemód választása nem változtatja meg a körsorozatot.
