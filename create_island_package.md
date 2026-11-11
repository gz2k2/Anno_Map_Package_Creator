# How to Create an Island Package from Exported Islands (meow's Island Editor)

Follow this step-by-step guide to package custom islands created in [meow's Island Editor](https://github.com/magicalcookie/anno-editor) and use them in [TAMPER](https://github.com/Taludas/Anno-117-Map-Editor) or in-game as Random Islands.

For all this, you need my [Island Package Creator](https://github.com/gz2k2/Anno_Map_Package_Creator).

> 💡 **Anno 1800 Support:**  
> This guide works identically for **Anno 1800**. Simply set the target game in **Island Package Creator** to **Anno 1800** and use the [Anno 1800 Map Editor](https://github.com/gz2k2/Anno-1800-MapEditor_p) instead of TAMPER. The rest of the workflow is exactly the same.

---

## 1. File Preparation & Folder Setup

1. **Export Islands:** Export all created islands to a mod using **meow's Editor**.
2. **Copy Province Files:** Navigate to the exported mod directory and copy all island files from `/data/base/provinces` into a new working folder (e.g., `my own Islands/provinces`).
3. **Set Up Additional Files:**
   * Create an `additional_files` folder inside your working directory:  
     `my own Islands/additional_files`
   * Create a `data` folder inside it:  
     `my own Islands/additional_files/data`
   * Copy all assets—including the `editor` folder—into this directory:  
     `my own Islands/additional_files/data/editor/...`

---

## 2. Create and Configure the Island Package

1. Open **Island Package Creator** and select **Anno 117** or **Anno 1800**.
2. Open **Island Packages**, click **New**, and create the package before importing Islands.
3. Enter the **Mod Name** and **Version**. Optionally configure a default **Region** and enable **Use different GUID ranges** with a package-specific GUID range.
4. Click **Save Package Settings**.

---

## 3. Import Islands Directly into the Package

1. Keep the target package selected in **Island Packages**.
2. Click **Add Islands (Folder)** and select your working folder (`my own Islands`), or use **Add Islands (File)** for one `.a7m`.
3. Every imported Island is assigned directly to the selected package. The configured package Region and package-specific GUID range are applied automatically when enabled.
4. Review the package table. Use the right-click menu to adjust **Region**, **GUID**, **Type**, or Anno 117 **Island Size** when required.
5. Click **Additional Files**, choose **Add Files**, select `my own Islands/additional_files`, and click **Save**.

---

## 4. Exporting as a Mod

1. Go to the **Export Island Package as Mod** tab.
2. Select your Island Package.
3. Browse to your game's mods folder (e.g., `Anno 117/mods` or `Anno 1800/mods`).
4. Click **Export Island Package as Mod**.

All required files are now deployed to your game directory. Your custom islands are registered as **Random Islands** and will be placed naturally by the game generator.

---

## 5. Placing Custom Islands in the Map Editor (Optional)

To build fully custom map layouts using your new islands, integrate them into the map editor:

* **Anno 117:** Use **TAMPER** by [Taludas](https://github.com/Taludas/Anno-117-Map-Editor/releases)
* **Anno 1800:** Use the [Anno 1800 Map Editor](https://github.com/gz2k2/Anno-1800-MapEditor_p)

**Steps:**
1. Launch the editor and open **Options > Custom Island Paths**.
2. Click **Add Folder** and point it to your exported mod folder (e.g., `Anno 117/mods/[Your_Package_Name]`).
3. Import an existing map (**File > Import from Game**) or start a new project.
4. Access your islands via the **Place Custom Island** panel.
5. Design your map, export it as a mod, and enjoy your custom world in-game!
