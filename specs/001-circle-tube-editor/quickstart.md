# Quickstart és ellenőrzés

## Előfeltételek

- Windows számítógép.
- Python 3.10 vagy újabb, Tk támogatással.

## Tkinter ellenőrzése

A projekt gyökérkönyvtárából PowerShellben futtasd:

```powershell
python -m tkinter
```

Siker esetén megjelenik a Tkinter próbaablaka. Zárd be, mielőtt elindítod az alkalmazást.

## Alkalmazás indítása

```powershell
python main.py
```

Elvárt eredmény: megjelenik egy üres rajzfelület.

## Kézi ellenőrzési forgatókönyv

1. Kattints a rajzfelületre a kör középpontjának megadásához.
2. Kattints egy másik helyre a sugár megadásához; ellenőrizd a kör megjelenését.
3. Adj meg egy második kört; ellenőrizd, hogy a csőszerű alakzat is megjelenik.
4. Adj hozzá egy további, eltérő sugarú kört; ellenőrizd, hogy az alakzat automatikusan
   frissül.
5. A sugár megadásakor kattints újra a középpontba; ellenőrizd, hogy nulla sugarú kör nem jön
   létre, és a következő sugárkattintás még ugyanahhoz a középponthoz tartozik.

## Könyvtárak

Az alkalmazás nem igényel harmadik féltől származó Python-csomagot. Az ablak és a rajzfelület
a Python standard library `tkinter` modulját használja.
