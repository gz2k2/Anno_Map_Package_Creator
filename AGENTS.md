# AGENTS.md

## Purpose

This file defines the mandatory engineering rules for creating a new application in this repository. Every contributor and coding agent must follow these rules when creating, changing, testing, building, packaging, or releasing the application.

The primary goals are:

- a clean and maintainable architecture;
- strict separation of responsibilities;
- small, focused files and functions;
- fully documented and commented source code in English;
- reproducible local builds;
- a portable project package;
- an automated GitHub release workflow that matches the application.

These rules apply to the complete project. More specific `AGENTS.md` files in subdirectories may add stricter local rules, but they must not weaken this document.

---

## 1. Mandatory Working Method

Before writing code:

1. Inspect the existing project structure and naming conventions.
2. Identify the feature's responsibilities, inputs, outputs, dependencies, UI impact, persistence impact, and packaging requirements.
3. Decide which existing module owns the behavior.
4. Create a new module only when the behavior represents a distinct responsibility.
5. Check whether the change requires updates to tests, bundled resources, `requirements.txt`, `00_build_onefile.py`, `00_pack_project.py`, or `.github/workflows/release.yml`.

Never place new code in a convenient file merely because that file already exists. Place it in the file whose responsibility matches the feature.

When modifying an existing project, preserve working behavior and established data formats unless the task explicitly requires a migration. Do not silently normalize, discard, reorder, or rewrite user data.

---

## 2. Required Project Structure

Use the following structure as the default for a Python desktop application. Adapt individual directories only when the selected framework or application type genuinely requires it.

```text
project-root/
├── .github/
│   └── workflows/
│       └── release.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── backend/
│   │   ├── __init__.py
│   │   └── backend_<responsibility>.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_<topic>.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database_<topic>.py
│   ├── functions/
│   │   ├── __init__.py
│   │   └── function_<feature>.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── model_<domain>.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── service_<integration>.py
│   ├── templates/
│   │   ├── __init__.py
│   │   └── template_<component>.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── ui.py
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   └── ui_dialog_<name>.py
│   │   └── tabs/
│   │       ├── __init__.py
│   │       └── ui_tab_<name>.py
│   └── utils/
│       ├── __init__.py
│       └── util_<topic>.py
├── assets/
│   ├── icons/
│   ├── images/
│   └── themes/
├── data/
│   └── <bundled-read-only-data>/
├── tests/
│   ├── __init__.py
│   ├── test_<feature>.py
│   └── fixtures/
├── <application_launcher>.py
├── 00_build_onefile.py
├── 00_pack_project.py
├── requirements.txt
├── version.txt
├── README.md
├── CHANGELOG.md
├── .gitignore
└── AGENTS.md
```

Do not create every optional directory in advance. Create `models/`, `services/`, `dialogs/`, or `utils/` when the application actually needs that responsibility.

### Directory responsibilities

- `app/main.py`: application composition and startup coordination. It may connect major components but must not contain feature implementation.
- `app/backend/`: low-level file formats, parsers, persistence engines, adapters, and infrastructure-specific data access.
- `app/config/`: constants, defaults, option definitions, platform settings, and configuration schemas. Do not place feature algorithms here.
- `app/database/`: static mappings, catalogs, lookup data, and application-owned reference datasets.
- `app/functions/`: focused domain or feature operations that do not belong to the UI or a low-level backend.
- `app/models/`: dataclasses, typed domain models, state objects, and validation models.
- `app/services/`: coordination of external programs, APIs, subprocesses, or multi-step application workflows.
- `app/templates/`: reusable UI components and shared presentation patterns.
- `app/ui/`: windows, tabs, dialogs, widget layout, event binding, and presentation state.
- `app/utils/`: small generic helpers with no feature-specific ownership. This directory must not become a dumping ground.
- `assets/`: icons, images, themes, fonts, and other presentation assets.
- `data/`: read-only runtime resources shipped with the application.
- `tests/`: automated tests mirroring the application structure.

---

## 3. Strict Separation of Responsibilities

### UI rules

UI modules may:

