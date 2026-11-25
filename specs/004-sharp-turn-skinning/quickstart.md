# Gyors ellenőrzés: Robusztus kör-bőrözés éles kanyarokban

## Előfeltételek

- Windows
- A projekt gyökérkönyvtárából elérhető `uv`
- Python 3.14 és Tkinter; szükség esetén az `uv` letölti a Pythont

## Automatikus ellenőrzések

Futtasd a célzott geometriai teszteket:

```powershell
uv run --no-project --python 3.14 python -m unittest discover -s tests -p test_geometry.py -v
```

Futtasd az alkalmazásmegjelenítést és a körsorrendet is ellenőrző teszteket:

```powershell
uv run --no-project --python 3.14 python -m unittest discover -s tests -p test_app_modes.py -v
```

Végül futtasd a teljes tesztkészletet:

```powershell
uv run --no-project --python 3.14 python -m unittest discover -s tests -v
```

Az ellenőrzéseknek igazolniuk kell, hogy a sikeres kontúr zárt, folytonos, önmetszésmentes,
és körülveszi a bemeneti köröket; az érvénytelen konfiguráció visszajelzést ad és nem változtatja
meg a köröket vagy azok sorrendjét. A meglévő Disk-Bézier teszteknek továbbra is sikeresnek kell
maradniuk.

## Kézi ellenőrzés

1. Indítsd el az alkalmazást:

   ```powershell
   uv run --no-project --python 3.14 python main.py
   ```

2. A rajzfelületen adj meg három, azonos, körülbelül 15 képpont sugarú kört ezekkel a
   középpontokkal: `(120, 200)`, `(260, 200)`, `(139, 270)`. Ez közel 150 fokos irányváltozást
   és éles visszakanyarodást eredményez.
3. Válts Skinning mode-ra. Ha a konfigurációból érvényes határ alakítható ki, ellenőrizd, hogy
   egyetlen zárt, önmetszésmentes alakzat jelenik meg, amely körülveszi mindhárom kört.
4. Mozgasd vagy méretezd át az egyik kört. Ellenőrizd, hogy az alakzat frissül, a többi kör és
   a sorrendjük változatlan marad.
5. Próbálj ki majdnem egyenes, eltérő sugarú, közeli és átfedő köröket is. Minden esetben
   ellenőrizd az érvényes kontúrt vagy az érthető hibaüzenetet, valamint a körök megőrzését.
6. Válts Disk-Bézier módra, és ellenőrizd, hogy a körök adatai nem változtak.

Az adatfogalmakat és invariánsokat lásd a [data-model.md](./data-model.md) fájlban.
