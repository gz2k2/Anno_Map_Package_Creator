> **Deutsche Dokumentation verfügbar:** [Direkt zur deutschen Anleitung springen](#deutsche-dokumentation)

---

# Anno Map Package Creator

A desktop tool for organizing custom `.a7m` island maps into reusable **Map Packages** and exporting them as ready-to-use mods for **Anno 117** and **Anno 1800**.

The application provides a guided workflow for importing maps, assigning regions and GUIDs, grouping maps into packages, adding extra mod files, and generating the game-specific mod structure and `assets.xml` automatically.

## Features

- Supports **Anno 117** and **Anno 1800** from one interface.
- Imports individual `.a7m` files or recursively scans folders for maps.
- Assigns and manages GUIDs, regions, map types, and Map Packages.
- Supports `Normal` and `Decoration` island types.
- Creates reusable Map Packages with Mod Name, Version, Region, and optional package-specific GUID ranges.
- Supports custom game regions and region IDs.
- Supports **Additional Files** that are copied into the root of the exported mod.
- Generates the required game-specific `assets.xml` and `modinfo.json`.
- Exports map source folders, including their related files and subfolders.
- Performs exports in a background worker and shows a live autoscrolling export log.
- Includes separate default export paths for Anno 117 and Anno 1800.
- Dark-mode CustomTkinter interface with sortable tables.

---

# Quick Workflow: Create a Map Package

This is the recommended workflow for creating a mod from one or more maps.

## 1. Select the game

At the top of the application, select either:

- **Anno 117**
- **Anno 1800**

The selection controls which map database, regions, packages, settings, and export format are used.

## 2. Configure Settings first

Open **Settings** and configure at least:

1. **Creator**
2. **GUID Start** and **GUID End** for the selected game
3. **Default Export Path**, if desired

If your maps use a region that is not included by default, add it under **Custom Region** with the correct game region ID.

Click **Save**.

> The Creator is required for mod export. A valid GUID range is required before importing maps.

## 3. Create a Map Package

Open **Map Packages** and click **New**.

Enter an internal package name, for example:

```text
My Celtic Islands
```

Then configure:

- **Mod Name**, for example `Celtic Island Collection`
- **Version**, for example `1.0.0`
- **Region**
- Optional package-specific GUID range

Click **Save Package Settings**.

## 4. Import maps

Open **General**.

Use either:

- **Add Map ( File )** for one `.a7m` file
- **Add Map ( Folder )** to recursively find all `.a7m` files below a selected folder

New maps receive the next free GUID from the configured game GUID range.

## 5. Configure the maps

Select one or more maps in the General table and right-click.

Use the context menu to:

- set the **Region**;
- change the **GUID**;
- change the **Type** between `Normal` and `Decoration`;
- add the maps to a **Map Package**;
- delete maps from the application database.

When adding maps to a package, the application can optionally apply the package Region and package-specific GUID range.

## 6. Review the Map Package

Open **Map Packages** and select the package.

The table shows all maps assigned to it. Verify that each map has the intended:

- Region
- GUID
- Type
- source file

Use the right-click menu if something needs to be changed.

## 7. Add optional additional mod files

If the mod requires files in addition to the map folders, click **Additional Files**.

Click **Add Files** and select a folder. The selected folder itself acts only as the source root. Its **contents** are copied directly into the generated mod root.

For example, selecting:

```text
C:\map_files\xxx\yyy\material\
```

with:

```text
material\
├── graphics\
├── textures\
└── configuration.xml
```

results in:

```text
[MapPackage] Celtic Island Collection\
├── graphics\
├── textures\
└── configuration.xml
```

The `material` folder itself is **not** created in the mod.

The Additional Files table shows the source root, source folder, and an export example. Right-click an entry and choose **Delete** to remove it from the package. Click **Save** to store the list for the currently selected Map Package.

## 8. Export the mod

Open **Export Maps as Mod**.

1. Select the **Map Package**.
2. Verify or select the **Export Folder**.
3. Click **Export Map Package as Mod**.

The result is created as:

```text
<Export Folder>\[MapPackage] <Mod Name>\
```

The export log displays the files being copied and the generated metadata. If the target mod folder already exists, the application asks before replacing it.

---

# User Interface Reference

## Global Header

### Game

Switches the complete working context between **Anno 117** and **Anno 1800**.

Changing the game updates the General map database, Map Packages, export package list, and game-specific export path.

### GitHub

Opens the project's configured GitHub profile in the default web browser.

### Ko-fi

Opens the configured Ko-fi page in the default web browser.

---

# General Tab

The **General** tab is the main map database for the currently selected game.

## Add Map ( Folder )

Opens a folder picker and recursively scans the selected directory for `.a7m` files.

Each discovered map is imported separately.

## Add Map ( File )

Imports one `.a7m` map file.

If the same source path already exists in the database, the application asks whether the existing entry should be updated or kept unchanged.

## Filter

Filters the table by Map Package.

- **All** shows every imported map for the selected game.
- Selecting a Map Package shows only maps assigned to that package.

## Table columns

### Map Name

The filename of the imported `.a7m` map without the extension.

### Region

The display region assigned to the map. During export it is translated to the corresponding game-specific region ID.

### Map Package

The package currently containing the map. An empty value means that the map has not yet been assigned to a package.

### GUID

The unique numerical GUID used for the exported RandomIsland asset.

When a new map is imported, the application selects the next free GUID from the configured GUID range.

### Type

Supported values:

- `Normal`
- `Decoration`

The selected type changes the generated island asset configuration.

### Map File

Absolute path to the imported `.a7m` source file.

## General table context menu

Right-click one or more maps.

### Set Region

Assigns a built-in or custom region to the selected map or maps.

### Change GUID

Changes the GUID of exactly one selected map. Duplicate GUIDs are rejected.

### Change Type

Sets the selected maps to `Normal` or `Decoration`.

### Add to Map Package...

Assigns the selected maps to a Map Package.

If the package has its own GUID range configured, the application asks whether new GUIDs should be assigned from that range.

If the package defines a Region, the application also asks whether that Region should be applied to the selected maps.

### Delete

Deletes the selected entries from the application's map database. This does not delete the original source files from disk.

---

# Map Packages Tab

A **Map Package** describes a group of maps that will be exported together as one mod.

## Map Package

Selects the package to edit.

### New

Creates a new Map Package. Each package receives an internal two-character package ID used in generated map paths.

### Rename

Renames the selected package and updates existing map assignments.

### Delete

Deletes the package definition and clears its assignments from maps. The maps themselves remain in the General database.

## Mod Name

The visible name used for the exported mod.

The export folder is named:

```text
[MapPackage] <Mod Name>
```

The Mod Name also becomes part of the generated `modinfo.json` metadata.

## Additional Files

Opens the **Additional Files** window for the selected package.

A small information text below the button shows how many additional source folders are currently stored in the package.

### Add Files

Chooses a source folder whose **contents** should be copied directly into the root of the generated mod.

### Additional Files table

- **Root Folder**: name of the selected source root.
- **Source Folder**: complete source path.
- **Export Example**: example showing where the first discovered item will appear below `[MapPackage] <Mod Name>`.

### Right-click → Delete

Removes selected entries from the pending Additional Files list.

### Save

Stores the Additional Files list in the currently selected Map Package.

## Version

Version written into `modinfo.json`.

A version must be configured before export.

## Region

Default Region associated with the Map Package.

When maps are added to the package from the General tab, the application can optionally apply this Region to them.

## Save Package Settings

Stores Mod Name, Version, Region, and optional GUID-range configuration for the package.

## Use different GUID ranges

Enables a separate GUID range for this Map Package.

This is useful for reserving a dedicated GUID block for a particular collection of maps.

### GUID Start / GUID End

Defines the inclusive package-specific range.

When maps are assigned to this package, the application can optionally allocate new free GUIDs from this range.

## Map Package table

Shows the maps currently assigned to the selected package:

- Map Name
- Region
- Map Package
- GUID
- Type
- Map File

## Map Package table context menu

### Set Region

Changes the Region of the selected package maps.

### Change GUID

Changes the GUID of exactly one selected map.

### Change Type

Sets selected maps to `Normal` or `Decoration`.

### Remove from Package

Removes the selected maps from this Map Package without deleting them from the General database.

---

# Export Maps as Mod Tab

This tab turns a configured Map Package into a mod folder.

## Map Package

Selects the package to export.

Only packages belonging to the currently selected game are listed.

## Export Folder

Parent folder in which the generated mod folder will be created.

The initial value is taken from the selected game's **Default Export Path** in Settings.

### Browse...

Selects another export parent folder for the current operation.

## Export Map Package as Mod

Starts the export.

Before export, the application validates that:

- a Map Package is selected;
- the package still exists;
- Mod Name is configured and valid as a Windows folder name;
- the Export Folder exists;
- the package contains maps;
- the package has an internal ID;
- Version is configured;
- Creator is configured;
- all map files and required Region mappings are available.

If the target mod already exists, the application asks before replacing it.

The file operation runs in a background worker so the interface remains responsive.

## Export Log

Shows live export progress, including copied map files, generated files, Additional Files, success messages, and errors. The log automatically scrolls to the newest message.

---

# Settings Tab

Settings are split into **General**, **Anno 117**, and **Anno 1800**.

The **Save** button at the bottom stores the application settings.

## Settings → General

### Creator

Creator name placed in `modinfo.json`.

This field is required for exporting a mod.

### Creator Contact

Contact or URL placed in the `CreatorContact` field of `modinfo.json`.

---

# Settings → Anno 117

## GUID Start / GUID End

Default inclusive GUID allocation range used when importing Anno 117 maps.

Both values are required and must contain digits only. `GUID Start` must not be greater than `GUID End`.

## Default Export Path

Default parent directory shown in **Export Maps as Mod** when Anno 117 is selected.

## Custom Region

Adds extra display-name-to-game-ID mappings for regions not included in the application's built-in region list.

### Region

Display name shown in the application's Region selectors.

### ID

Actual game region identifier written to the exported `assets.xml`.

### Built-in Anno 117 regions

| Display Region | Exported ID |
|---|---|
| Albion | `Celtic` |
| Latium | `Roman` |

### Custom Region table context menu

- **Change Region**: renames the selected custom display region.
- **Change ID**: changes its underlying game region ID.
- **Delete**: removes the custom region.

---

# Settings → Anno 1800

The controls work the same way as the Anno 117 settings but are stored independently.

## Built-in Anno 1800 regions

| Display Region | Exported ID |
|---|---|
| Arctic | `Arctic` |
| Enbesa | `Africa` |
| The New World | `Colony01` |
| The Old World | `Moderate` |

Custom regions can be added for additional or mod-specific region identifiers.

---

# Export Structure

## Map files

Map folders are copied to:

```text
[MapPackage] <Mod Name>\
└── data\
    └── <Package ID>\
        └── islands\
            └── <Original Map Folder>\
                └── ...
```

The complete source directory containing each `.a7m` is copied, not only the `.a7m` itself. This preserves supporting files stored beside the map.

## Anno 117 assets.xml

Generated at:

```text
[MapPackage] <Mod Name>\data\base\config\export\assets.xml
```

For normal Anno 117 maps, placeholder size is inferred from the map name where possible. Names containing `medium`, `large`, `extralarge`, `extra_large`, or `continental` influence the generated placeholder configuration.

## Anno 1800 assets.xml

Generated at:

```text
[MapPackage] <Mod Name>\data\config\export\main\asset\assets.xml
```

## modinfo.json

Generated in the root of the mod:

```text
[MapPackage] <Mod Name>\modinfo.json
```

It contains the configured Version, Creator, Creator Contact, generated ModID, Map category, and localized Mod Name/Description entries.

---

# Important Notes

## Source files remain external

Imported maps are referenced by absolute source path. Keep the original map folders available until the mod has been exported.

## Moving source folders

If an imported `.a7m` or an Additional Files source folder is moved or deleted, export can fail because the stored path is no longer valid.

## Duplicate map folder names

Two maps in the same exported package cannot come from different source directories with the same folder name. The generated structure uses the source folder name under `data/<Package ID>/islands/`, so such a collision is rejected.

## Region IDs matter

The display Region and game Region ID are not necessarily identical. For example, Anno 117 `Albion` exports as `Celtic`, while `Latium` exports as `Roman`.

If a selected Region has no usable mapping, export stops instead of producing an invalid `assets.xml`.

## Existing export folders

A new export replaces an existing `[MapPackage] <Mod Name>` folder after confirmation. Do not store unrelated files in that generated folder unless they are represented through Additional Files or otherwise backed up.

---

# Running from Source

## Requirements

- Python 3.12 is the version used by the project's GitHub build workflow.
- Install dependencies from `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

Start the application with:

```bash
python AnnoMapPackageCreator.py
```

---

# Tests

Run the test suite with:

```bash
pytest
```

---

# Building the One-File Application

The project uses PyInstaller through the provided build script.

```bash
python 00_build_onefile.py
```

The script reads `version.txt`, validates its required bundled resources, cleans previous `build` and `dist` directories, and creates a versioned windowed executable in `dist`.

---

# Packing the Source Project

Create the project source archive with:

```bash
python 00_pack_project.py
```

---

# Release Workflow

The repository includes:

```text
.github/workflows/release.yml
```

The workflow can be started manually or by pushing a tag matching:

```text
v*
```

It installs Python 3.12, installs `requirements.txt`, runs `pytest`, executes `00_build_onefile.py`, uploads the Windows build artifact, and publishes the built files to a GitHub Release for version tags.

---

# Project Structure

```text
Anno Map Package Creator/
├── .github/workflows/release.yml
├── app/
│   ├── backend/       # JSON persistence
│   ├── config/        # Application, paths, and built-in regions
│   ├── functions/     # Database, settings, links, update logic
│   ├── models/        # Map and export data contracts
│   ├── services/      # Shared and game-specific export logic
│   ├── templates/     # Shared dialogs and sortable tables
│   └── ui/            # Main window, tabs, and Additional Files UI
├── tests/
├── AnnoMapPackageCreator.py
├── 00_build_onefile.py
├── 00_pack_project.py
├── config.json
├── config_anno_117.json
├── config_anno_1800.json
├── requirements.txt
├── version.txt
├── CHANGELOG.md
└── README.md
```

---

# Application Data

The application stores its persistent working data next to the application/project root:

- `config.json`: global settings and per-game GUID/export-path settings
- `config_anno_117.json`: Anno 117 maps, Map Packages, and custom regions
- `config_anno_1800.json`: Anno 1800 maps, Map Packages, and custom regions
- `version.txt`: authoritative application version

When running as a packaged executable, these files are resolved relative to the executable directory.

---

# Troubleshooting

### "GUID Start and GUID End must be configured before importing maps"

Open **Settings**, configure the GUID range for the selected game, and click **Save**.

### "No free GUID remains in range ..."

Increase or change the configured GUID range, or manually reorganize existing GUID assignments.

### "Set Mod Name in the Map Packages tab first"

Select the Map Package, enter a Mod Name, and click **Save Package Settings**.

### "Set Version in the Map Packages tab before exporting"

Enter a Version for the selected package and save the package settings.

### "Set Creator in Settings > General before exporting"

Enter the Creator under **Settings → General** and save the settings.

### "No Region ID mapping found"

Check the map's Region. If it is not a built-in region, create a matching **Custom Region** with the correct game ID under Settings.

### "Map file not found"

The imported `.a7m` has been moved, renamed, or deleted. Restore it to the stored path or re-import the map from its new location.

### "Additional Files folder does not exist"

A folder saved under **Additional Files** was moved or deleted. Open the Additional Files dialog, remove the invalid entry, and add its new location if necessary.

### Existing mod will be replaced

This is expected when exporting to a folder containing a mod with the same Mod Name. Confirm replacement only when you want the application to regenerate that mod.

---

# Known Limitations

- Only `.a7m` map files are imported as maps.
- Map and Additional Files entries depend on their stored filesystem paths remaining available.
- Map Packages are game-specific and are not shared between Anno 117 and Anno 1800.
- Package IDs are automatically managed internally and are limited to two lowercase base-36 characters.
- The current release workflow builds a Windows artifact.

---

# License

No license file or explicit software license is currently defined in the project. Do not assume redistribution or modification rights beyond those granted by the project owner until a license is added.

---

## Recommended Map Package Checklist

Before exporting, verify:

- [ ] Correct game selected
- [ ] Creator configured
- [ ] Valid GUID range configured
- [ ] Map Package created
- [ ] Mod Name configured
- [ ] Version configured
- [ ] Correct package Region selected
- [ ] All maps assigned to the package
- [ ] Each map has the correct Region
- [ ] Each map has a unique GUID
- [ ] Each map has the correct `Normal` / `Decoration` Type
- [ ] Optional Additional Files configured and saved
- [ ] Export Folder exists
- [ ] Source map folders still exist
- [ ] Export completed without errors in the Export Log

---

# Deutsche Dokumentation

Der **Anno Map Package Creator** ist ein Desktop-Tool, mit dem benutzerdefinierte `.a7m`-Inselkarten in wiederverwendbaren **Map Packages** organisiert und als einsatzbereite Mods für **Anno 117** und **Anno 1800** exportiert werden können.

Die Anwendung führt durch den vollständigen Ablauf: Karten importieren, Regionen und GUIDs zuweisen, Karten zu Paketen zusammenfassen, zusätzliche Mod-Dateien ergänzen und anschließend die passende Mod-Struktur sowie die erforderliche `assets.xml` erzeugen.

## Funktionsumfang

- Unterstützung für **Anno 117** und **Anno 1800** in einer Anwendung
- Import einzelner `.a7m`-Dateien oder rekursive Ordnersuche
- Verwaltung von GUIDs, Regionen, Kartentypen und Map Packages
- Kartentypen `Normal` und `Decoration`
- Map Packages mit Mod Name, Version, Region und optionalem eigenen GUID-Bereich
- Benutzerdefinierte Regionen und Region-IDs
- **Additional Files**, die direkt in das Stammverzeichnis der exportierten Mod kopiert werden
- Automatische Erzeugung der passenden `assets.xml` und `modinfo.json`
- Export vollständiger Kartenordner inklusive Unterordnern und Begleitdateien
- Export in einem Hintergrund-Worker mit automatisch scrollendem Live-Log
- Separate Standard-Exportpfade für Anno 117 und Anno 1800
- Dark-Mode-Oberfläche mit sortierbaren Tabellen

---

# Schnellablauf: Ein Map Package erstellen

## 1. Spiel auswählen

Wähle oben in der Anwendung **Anno 117** oder **Anno 1800** aus.

Die Auswahl bestimmt, welche Kartendatenbank, Regionen, Map Packages, Einstellungen und Exportformate verwendet werden.

## 2. Einstellungen konfigurieren

Öffne **Settings** und trage mindestens Folgendes ein:

1. **Creator**
2. **GUID Start** und **GUID End** für das ausgewählte Spiel
3. Optional den **Default Export Path**

Wenn eine Karte eine Region verwendet, die nicht standardmäßig vorhanden ist, füge sie im Bereich **Custom Region** mit der korrekten Spiel-Region-ID hinzu.

Klicke anschließend auf **Save**.

> Der Creator ist für den Mod-Export erforderlich. Ein gültiger GUID-Bereich muss vor dem Import von Karten eingerichtet sein.

## 3. Map Package anlegen

Öffne **Map Packages** und klicke auf **New**.

Gib einen internen Paketnamen ein, zum Beispiel:

```text
My Celtic Islands
```

Konfiguriere danach:

- **Mod Name**, zum Beispiel `Celtic Island Collection`
- **Version**, zum Beispiel `1.0.0`
- **Region**
- optional einen eigenen GUID-Bereich für dieses Paket

Klicke auf **Save Package Settings**.

## 4. Karten importieren

Öffne **General** und verwende:

- **Add Map ( File )** für eine einzelne `.a7m`-Datei
- **Add Map ( Folder )** für eine rekursive Suche nach `.a7m`-Dateien in einem Ordner

Neue Karten erhalten automatisch die nächste freie GUID aus dem konfigurierten GUID-Bereich.

## 5. Karten konfigurieren

Markiere eine oder mehrere Karten in der General-Tabelle und öffne mit der rechten Maustaste das Kontextmenü.

Dort kannst du:

- die **Region** setzen,
- die **GUID** ändern,
- den **Type** zwischen `Normal` und `Decoration` ändern,
- Karten zu einem **Map Package** hinzufügen,
- Karten aus der Anwendungsdatenbank löschen.

Beim Hinzufügen zu einem Map Package kann die Anwendung optional die Paket-Region und den paketbezogenen GUID-Bereich übernehmen.

## 6. Map Package prüfen

Öffne **Map Packages** und wähle das Paket aus.

Prüfe in der Tabelle für jede Karte:

- Region
- GUID
- Type
- Quelldatei

Erforderliche Änderungen können über das Rechtsklickmenü vorgenommen werden.

## 7. Optionale zusätzliche Mod-Dateien hinzufügen

Wenn die Mod weitere Dateien benötigt, klicke auf **Additional Files**.

Klicke auf **Add Files** und wähle einen Ordner aus. Der ausgewählte Ordner ist nur das Quell-Stammverzeichnis. Sein **Inhalt** wird direkt in das Stammverzeichnis der erzeugten Mod kopiert.

Beispiel für den ausgewählten Ordner:

```text
C:\map_files\xxx\yyy\material\
```

Inhalt:

```text
material\
├── graphics\
├── textures\
└── configuration.xml
```

Exportiertes Ergebnis:

```text
[MapPackage] Celtic Island Collection\
├── graphics\
├── textures\
└── configuration.xml
```

Der Ordner `material` selbst wird nicht in der Mod angelegt.

Die Tabelle zeigt Quell-Root, vollständigen Quellpfad und ein Exportbeispiel. Über **Rechtsklick → Delete** kann ein Eintrag entfernt werden. Mit **Save** wird die Liste für das aktuell ausgewählte Map Package gespeichert.

## 8. Mod exportieren

Öffne **Export Maps as Mod**.

1. Wähle das **Map Package**.
2. Prüfe oder ändere den **Export Folder**.
3. Klicke auf **Export Map Package as Mod**.

Das Ergebnis wird hier erstellt:

```text
<Export Folder>\[MapPackage] <Mod Name>\
```

Das Export-Log zeigt kopierte Dateien und erzeugte Metadaten. Existiert der Zielordner bereits, fragt die Anwendung vor dem Ersetzen nach.

---

# Beschreibung der Oberfläche

## Globale Kopfzeile

### Game

Wechselt den vollständigen Arbeitskontext zwischen **Anno 117** und **Anno 1800**. Dadurch ändern sich Kartendatenbank, Map Packages, Exportpakete und Standard-Exportpfad.

### GitHub

Öffnet das konfigurierte GitHub-Profil im Standardbrowser.

### Ko-fi

Öffnet die konfigurierte Ko-fi-Seite im Standardbrowser.

---

# Tab General

Der Tab **General** enthält die zentrale Kartendatenbank des ausgewählten Spiels.

## Add Map ( Folder )

Öffnet eine Ordnerauswahl und durchsucht den gewählten Ordner rekursiv nach `.a7m`-Dateien. Jede gefundene Karte wird einzeln importiert.

## Add Map ( File )

Importiert eine einzelne `.a7m`-Karte. Ist derselbe Quellpfad bereits vorhanden, kann der bestehende Eintrag aktualisiert oder unverändert beibehalten werden.

## Filter

Filtert die Tabelle nach Map Package.

- **All** zeigt alle importierten Karten des ausgewählten Spiels.
- Ein ausgewähltes Map Package zeigt nur die darin enthaltenen Karten.

## Tabellenspalten

- **Map Name:** Dateiname der `.a7m` ohne Erweiterung
- **Region:** Anzeigename der zugewiesenen Region; wird beim Export in die Spiel-Region-ID übersetzt
- **Map Package:** aktuell zugewiesenes Paket; leer bedeutet nicht zugewiesen
- **GUID:** eindeutige numerische GUID des exportierten RandomIsland-Assets
- **Type:** `Normal` oder `Decoration`
- **Map File:** absoluter Pfad zur importierten `.a7m`

## Rechtsklickmenü

### Set Region

Weist den ausgewählten Karten eine eingebaute oder benutzerdefinierte Region zu.

### Change GUID

Ändert die GUID einer einzelnen ausgewählten Karte. Doppelte GUIDs werden abgelehnt.

### Change Type

Ändert den Typ der ausgewählten Karten auf `Normal` oder `Decoration`.

### Add to Map Package...

Ordnet die ausgewählten Karten einem Map Package zu. Falls das Paket eine eigene Region oder einen eigenen GUID-Bereich besitzt, fragt die Anwendung, ob diese Werte übernommen werden sollen.

### Delete

Entfernt die ausgewählten Einträge aus der Anwendungsdatenbank. Die Originaldateien auf dem Datenträger werden nicht gelöscht.

---

# Tab Map Packages

Ein **Map Package** beschreibt eine Gruppe von Karten, die gemeinsam als eine Mod exportiert wird.

## Map Package

Wählt das zu bearbeitende Paket aus.

- **New:** erstellt ein neues Map Package und vergibt intern eine zweistellige Package-ID
- **Rename:** benennt das Paket um und aktualisiert vorhandene Kartenzuweisungen
- **Delete:** löscht die Paketdefinition und entfernt die Zuweisungen, lässt die Karten aber in der General-Datenbank

## Mod Name

Sichtbarer Name der exportierten Mod. Der Exportordner wird folgendermaßen benannt:

```text
[MapPackage] <Mod Name>
```

Der Mod Name wird außerdem in die `modinfo.json` übernommen.

## Additional Files

Öffnet das Fenster für zusätzliche Dateien des ausgewählten Map Packages. Unter dem Button wird angezeigt, wie viele zusätzliche Quellordner gespeichert sind.

### Add Files

Wählt einen Quellordner. Nur dessen Inhalt wird direkt in das Mod-Stammverzeichnis kopiert.

### Tabelle

- **Root Folder:** Name des ausgewählten Quell-Stammordners
- **Source Folder:** vollständiger Quellpfad
- **Export Example:** Beispielpfad des ersten gefundenen Elements unter `[MapPackage] <Mod Name>`

### Rechtsklick → Delete

Entfernt die markierten Einträge aus der noch nicht gespeicherten Liste.

### Save

Speichert die Additional-Files-Liste im aktuell ausgewählten Map Package.

## Version

Version, die in die `modinfo.json` geschrieben wird. Vor dem Export muss eine Version eingetragen sein.

## Region

Standardregion des Map Packages. Beim Hinzufügen von Karten kann diese Region optional auf die Karten übertragen werden.

## Save Package Settings

Speichert Mod Name, Version, Region und die optionale GUID-Bereichskonfiguration.

## Use different GUID ranges

Aktiviert einen separaten GUID-Bereich für dieses Map Package.

### GUID Start / GUID End

Definiert den inklusiven paketbezogenen GUID-Bereich. Beim Zuweisen von Karten können daraus neue freie GUIDs vergeben werden.

## Paket-Tabelle

Zeigt alle Karten des ausgewählten Pakets mit Map Name, Region, Map Package, GUID, Type und Map File.

## Rechtsklickmenü

- **Set Region:** ändert die Region ausgewählter Karten
- **Change GUID:** ändert die GUID einer einzelnen Karte
- **Change Type:** setzt den Typ auf `Normal` oder `Decoration`
- **Remove from Package:** entfernt Karten aus dem Paket, löscht sie aber nicht aus General

---

# Tab Export Maps as Mod

Dieser Tab exportiert ein konfiguriertes Map Package als Mod-Ordner.

## Map Package

Wählt das zu exportierende Paket des aktuellen Spiels aus.

## Export Folder

Übergeordneter Ordner, in dem die Mod angelegt wird. Der Anfangswert stammt aus dem spielbezogenen **Default Export Path**.

### Browse...

Wählt einen anderen Exportordner für den aktuellen Vorgang.

## Export Map Package as Mod

Startet den Export. Vorher prüft die Anwendung unter anderem:

- Map Package ausgewählt und vorhanden
- gültiger Mod Name
- Export Folder vorhanden
- Paket enthält Karten
- interne Package-ID vorhanden
- Version und Creator gesetzt
- Karten- und Additional-Files-Quellen vorhanden
- gültige Region-Zuordnungen vorhanden

Ein bestehender Zielordner wird nur nach Bestätigung ersetzt. Der Export läuft in einem Hintergrund-Worker.

## Export Log

Zeigt kopierte Kartendateien, erzeugte Dateien, Additional Files, Meldungen und Fehler. Das Log scrollt automatisch zum neuesten Eintrag.

---

# Tab Settings

Die Einstellungen sind in **General**, **Anno 117** und **Anno 1800** aufgeteilt. Mit dem unten sichtbaren **Save**-Button werden die Einstellungen gespeichert.

## Settings → General

### Creator

Erstellername für `modinfo.json`. Dieses Feld ist für den Export erforderlich.

### Creator Contact

Kontakt oder URL für das Feld `CreatorContact` in `modinfo.json`.

## Settings → Anno 117

### GUID Start / GUID End

Standardbereich für die automatische GUID-Vergabe beim Import von Anno-117-Karten. Beide Werte müssen aus Ziffern bestehen und Start darf nicht größer als Ende sein.

### Default Export Path

Standard-Zielordner für den Anno-117-Export.

### Custom Region

Erstellt zusätzliche Zuordnungen zwischen einem Anzeigenamen und einer Spiel-Region-ID.

- **Region:** Name in den Auswahlfeldern der Anwendung
- **ID:** tatsächlicher Wert in der exportierten `assets.xml`

### Eingebaute Anno-117-Regionen

| Anzeigeregion | Exportierte ID |
|---|---|
| Albion | `Celtic` |
| Latium | `Roman` |

### Rechtsklickmenü der Custom-Region-Tabelle

- **Change Region:** ändert den Anzeigenamen
- **Change ID:** ändert die Spiel-Region-ID
- **Delete:** löscht die benutzerdefinierte Region

## Settings → Anno 1800

Die Bedienung entspricht Anno 117, die Werte werden jedoch separat gespeichert.

### Eingebaute Anno-1800-Regionen

| Anzeigeregion | Exportierte ID |
|---|---|
| Arctic | `Arctic` |
| Enbesa | `Africa` |
| The New World | `Colony01` |
| The Old World | `Moderate` |

---

# Exportstruktur

## Kartendateien

```text
[MapPackage] <Mod Name>\
└── data\
    └── <Package ID>\
        └── islands\
            └── <Original Map Folder>\
                └── ...
```

Der vollständige Quellordner der `.a7m` wird kopiert. Dadurch bleiben zugehörige Dateien und Unterordner erhalten.

## Anno 117 assets.xml

```text
[MapPackage] <Mod Name>\data\base\config\export\assets.xml
```

Für normale Karten wird die Platzhaltergröße soweit möglich aus dem Kartennamen erkannt. Begriffe wie `medium`, `large`, `extralarge`, `extra_large` oder `continental` beeinflussen die erzeugte Konfiguration.

## Anno 1800 assets.xml

```text
[MapPackage] <Mod Name>\data\config\export\main\asset\assets.xml
```

## modinfo.json

```text
[MapPackage] <Mod Name>\modinfo.json
```

Enthält Version, Creator, Creator Contact, erzeugte ModID, Kategorie sowie lokalisierte Mod-Namen und Beschreibungen.

---

# Wichtige Hinweise

## Quelldateien bleiben extern

Importierte Karten werden über absolute Pfade referenziert. Die ursprünglichen Kartenordner müssen bis zum Export verfügbar bleiben.

## Verschobene Quellen

Wird eine `.a7m` oder ein Additional-Files-Ordner verschoben oder gelöscht, kann der Export wegen des ungültigen gespeicherten Pfads fehlschlagen.

## Doppelte Kartenordnernamen

Zwei unterschiedliche Quellordner mit demselben Ordnernamen können nicht gemeinsam in einem Paket exportiert werden, da beide denselben Zielpfad unter `data/<Package ID>/islands/` erhielten.

## Region-IDs

Anzeigename und Spiel-ID können unterschiedlich sein. Beispielsweise wird Anno 117 `Albion` als `Celtic` und `Latium` als `Roman` exportiert.

## Bestehende Exportordner

Ein vorhandener Ordner `[MapPackage] <Mod Name>` wird nach Bestätigung vollständig ersetzt. Speichere dort keine unabhängigen Dateien, die nicht über Additional Files oder anderweitig gesichert sind.

---

# Aus dem Quellcode starten

## Voraussetzungen

Das GitHub-Build verwendet Python 3.12. Abhängigkeiten installieren:

```bash
python -m pip install -r requirements.txt
```

Anwendung starten:

```bash
python AnnoMapPackageCreator.py
```

# Tests

```bash
pytest
```

# Onefile-Build

```bash
python 00_build_onefile.py
```

Das Skript liest `version.txt`, prüft die benötigten Ressourcen, bereinigt alte Build-Ausgaben und erstellt eine versionierte Fensteranwendung in `dist`.

# Quellprojekt packen

```bash
python 00_pack_project.py
```

# Release-Workflow

`.github/workflows/release.yml` kann manuell oder durch einen Git-Tag nach dem Muster `v*` gestartet werden. Der Workflow verwendet Python 3.12, installiert die Abhängigkeiten, führt `pytest` und `00_build_onefile.py` aus und veröffentlicht das Windows-Artefakt bei Versionstags.

---

# Projektstruktur

```text
Anno Map Package Creator/
├── .github/workflows/release.yml
├── app/
│   ├── backend/       # JSON-Persistenz
│   ├── config/        # Anwendung, Pfade und eingebaute Regionen
│   ├── functions/     # Datenbank-, Einstellungs-, Link- und Updatefunktionen
│   ├── models/        # Karten- und Exportdatenmodelle
│   ├── services/      # gemeinsame und spielspezifische Exportlogik
│   ├── templates/     # gemeinsame Dialoge und Tabellen
│   └── ui/            # Hauptfenster, Tabs und Additional-Files-Fenster
├── tests/
├── AnnoMapPackageCreator.py
├── 00_build_onefile.py
├── 00_pack_project.py
├── config.json
├── config_anno_117.json
├── config_anno_1800.json
├── requirements.txt
├── version.txt
├── CHANGELOG.md
└── README.md
```

# Anwendungsdaten

- `config.json`: globale Einstellungen sowie GUID- und Exportpfade
- `config_anno_117.json`: Anno-117-Karten, Map Packages und Custom Regions
- `config_anno_1800.json`: Anno-1800-Karten, Map Packages und Custom Regions
- `version.txt`: maßgebliche Anwendungsversion

In der gepackten Anwendung werden diese Dateien relativ zum Verzeichnis der ausführbaren Datei aufgelöst.

---

# Fehlerbehebung

### „GUID Start and GUID End must be configured before importing maps“

Unter **Settings** den GUID-Bereich für das ausgewählte Spiel eintragen und **Save** klicken.

### „No free GUID remains in range ...“

Den GUID-Bereich vergrößern oder vorhandene GUID-Zuweisungen neu organisieren.

### „Set Mod Name in the Map Packages tab first“

Im Tab Map Packages einen Mod Name eintragen und **Save Package Settings** klicken.

### „Set Version in the Map Packages tab before exporting“

Eine Version eintragen und die Paketdaten speichern.

### „Set Creator in Settings > General before exporting“

Unter **Settings → General** den Creator eintragen und speichern.

### „No Region ID mapping found“

Die Kartenregion prüfen. Für nicht eingebaute Regionen eine Custom Region mit korrekter Spiel-ID anlegen.

### „Map file not found“

Die `.a7m` wurde verschoben, umbenannt oder gelöscht. Datei wiederherstellen oder vom neuen Pfad erneut importieren.

### „Additional Files folder does not exist“

Der gespeicherte zusätzliche Quellordner wurde verschoben oder gelöscht. Den ungültigen Eintrag entfernen und bei Bedarf den neuen Pfad hinzufügen.

---

# Bekannte Einschränkungen

- Es können nur `.a7m`-Dateien als Karten importiert werden.
- Karten und Additional Files sind von den gespeicherten Dateisystempfaden abhängig.
- Map Packages sind spielspezifisch und werden nicht zwischen Anno 117 und Anno 1800 geteilt.
- Interne Package-IDs bestehen aus zwei kleingeschriebenen Base-36-Zeichen.
- Der aktuelle Release-Workflow erzeugt ein Windows-Artefakt.

# Lizenz

Im Projekt ist derzeit keine Lizenzdatei oder ausdrückliche Softwarelizenz definiert. Ohne ergänzte Lizenz sollten keine weitergehenden Rechte zur Verteilung oder Änderung angenommen werden.

---

## Empfohlene Prüfliste vor dem Export

- [ ] Richtiges Spiel ausgewählt
- [ ] Creator eingetragen
- [ ] Gültiger GUID-Bereich konfiguriert
- [ ] Map Package erstellt
- [ ] Mod Name eingetragen
- [ ] Version eingetragen
- [ ] Richtige Paket-Region ausgewählt
- [ ] Alle Karten dem Paket zugewiesen
- [ ] Jede Karte besitzt die richtige Region
- [ ] Jede Karte besitzt eine eindeutige GUID
- [ ] Jede Karte besitzt den richtigen Typ `Normal` oder `Decoration`
- [ ] Optionale Additional Files konfiguriert und gespeichert
- [ ] Export Folder existiert
- [ ] Quellordner der Karten sind noch vorhanden
- [ ] Export-Log enthält keine Fehler