- create and arrange widgets;
- bind events;
- collect and validate simple user input;
- call feature, service, or backend APIs;
- display progress, results, warnings, and errors.

UI modules must not:

- parse or serialize complex file formats;
- contain large transformation algorithms;
- perform long-running work directly on the UI thread;
- contain reusable domain logic;
- directly modify unrelated application state;
- duplicate logic already owned by another module.

### Backend rules

Backend modules must expose small, explicit APIs. They must not import UI modules or display dialogs. Return values or raise descriptive exceptions and let the UI decide how to present the result.

### Feature rules

Each feature module must have one clear purpose. For example:

- `function_map_export.py` owns map-export behavior;
- `function_density.py` owns density calculations and transformations;
- `function_xml_repair.py` owns XML repair behavior;
- `ui_tab_settings.py` owns only the Settings tab presentation and event wiring.

If a file name needs the word `and` to describe unrelated responsibilities, split the file.

### Dependency direction

Use this default dependency direction:

```text
launcher -> app/main -> ui -> functions/services -> backend/models/config/database
```

Lower-level modules must not import higher-level UI modules. Avoid circular imports. If two modules depend on each other, move the shared contract or model to a lower-level module.

---

## 4. File and Function Size

Keep modules focused and readable.

- Prefer one primary responsibility per file.
- Prefer functions that perform one operation.
- Split a function when it mixes validation, transformation, persistence, and presentation.
- Split a UI module when a tab or dialog becomes an independently maintainable component.
- Extract repeated logic after the second real use, not in anticipation of hypothetical reuse.
- Do not hide complex logic in anonymous functions, deeply nested callbacks, or oversized constructors.

These are review signals rather than automatic limits:

- a function longer than approximately 50 lines should be reviewed for decomposition;
- a class longer than approximately 300 lines should be reviewed for separation;
- a module longer than approximately 500 lines should be reviewed for splitting by responsibility.

A longer unit is acceptable only when splitting it would make the behavior harder to understand. Document that reason in the code.

---

## 5. Mandatory English Documentation and Comments

All source code documentation must be written in English. This includes:

- module docstrings;
- class docstrings;
- function and method docstrings;
- inline comments;
- constant descriptions;
- TODO and FIXME notes;
- build-script comments;
- workflow comments;
- error messages intended for developers.

User-facing text may be localized separately, but source-code explanations remain English.

### Required documentation level

Every source file must begin with a module docstring that explains:

1. the module's responsibility;
2. what it owns;
3. important constraints or side effects.

Every class must have a docstring explaining its role and lifecycle.

Every function and method, including private helpers, must have an English docstring that describes:

- what it does;
- its important arguments;
- its return value;
- relevant side effects;
- exceptions that callers are expected to handle.

All non-obvious constants must have an adjacent English comment explaining:

- what the value controls;
- its unit, coordinate space, or format where applicable;
- why the default was chosen;
- what changing it affects.

### Comment quality

Comments must explain intent, constraints, risks, or reasons. Do not merely repeat the code.

Good:

```python
# Write to a sibling temporary file first so a failed serialization cannot
# destroy the last valid user document.
```

Bad:

```python
# Write the file.
```

Document unusual compatibility workarounds where they occur. Include the triggering condition and the reason the normal implementation is insufficient.

When changing code, update nearby comments and docstrings. Outdated documentation is a defect.

---

## 6. Naming and Style

- Use descriptive English names.
- Use `snake_case` for files, functions, methods, and variables.
- Use `PascalCase` for classes.
- Use `UPPER_SNAKE_CASE` for constants.
- Prefix internal helpers with `_` only when they are intentionally private to a module or class.
- Name files by responsibility, not by implementation history.
- Avoid names such as `helpers.py`, `misc.py`, `common.py`, `new.py`, or `temp.py` unless their scope is genuinely narrow and explicit.
- Use `pathlib.Path` for filesystem paths.
- Use type hints for public APIs and complex internal functions.
- Prefer explicit imports. Do not use wildcard imports.
- Keep import side effects to a minimum.
- Use UTF-8 for all text files.

