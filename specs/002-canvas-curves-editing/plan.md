# Implementation Plan: Nézetvezérlés és görbemód-választás

**Branch**: `002-canvas-curves-editing` | **Date**: 2026-10-28 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-canvas-curves-editing/spec.md`

## Summary

Bővítsük a meglévő, Python/Tkinter-alapú kör-tube szerkesztőt kurzorközpontú görgős nagyítással,
középső egérgombbal történő pásztázással, Backspace-es utolsó-kör-eltávolítással és választható
Disk-Bézier/kör-bőrözési megjelenítéssel. A köradatok világkoordinátákban maradnak; a nézet
csupán rajzoláskor alakítja át őket. A bőrözés két érintő oldalgörbét alkotó, lokális Hermite
szakaszokkal készül, és világosan elutasítja a nem támogatott bemeneti geometriát. A meglévő
Disk-Bézier mód és alkalmazásindítás változatlanul elérhető marad.

## Technical Context

**Language/Version**: Python 3.10+

**Primary Dependencies**: Tkinter és Python standard library; nincs külső függőség

**Storage**: N/A; körök, görbemód és nézetállapot csak az alkalmazás futása alatt élnek

**Testing**: Standard library `unittest` a geometriához és beviteli állapotokhoz; rejtett
Tkinter-ablakos eseménytesztek és kézi vizuális ellenőrzés

**Target Platform**: Windows asztali alkalmazás Tkinter-támogatású Python 3.10+ környezetben

**Project Type**: Meglévő, egyprojektű Python asztali alkalmazás

**Performance Goals**: A nagyítás, pásztázás, módváltás és körmódosítás után a vászon azonnali
újrarajzolása; a jelenlegi 120 Disk-Bézier minta megőrzése

**Constraints**: A geometriai köradatok világkoordinátákban maradnak; a sugár kattintási
távolságát ugyanabban a világkoordináta-rendszerben kell mérni. A skinning csak ellenőrzött,
megengedett konfigurációknál készülhet el; sikertelen konstrukció nem törölheti a köröket.
Meglévő Disk-Bézier viselkedés regresszió nélkül maradjon.

**Scale/Scope**: Egy felhasználó, egy munkamenet és mérsékelt számú rendezett kör; nincs
mentés/exportálás vagy közvetlen fogópontos körszerkesztés.

## Constitution Check

- **Clarity and understandability**: A geometriát, a beviteli állapotot és a nézet megjelenítését
  külön modulban tartjuk; a két görbemód egyértelműen választható és megnevezett.
- **Simplicity**: A meglévő Tkinter- és standard-library megoldást bővítjük új függőségek nélkül.
- **Efficiency**: A nézet- és modellállapot változásakor rajzolunk újra; nem fut folyamatos
  animáció vagy háttérfolyamat.
- **Correctness and validation**: A világ-/képernyőkoordináták átalakítását, a Backspace
  állapotát és a Hermite-érintőket célzott tesztekkel ellenőrizzük.
- **Focused, maintainable changes**: Csak a kért navigációt, utolsó kör eltávolítását,
  módkapcsolást, geometriai skinninget, teszteket és futtatási dokumentációt módosítjuk.

**Gate result**: PASS. A terv meglévő alkalmazást bővít, külső függőséget nem vezet be, és
egyértelműen visszautasítja azokat a bőrözési konfigurációkat, amelyekre a geometria nem ad
megbízható eredményt.

## Project Structure

### Documentation (this feature)

```text
specs/002-canvas-curves-editing/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── checklists/requirements.md
```

### Source Code (repository root)

```text
main.py                    # Alkalmazás belépési pontja; meglévő szerepében változatlan
app.py                     # Vászon, vezérlők, nézettranszformáció és eseménykötések
editor.py                  # Körlista, kétkattintásos bevitel, utolsó kör visszavonása
geometry.py                # Meglévő Disk-Bézier mellett kör-bőrözés és Hermite-szakaszok
tests/
├── test_app.py            # Nézettranszformáció és átalakított körbevitel
├── test_app_modes.py      # Módváltás és felületi hibakezelés
├── test_geometry.py       # Bézier-regresszió, tangencia, skinning és hibás bemenet
└── test_editor.py         # Körbevitel és utolsó kör eltávolítása
README.md                  # Frissített indítási és használati útmutató
```

**Structure Decision**: A már létező gyökérmodulokat bővítjük. Külön tesztkönyvtárba csak a
standard-library `unittest`-teszteket tesszük; nem hozunk létre alkalmazáscsomagot vagy új
függőséget.

## Complexity Tracking

Nincs alkotmányos eltérés. A kör-bőrözés geometriai összetettsége a kért második görbemód
közvetlen következménye; a nem biztonságosan kezelhető esetek hibával térnek vissza.
