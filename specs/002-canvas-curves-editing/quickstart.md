# Quickstart és ellenőrzés

## Előfeltételek

- Windows.
- `uv`, vagy Python 3.10+ Tkinter támogatással.

## Indítás

A projekt gyökérkönyvtárából PowerShellben:

```powershell
uv run --no-project --python 3.14 python main.py
```

PATH-ban elérhető Python esetén:

```powershell
python main.py
```

## Kézi ellenőrzés

1. Helyezz el legalább két kört, majd görgess az alakzat fölött ki és be.
2. Ellenőrizd, hogy a nagyítás a mutató alatt marad, és a körök aránya változatlan.
3. Középső egérgombbal húzd el a nézetet; ellenőrizd, hogy minden rajzolt elem együtt mozog.
4. Változtass nagyítást vagy húzd el a nézetet, majd helyezz el új kört; ellenőrizd, hogy a
   kattintások a munkaterület megfelelő pontját jelölik, és a kör nem torzul.
5. Nyomj Backspace-t, ellenőrizd az utolsó kör eltűnését, majd adj meg új kört.
6. Válts Disk-Bézier módról kör-bőrözésre és vissza; ellenőrizd, hogy a körök változatlanok.
7. Próbálj ki egy bőrözésre nem alkalmas elrendezést; ellenőrizd a hibaüzenetet, a bemenet
   megtartását és a Disk-Bézier módra való visszaváltást.

## Automatizált ellenőrzések

```powershell
uv run --no-project --python 3.14 python -m unittest discover -s tests -v
```

Elvárt eredmény: a geometriai, körbevitel- és nézetátalakítás-tesztek hibamentesen lefutnak.