Public interfaces should remain small. Do not expose internal implementation details without a real caller need.

---

## 7. Error Handling, Data Safety, and Logging

- Never use an empty `except` block.
- Catch the narrowest practical exception type.
- Add context when re-raising an exception.
- Never silently discard failed operations.
- Validate user-controlled paths and inputs before changing files.
- Use atomic writes for important user data: write and validate a temporary file, then replace the target.
- Never overwrite an original source file when a patch, generated file, cache, or export can be used instead.
- Preserve unknown or unsupported content whenever the application edits structured data.
- Do not normalize data unless normalization is an explicit feature requirement.
- Use the standard `logging` module for diagnostic output in non-trivial applications.
- Keep user-facing error messages actionable and concise; keep technical details in logs.

Long-running tasks must provide visible status or progress and must not freeze the UI. Use a worker mechanism appropriate to the selected UI framework, but keep all UI updates on the UI thread.

### Log and output windows

Whenever a window, dialog, panel, or text area displays live log output, status messages, console output, build output, or other continuously appended information, it must automatically scroll to the newest entry.

Mandatory behavior:

- after appending a new log or output entry, scroll the view to the end;
- the most recent content must always remain visible without requiring manual scrolling;
- automatic scrolling must continue while new output is produced;
- the implementation must be performed on the UI thread when required by the UI framework;
- the log widget should remain read-only for the user unless editing is an explicit feature;
- when output is produced from a worker thread or subprocess, forward the text safely to the UI thread before updating and scrolling the widget.

For Tkinter or CustomTkinter text-based log widgets, the equivalent behavior should update the widget and then move the viewport to the end, for example with `see("end")` after inserting new content.


---

## 8. Mandatory UI, Background Processing, and Settings Rules

### Background processing and workers

All operations that can noticeably block, delay, or freeze the interface must run outside the UI thread. The application UI must remain responsive while file processing, parsing, conversion, scanning, calculation, importing, exporting, network access, build operations, or other expensive work is running.

Mandatory rules:

- never perform expensive or potentially blocking operations directly on the UI thread;
- move appropriate work to background workers;
- complex workloads that can safely be processed independently should be divided across multiple workers;
- the worker count must always be configurable by the user in the Settings UI;
- define a safe default worker count and validate configured values before creating workers;
- never create an unbounded number of threads or processes;
- only parallelize tasks that can safely run concurrently;
- protect shared state and avoid concurrent writes to the same target unless the implementation explicitly guarantees safety;
- worker exceptions must be captured and returned to the controlling layer instead of silently terminating a worker;
- cancellation and shutdown must stop or drain workers cleanly where the operation supports cancellation;
- progress, log messages, and completion events must be forwarded safely to the UI thread;
- background workers must never directly manipulate Tkinter, CustomTkinter, PyQt6, or other UI widgets from a worker thread unless the framework explicitly guarantees that operation is thread-safe.

The selected worker strategy must match the workload. I/O-bound tasks may use threads where appropriate. CPU-heavy work that can be separated safely should use real parallel execution where the selected Python/runtime architecture benefits from it. Do not add multiprocessing merely to satisfy this rule when the workload cannot safely or usefully be split.

The worker-count setting must be centralized and reused by all features that support parallel execution. Do not create unrelated hard-coded worker counts in individual feature modules.

### Mandatory GUI framework decision before initial implementation

Before writing the first application code for a new project, ask the user which of these GUI variants should be used:

1. `CustomTkinter` with dark mode as the default appearance; or
2. `PyQt6` with Qt Quick Controls `Material` style in dark mode using a blue primary/accent color scheme.

   Reference: https://doc.qt.io/qtforpython-6/overviews/qtquickcontrols-material.html#material-style

Do not begin the initial application implementation until that framework/style choice has been provided. Once the framework and style are selected, use them consistently throughout the application and avoid mixing GUI frameworks or unrelated visual styles.

Before initial code generation, also ask the user explicitly and separately whether these optional integrations should be included:

1. `GitHub button` in the main UI;
2. `Ko-fi button` in the main UI;
3. `Update check` using local and GitHub `version.txt`.

