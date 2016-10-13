# SwiftyLocalization
A simple localization solution for iOS. Google Spreadsheets -> Localizable.strings -> Swift's struct.

From Google Spreadsheet:
![Alt text](/Screen Shot 2559-10-13 at 1.56.55 AM.png "Spreadsheet")

To struct:
![Alt text](/Screen Shot 2559-10-13 at 4.05.57 AM.png "generated struct")

# Features
- [x] Flexible localization with Google Spreadsheets - comment, color & fonts and much more
- [x] Multiple Spreadsheets support - distinguish between pages/features/domains
- [x] Generate Localizables.string - no more touching these files
- [x] :tada: Generate Localizables.swift - a struct that manages all keys, decode and return localized String. **No more wrong keys out of nowhere, the compiler catches them for you!**

<br>
For Android:
- [x] Generate value-lang/strings.xml (not thoroughly tested yet)
- [ ] Generate a counterpart of Localizables.swift - a helper to decode and return localized String.

# Overview

- Edit Google Spreadsheets
- Spreadsheets -> csv files (Google App Script)
- csv files -> local csv files (Synced by Google Drive app, or manually download)
- local csv files -> Localizable.strings & Localizables.struct (Python script)


# Steps
1. Edit Google Spreadsheets. Look at a guideline [here.](https://docs.google.com/spreadsheets/d/1zB_tPPhUxbjB6sVpLmvgGVXdd-7d5mvfrOaCzgkhHv8/edit?usp=sharing)
2. Export them to csv files with [Michael Derazon's Google script.](https://www.drzon.net/export-all-google-sheets-to-csv/) A slightly modified version is included here (google_sheets_export_csv.txt). Just copy to script editor and run it. After this, a folder named 'csvFiles' will waiting in your Drive folder. It contains all csv files from all sheets (sheetname.csv). Change the code, e.g. for folder names, as you need.
3. (Optional) For quick development iteration:
    1. Sync 'csvFiles' with [Google Drive app for mac](https://www.google.com/drive/download/). So that everytime you run script to export csv, 'csvFiles' will be available locally on your local Drive's folder.
    2. softlink (ln -s) your local Google Drive with:
        ````bash
        ln -s {path-to-your-csvFiles-in-local-Drive} {anywhere-near-your-xcode-project}
        ````
    So that your project has kind of shortcut to 'csvFiles'.
4. Get csvFiles (either by 3. or download manually from Google Drive).
5. Generate Localizable.strings & Localizables.swift.

      Set your paths & how to decode a key to a localized string at settings.json. Then run this script:

      ````python
      python csv_localizer.py
      ````
      Or you can just double-click on main.command (for mac), it will run this on terminal for you.


   **HOW IT WORKS**

   **TL;DR**: *Take a look at /SampleOutput/struct/Localizables.swift. Then you may not need to know about this.*

   What the script do is that it will find input path to csvFiles (path/name from settings.json), then it aggregates every .csv files inside that folder **recursively.** Then it generates {lang}.lproj/Localizable.strings to your output path. It prepends each key with a sheet name, so {sheetname}_{key} is the actual key inside our string files.


   The generated struct will be named Localizables.swift. Nested structs will have same name as sheet_name. Each has key as in your Spreadsheets. Each variable inside is a computed static var (so that everytime we get its value, it returns a localized string that reflects current in-app language). **For the struct to work, you need to specify how to decode a localized string given a key in settings.json.** For example, you can use NSLocalizedString. I use [this great library](https://github.com/marmelroy/Localize-Swift) to help manage in-app language setting. It has a String extension that allows me to use "key".localized() to return a string. I set "\"{key}\".localized()" in settings.json.


   To use. Suppose you have a sheet named 'login' with a key 'button_title_register' inside, you can retrieve it like:
   ````Swift
   Localizables.login.button_title_register
   ````


Settings.json
---

- BASE_STRING_PATH: a base path
- IN_PATH: a folder of csv files, relative to the base path
- OUT_PATH: a folder to output localizables, relative to the base path
- PLATFORM: ios or android (android will generate strings.xml)
- LANG_KEYS: array of valid language codes. e.g. ["en", "fr", "th"]. It will be used as {lang}.lproj for ios, and values-{lang} for android.
- GEN_STRUCT_IF_IOS: whether to generate Localizables.swift or not (true or false)
- GEN_STRUCT_BASE_PATH: a base path for struct generation
- GEN_STRUCT_OUT_PATH: a folder to put a struct
- GEN_STRUCT_FILE_NAME: a name of struct file. e.g. Localizables.swift
- GEN_STRUCT_STRUCT_NAME: name of struct. e.g. Localizables
- **GEN_STRUCT_VALUE_RETRIEVAL: specify a way to decode localized string from a key.** E.g. if you have a function "key".localized() to get a value. You can set this field to "\"{key}\".localized()". Or use plain NSLocalizedString like "NSLocalizedString(\"{key}\", tableName: nil, bunedle: bundle)"

Benefits
---
* Format Google Spreadsheets as you like. As an idea, fill unfinished translation cell with red color. Add comments. Add border to visually group a set of related keys. Make some important keys with bigger fonts. Etc.
* No out-of-sync between different language files since we don't touch Localizable.strings anymore.
* Having struct as an interface to localized strings allows us to:
  * Use autocomplete
  * Xcode won't compile if there's a wrong key in the project.

---
:sweat_smile: Phews! That looks complicated and feels like homemade solution. But trust me, it's really worthwhile. Imagine this, that moment when you add a new key-value in a spreadsheet, click export csvFiles. Wait for them to sync on your local folder. And double click on main.command to update all files & struct with the latest version. Boom, that new key is avaiable instantly through Xcode Autocomplete!

Contribution
---
All suggestions/helps are welcome!
