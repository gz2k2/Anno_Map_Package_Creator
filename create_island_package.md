# How to Create an Island Package from Exported Islands (meow's Island Editor)

Follow this step-by-step guide to package custom islands created in meow's Island Editor (https://github.com/magicalcookie/anno-editor) and use them in TAMPER (https://github.com/Taludas/Anno-117-Map-Editor) or in-game as Random Islands.

For all this, you need my Island Package Creator (https://github.com/gz2k2/Anno_Map_Package_Creator)

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

## 2. Importing & Configuring in Island Package Creator

1. Open **Island Package Creator**, set the target game to **Anno 117**, and click **Add Islands (Folder)**.
2. Select your main working folder (`my own Islands`). Your exported islands will appear in the app list.
3. **Configure Island Specs:** Right-click each island in the list to assign the correct **island size** and **region**.

---

## 3. Building the Island Package

1. **Create Package:** Go to the **Island Packages** tab, create a new package, set its name and version, and optionally select a default region.
2. **Assign Islands:** Return to the **General** tab, select the islands you wish to include (mass selection supported), right-click, and add them to your package.
3. **Attach Assets:** 
   * Go back to the **Island Packages** tab and click on your newly created package to verify your listed islands.
   * Click the **Additional Files** button.
   * Click **Add Files**, navigate to `my own Islands/additional_files`, select the folder, and click **Save**.

---

## 4. Exporting as a Mod

1. Go to the **Export Island Package as Mod** tab.
2. Select your Island Package.
3. Browse to your Anno 117 Mods folder (`Anno 117/mods`).
4. Click **Export Island Package as Mod**.

All required files are now deployed to your game directory. Your custom islands are registered as **Random Islands** and will be placed naturally by the game generator.

---

## 5. Placing Custom Islands in TAMPER (Optional)

To build fully custom map layouts using your new islands, integrate them into the **Anno 117 Map Editor (TAMPER)** by [Taludas](https://github.com/Taludas/Anno-117-Map-Editor/releases):

1. Launch **TAMPER** and open **Options > Custom Island Paths**.
2. Click **Add Folder** and point it to your exported mod folder:  
   `Anno 117/mods/[Your_Package_Name]`
3. Import an existing map (**File > Import from Game**) or start a new project.
4. Access your islands via the **Place Custom Island** panel.
5. Design your map, export it as a mod, and enjoy your custom world in-game!