Do not assume that these integrations are wanted. Record the three choices and generate only the integrations the user enabled. The GUI framework/style choice and these integration choices should be collected before the first application code is written so the initial project structure, configuration, build script, packaging script, and release workflow can be generated consistently.

### Mandatory application-wide dialog and status-window styling

Every status window, progress window, log window, dialog, message box, confirmation window, warning, error dialog, update-status window, settings dialog, file-operation dialog, and other secondary window must use the same visual style as the main application.

Mandatory rules:

- secondary windows must visually belong to the application and must not fall back to an unrelated default toolkit appearance;
- use the same dark-mode policy, color palette, typography, spacing, button styling, border treatment, corner styling, and general layout language as the main UI;
- when `CustomTkinter` is selected, dialogs and status windows must use the application's CustomTkinter dark appearance wherever technically possible instead of unstyled Tk widgets;
- when `PyQt6` with Qt Quick Controls `Material` style in dark mode using a blue primary/accent color scheme is selected, dialogs and status windows must use that same application style and palette;
- reusable dialog/status-window components should be centralized in `app/templates/` or the corresponding shared UI component directory so features do not create inconsistent one-off dialogs;
- native operating-system dialogs may be used only where a native dialog is intentionally required, such as an appropriate system file/folder picker;
- new dialogs must be checked for visual consistency before the feature is considered complete.


### Main UI header buttons

Before writing the first application code, ask the user whether the GitHub and Ko-fi buttons should be included. If enabled, the application's main UI must provide the selected persistent external-link buttons in its upper-right area. They must remain easy to discover and must not be hidden inside a menu.

Available optional links:

