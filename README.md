# Körökből képzett cső

Egyszerű interaktív rajzalkalmazás, amely a felhasználó által megadott körökből
Disk-Bézier vagy skinning mode csövet jelenít meg.

## Előfeltételek

- Windows
- `uv` csomag- és Python-kezelő

## Indítás

Nyiss PowerShellt a projekt mappájában, majd indítsd el az alkalmazást:

```powershell
uv run --no-project --python 3.14 python main.py
```

Az `uv` automatikusan letölti a Pythont, ha a kért verzió még nincs telepítve. A Tkinter
elérhetőségét ezzel ellenőrizheted:

```powershell
uv run --no-project --python 3.14 python -c "import tkinter; print('Tkinter OK')"
```

Ha már telepített, PATH-ban elérhető Pythonod van Tkinterrel, az alkalmazás a szokásos módon
is futtatható:

```powershell
python main.py
```

## Használat

1. Kattints a fehér rajzfelületre egy kör középpontjának megadásához.
2. Kattints egy másik helyre a sugár megadásához. A két kattintás távolsága lesz a kör sugara.
3. Legalább két kör után megjelenik a csőszerű alakzat.
4. További körök hozzáadásakor az alakzat automatikusan frissül.
5. A **Görbemód** választóval válts a Disk-Bézier és a skinning mode között.
6. Skinning módban a bemeneti körök teljes belseje kékkel van kitöltve.
7. A kör két szemközti fogópontjának húzásával módosítsd a sugarát; a kör középpontja nem
   változik.
8. A kör belsejét a fogópontoktól távolabb húzva mozgasd a kört; a sugara változatlan marad.
9. A görgővel nagyíts vagy kicsinyíts a mutató helye körül.
10. A középső egérgomb nyomva tartásával húzd el a nézetet.
11. A rajzfelületre kattintás után a **Backspace** megszakítja a függőben lévő körközéppont
   megadását; máskülönben eltávolítja az utolsó teljes kört.

Ha a sugár megadásakor ugyanoda kattintasz, mint a középpontnál, a kör nem jön létre. Kattints
ismét, a középponttól eltérő helyre.

A körök sorrendben Disk-Bézier vezérlőkorongként szerepelnek. Az első és az utolsó körhöz
illeszkedik a görbe; a belső körök vezérlőadatok, ezért nem feltétlenül érinti őket a cső.
Skinning módban a körök irányát követő Hermite-szakaszok és kerekített végzárások alkotják a
kontúrt. Az éles, akár közel 170 fokos kanyarok, a közel egyenes szakaszok, az eltérő méretű
körök, valamint a közeli vagy részben átfedő körök is működhetnek, ha egyszerű, a köröket
körülvevő kontúr készíthető. A rendszer a teljes kontúrt ellenőrzi; ha egy konfiguráció
egybeeső középpont, egymásba ágyazott kör, visszafordulás vagy önmetszés miatt nem kezelhető,
érthető hibaüzenetet ad, de a köröket és sorrendjüket megőrzi. Ilyenkor folytathatod a
szerkesztést, vagy visszaválthatsz Disk-Bézier módra.

## Tesztek futtatása

PowerShellben, a projekt gyökérkönyvtárából:

```powershell
uv run --no-project --python 3.14 python -m unittest discover -s tests -v
```

## Felhasznált könyvtárak

- `tkinter` — a Python standard library része; az ablak, egérkattintás-kezelés és rajzfelület.
- `dataclasses`, `math`, `typing` — a Python standard library részei; a geometriai adatok és
  számítások.

Nincs szükség külső Python-csomag telepítésére.
