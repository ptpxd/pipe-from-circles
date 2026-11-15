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
6. A görgővel nagyíts vagy kicsinyíts a mutató helye körül.
7. A középső egérgomb nyomva tartásával húzd el a nézetet.
8. A rajzfelületre kattintás után a **Backspace** megszakítja a függőben lévő körközéppont
   megadását; máskülönben eltávolítja az utolsó teljes kört.

Ha a sugár megadásakor ugyanoda kattintasz, mint a középpontnál, a kör nem jön létre. Kattints
ismét, a középponttól eltérő helyre.

A körök sorrendben Disk-Bézier vezérlőkorongként szerepelnek. Az első és az utolsó körhöz
illeszkedik a görbe; a belső körök vezérlőadatok, ezért nem feltétlenül érinti őket a cső.
Skinning mode-nál a külső közös érintők, illetve a helyi középponti irányokból számított
érintőpontok adják a Hermite-szakaszok végpontjait. A módszer nem alkalmazható minden
körkonfigurációra: például egybeeső, közel kollineáris, élesen visszaforduló vagy önmetsző
elrendezésnél hibaüzenetet kapsz. Ilyenkor a körök megmaradnak, és visszaválthatsz
Disk-Bézier módra.

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