- `GitHub`: black button linking to [gz2k2 on GitHub](https://github.com/gz2k2);
- `Ko-fi`: red-brown button linking to [gz2k2 on Ko-fi](https://ko-fi.com/gz2k2).

Place the two buttons next to each other in the upper-right area of the main UI. Their ordering must remain consistent across the application. Opening either link must use the operating system's default web browser. External-link handling should be implemented in a small reusable helper rather than duplicated in each button callback.

### Mandatory reusable UI templates

Pop-up windows, dialogs, tables, and other recurring complex UI elements must be implemented as reusable templates/components. Feature modules must configure or extend these templates instead of recreating the same widgets and behavior independently.

Recommended shared components include:

```text
app/templates/
├── template_popup.py
├── template_dialog.py
├── template_table.py
├── template_map_view.py
├── template_statuswindow.py
└── template_progresswindow.py
```

Mandatory rules:

- common layout, styling, lifecycle handling, keyboard behavior, and reusable actions belong in the template;
- feature-specific data and callbacks are supplied through a clear configuration/API;
- do not copy and modify an existing pop-up, dialog, or table implementation when the same behavior can be represented by extending its template;
- templates must follow the selected application-wide visual style;
- templates must remain sufficiently generic so feature-specific business logic does not leak into shared UI components;
- changes to shared behavior should normally be implemented in the template so all consumers benefit consistently.

#### Table template requirements

The reusable table template must provide the common table capabilities required throughout the application. At minimum, its API must support:

- sorting rows by clicking/selecting a column;
- correct sorting for relevant value types, including text and numeric values where required;
- enabling or disabling cell/content editing per table, column, or use case;
- validation hooks for editable values before changes are accepted;
- row, cell, text, foreground, and/or background coloring where required by the selected GUI framework;
- conditional coloring based on values, categories, states, warnings, or other feature-provided rules;
- configurable columns, headings, widths, alignment, and visibility;
- selection handling and reusable callbacks for feature-specific actions;
- preserving a clean separation between the generic table component and feature-specific table data or rules.

Editing and coloring do not have to be enabled for every table. They must be built into the reusable table template as configurable capabilities so individual tables can enable them when needed without implementing separate table systems.

Feature modules should provide data, column definitions, formatting rules, edit permissions, validation callbacks, and action callbacks to the table template. They should not reimplement basic sorting, editing, selection, or coloring infrastructure.

#### Map-view template requirements

Windows and views that display an image, map, heightmap, floor plan, canvas, texture, or similar visual surface with projected or interactive elements must use a reusable map-view template. The shared component should normally be implemented as `app/templates/template_map_view.py` and must own the common navigation and input behavior.

At minimum, the map-view template must provide configurable support for:

- zoom in and zoom out;
- zooming with the mouse wheel;
- panning the view in all directions;
- panning by pressing and holding the **middle mouse button** and dragging the mouse; this is the mandatory default pan binding;
- keyboard-controlled map navigation;
- reusable mouse bindings for map interaction;
- reusable keyboard bindings for map interaction;
- translating screen/view coordinates to map/image coordinates and back where overlays require it;
- keeping projected overlays, markers, paths, selections, and other elements aligned with the underlying image while zooming or panning;
- configurable minimum and maximum zoom levels;
- a configurable initial zoom and initial viewport position;
- resetting or fitting the view to the displayed image/map when required;
- feature hooks for hover, click, selection, context-menu, placement, drag, or other map-specific actions without reimplementing the base navigation layer.

Mouse and keyboard bindings for common map navigation must be defined centrally in the template rather than independently by every map view. Feature-specific bindings may extend the template, but they must not unnecessarily replace or duplicate the standard navigation behavior.

The standard mouse binding for pan is **middle mouse button press + drag**. Releasing the middle mouse button ends the pan operation. Left-click and right-click must remain available for feature-specific selection, placement, context-menu, or editing actions unless a feature explicitly requires otherwise.

The map-view template must keep image rendering, overlays, coordinate transformations, zoom state, and pan state synchronized. A feature module must provide the image/map data and feature-specific projected elements through a clear API instead of implementing its own independent zoom/pan system.

When a projected element represents map coordinates, its logical coordinates must remain independent from the current screen zoom. Zooming and panning must change only the presentation/viewport transformation and must not corrupt or permanently rewrite the underlying map coordinates.

### Settings UI structure

Every application must provide a Settings area. The Settings UI must itself be divided into meaningful sub-tabs whenever multiple groups of settings exist. Do not place all application settings into one continuously growing view.

Group settings by responsibility, for example:

```text
Settings
├── General
├── Processing
│   └── Worker count
├── Paths
├── Appearance
├── Updates
└── Advanced
```

Only create tabs that are meaningful for the application. Prefer several focused settings tabs over a bloated single settings page. Related options must remain together, and advanced or rarely used options should not dominate the default settings view.

### Settings Save button

The Settings UI must always provide a `Save` button in the bottom-right corner.

Mandatory behavior:

- the button must remain visible when switching between Settings sub-tabs;
- the button must not disappear below scrollable settings content;
- the Settings content area may scroll, but the bottom action area containing `Save` should remain fixed;
- `Save` must validate settings before persistence;
- invalid values, including invalid worker counts, must be reported without silently overwriting the last valid settings;
- settings persistence logic must remain outside the widget-layout implementation.

---

## 9. Configuration, Resources, and Runtime Paths

- Keep configurable values out of feature algorithms.
- Store application defaults and option definitions in `app/config/`.
- Store application-owned lookup tables in `app/database/`.
- Store bundled read-only files in `data/` or `assets/`.
- Store user-writable settings and generated data outside bundled resources.
- Centralize platform-specific behavior in a platform configuration or service module.
- Resolve resource paths correctly in both source mode and one-file executable mode.
- Do not depend on the current working directory.
- Do not use hard-coded absolute development paths.

When adding or moving a resource, update all of the following where relevant:

1. runtime path resolution;
2. `00_build_onefile.py` data-file declarations;
3. `00_pack_project.py` include/exclude rules;
4. `.github/workflows/release.yml` packaging steps;
5. tests that verify resource availability.

---

## 10. Dependencies

- Declare every runtime and build dependency in `requirements.txt` or in clearly separated requirement files if the project requires multiple environments.
- Pin versions when reproducibility or binary compatibility requires it.
- Remove dependencies that are no longer used.
- Prefer the Python standard library when it provides a clear and maintainable solution.
- Do not add a dependency for a trivial helper.
- Verify that every dependency works with the Python version used in `release.yml`.
- Verify that PyInstaller can discover or explicitly collect every dynamic dependency.
- Document external executable requirements and how they are packaged.

---

## 11. Tests

Every substantial feature and every bug fix must include or update tests.

Required testing principles:

- mirror application responsibilities in the `tests/` directory;
- test public behavior rather than private implementation details;
- add a regression test for each fixed bug where practical;
- use temporary directories for filesystem tests;
- never write tests into real user directories;
- keep fixtures small and purpose-specific;
- test malformed, missing, empty, and partially valid input when the feature handles files;
- test resource-path behavior where packaging is relevant;
- keep UI logic thin enough that feature behavior can be tested without launching the complete application.

Before completion, run the project's actual test command. A change is not complete merely because the application starts.

---

## 12. Mandatory One-File Build Script

Every new application must include a root-level `00_build_onefile.py` that matches the current code and resource structure.

The script must:

1. use the current Python interpreter via `sys.executable`;
2. read the version from `version.txt`;
3. validate the launcher, package root, requirements, resources, and required modules before deleting old output;
4. optionally install or clearly verify required build dependencies;
5. clean stale `build/`, `dist/`, and generated `.spec` files;
6. run PyInstaller in one-file mode;
7. select windowed or console mode to match the application;
8. include all required `data/` and `assets/` resources;
9. include required hidden imports and package collections;
10. exclude tests and development-only modules;
11. support platform-specific executable suffixes;
12. create a versioned output name such as `<ApplicationName>_v<version>`;
13. fail with a non-zero exit code when validation or building fails;
14. print the final artifact path after a successful build.

The build script is production code. It must be fully documented in English and kept synchronized with package renames, new modules, resources, dependencies, and external tools.

Do not commit generated PyInstaller `.spec` files unless the project deliberately uses a maintained spec file. If a spec file is required, treat it as source code and keep it synchronized with `00_build_onefile.py`.

---

## 13. Mandatory Project Pack Script

Every new application must include a root-level `00_pack_project.py`.

Its purpose is to create a reviewable and transferable project package containing the source and essential project metadata while excluding generated, private, or unnecessary content.

The script must:

1. determine the project root from `__file__`;
2. create its output in a dedicated `packed/` directory;
3. use a deterministic, versioned, or timestamped output name;
4. include source files, workflow files, Markdown documentation, configuration templates, and other explicitly required text resources;
5. preserve each file's relative path;
6. use UTF-8 and normalized line endings for text output;
7. sort files deterministically;
8. report the output path, file count, and final size;
9. fail clearly if a file cannot be read or written;
10. exclude the output package itself.

At minimum, exclude:

```text
.git/
.github cache directories
__pycache__/
*.pyc
.venv/
venv/
build/
dist/
packed/
coverage output
IDE metadata
local settings
secrets and credentials
user-generated files
large external tools
binary caches
temporary files
```

The pack script must never include `.env` files, access tokens, credentials, private keys, local machine paths, or personal user data.

If an unpack script is provided, it must validate paths and prevent directory traversal before writing files.

---

## 14. Mandatory GitHub Release Workflow

Every new application must include `.github/workflows/release.yml`, and the workflow must match the actual application, build script, supported platforms, dependencies, and artifact names.

The workflow must:

1. support manual execution with `workflow_dispatch`;
2. define an intentional release trigger, preferably version tags matching `v*`;
3. use the minimum required permissions, normally `contents: write` for release creation;
4. check out the repository with a current stable `actions/checkout` release;
5. set up the Python version used by the project;
6. install dependencies from the repository's requirement file;
7. install required system packages for the target runner;
8. run automated tests before packaging;
9. call `python 00_build_onefile.py` instead of duplicating local build logic;
10. verify that the expected build artifact exists;
11. package required external tools or resource directories in the final distribution;
12. upload intermediate build artifacts when jobs run on different operating systems;
13. create one GitHub Release containing the intended platform artifacts;
14. use the version from the tag or `version.txt` consistently;
15. use descriptive, versioned artifact names;
16. fail when required files are missing;
17. avoid embedding secrets in YAML or scripts.

If Windows and Linux are supported, create separate build jobs and a final release job. Platform-specific failures must be handled intentionally. Do not silently ignore a required test or build failure with `|| true` unless the command is explicitly diagnostic and the reason is documented in English.

Keep action versions current and pinned to explicit major versions. Review external download URLs, checksums, and fallback behavior. Prefer release assets from official upstream repositories.

---

## 15. Optional Application Update Check

Before writing the first application code, ask the user whether an update check should be included. If enabled, the application must include an update-check mechanism that compares the locally installed application version with the current version published in the application's GitHub repository.

### Version source

- The local version must be read from the application's `version.txt`.
- The remote version must be read from a `version.txt` stored in the corresponding GitHub repository.
- Do not hard-code the installed or current release version in the update-check implementation.
- Keep the repository URL and remote `version.txt` location in a clearly defined configuration constant rather than scattering URLs through UI or feature code.
- The implementation must work both when running from source and from the packaged one-file executable.

### Update-check behavior

The update check must:

1. read and normalize the local version from `version.txt`;
2. request the remote `version.txt` from the configured GitHub repository;
3. compare the two versions using a deterministic version comparison rather than plain string ordering;
4. distinguish at least between up-to-date, update-available, and update-check-failed states;
5. use a reasonable network timeout so an unavailable GitHub connection cannot freeze application startup;
6. perform network access outside the UI thread when required by the UI framework;
7. return the result to the UI thread before creating or modifying UI widgets;
8. handle missing files, malformed version values, network errors, HTTP errors, and offline operation without crashing the application.

A failed update check must never prevent the application from starting or being used.

### Mandatory update status window

The update check must display a status window. The status window must clearly show:

- `Current version`: the local version read from `version.txt`;
- `New version`: the version read from the GitHub `version.txt`;
- `GitHub repository`: a clickable link to the corresponding GitHub repository.

The window must also clearly identify the result, such as:

- `Application is up to date`;
- `A new version is available`;
- `Update check failed`.

When the remote version cannot be retrieved, do not invent or substitute a version value. Display the local version, indicate that the remote version is unavailable, and keep the GitHub repository link available.

The GitHub link must open the configured repository in the system's default browser. Keep browser-opening behavior outside the update-check network logic so it can be maintained and tested independently.

### Architecture

The update checker must follow the same separation-of-responsibilities rules as the rest of the application. A recommended structure is:

```text
app/
├── config/
│   └── config_update.py          # Repository and remote version configuration.
├── functions/
│   └── function_update_check.py  # Version retrieval and comparison logic.
└── ui/
    └── ui_update_status.py       # Update status window and user interaction.
```

The network/version logic must not directly create UI widgets, and the status window must not implement HTTP requests or version-comparison logic.

All update-check code, constants, functions, error handling, and non-obvious behavior must be documented and commented in English according to the documentation rules in this file.

### Build and packaging requirements

Whenever the update-check mechanism is added or changed, verify that:

- `version.txt` is available to the packaged application;
- `00_build_onefile.py` includes the required update-check modules, resources, and dependencies;
- `00_pack_project.py` includes the source files and `version.txt`;
- `.github/workflows/release.yml` publishes a repository state in which the remote `version.txt` matches the intended release version;
- the executable, release artifact, Git tag, release name, local `version.txt`, and remote `version.txt` use the same application version.

---

## 16. Versioning and Release Consistency

Use one authoritative application version stored in `version.txt` unless the selected ecosystem provides a better single source of truth.

The following must agree:

- `version.txt`;
- executable name;
- package/archive name;
- Git tag;
- GitHub Release name;
- displayed application version;
- changelog entry.

The launcher and application code must not contain independent hard-coded versions.

Before a release:

1. update `version.txt`;
2. update `CHANGELOG.md`;
3. run all tests;
4. run `00_build_onefile.py` locally on supported systems where practical;
5. run `00_pack_project.py` and inspect its contents;
6. verify that bundled resources and external tools are present;
7. verify startup from the built executable outside the repository;
8. verify that `release.yml` expects the exact produced file names;
9. create and push the matching version tag.

---

## 17. README Requirements

Every application must include an English `README.md` containing:

- application purpose;
- supported operating systems;
- screenshots when appropriate;
- prerequisites;
- source installation instructions;
- source startup command;
- test command;
- one-file build command;
- project pack command;
- release process;
- directory overview;
- configuration and user-data locations;
- known limitations;
- license information.

Update the README whenever commands, files, dependencies, supported systems, or packaging behavior change.

---

## 18. Definition of Done

A task is complete only when all applicable items are true:

- the implementation is placed in the correct functional directory;
- blocking work is moved to background processing and safely parallelized where appropriate;
- the worker count is configurable in Settings;
- Settings are divided into meaningful sub-tabs and the bottom-right `Save` button remains visible;
- enabled GitHub and/or Ko-fi buttons are present in the upper-right main UI;
- all status windows, progress windows, and dialogs consistently use the selected application style;
- recurring pop-ups, dialogs, and tables use reusable UI templates instead of duplicated implementations;
- table views use the shared table template for sorting and configurable editing/coloring behavior where required;
- map/image views with projected elements use the shared map-view template for zoom, pan, coordinate transforms, and common mouse/keyboard bindings;
- files and functions have focused responsibilities;
- all code, functions, constants, and non-obvious behavior are documented in English;
- no unrelated logic was added to UI or startup modules;
- errors are handled explicitly;
- user data is preserved safely;
- tests were added or updated and pass;
- dependencies are declared;
- resource paths work in source and packaged modes;
- `00_build_onefile.py` matches the code and resources;
- `00_pack_project.py` matches the project structure;
- `.github/workflows/release.yml` matches the build outputs;
- when enabled, the update check compares local and GitHub `version.txt` values and displays its status window;
- version and artifact names are consistent;
- `README.md` and `CHANGELOG.md` are current;
- generated files, caches, secrets, and local user data are not committed.

---

## 19. Final Review Checklist for Coding Agents

Before returning a completed change, verify and report:

```text
[ ] Architecture inspected before implementation
[ ] GUI framework/style was selected before initial coding: CustomTkinter dark mode or PyQt6 Qt Quick Controls Material style dark mode with blue primary/accent colors
[ ] Expensive/blocking tasks use background workers where appropriate
[ ] Complex divisible workloads use the configured worker count
[ ] Worker count is configurable in Settings
[ ] Settings use meaningful sub-tabs and keep Save visible at bottom-right
[ ] Initial GitHub/Ko-fi/update-check choices were requested; enabled GitHub/Ko-fi buttons are present in the upper-right area
[ ] All status windows and dialogs use the selected application-wide visual style
[ ] Pop-ups, dialogs, tables, status windows, and other recurring complex UI elements use reusable templates
[ ] Table template provides column sorting plus configurable editing, validation, selection, and coloring capabilities
[ ] Map/image views use the reusable map-view template; pan defaults to middle-mouse-button click/hold + drag, with shared zoom, coordinate transformation, and mouse/keyboard bindings
[ ] Code placed in responsibility-specific modules
[ ] No circular or UI-to-backend dependency violations
[ ] English module, class, function, and method documentation complete
[ ] Non-obvious constants and algorithms commented in English
[ ] Error handling and data preservation reviewed
[ ] Tests added or updated
[ ] Tests executed successfully
[ ] requirements.txt updated when needed
[ ] 00_build_onefile.py created or synchronized
[ ] 00_pack_project.py created or synchronized
[ ] .github/workflows/release.yml created or synchronized
[ ] If update check was enabled, it reads local and GitHub version.txt and shows the required status window
[ ] Resources included in source mode and one-file builds
[ ] Version and output names consistent
[ ] README.md and CHANGELOG.md updated
[ ] No secrets, caches, build output, or user data added
```

If an item is not applicable, state why. Do not claim that a test, build, package, or release check passed unless it was actually executed successfully.
