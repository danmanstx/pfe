# Postgresql Function Editor - Sublime Plugin

Plugin for [Sublime Text 3](http://www.sublimetext.com) that helps you work directly with postgresql database functions and run [pgTAP](http://pgtap.org) tests. [Trello board](https://trello.com/b/aNujDnId/posgresql-function-editor-sublime-text)

*Warning:* If you experience problems or have suggestions please [file an issue](https://github.com/danmanstx/pfe/issues).

## Features

* Creates a local temporary copy of all database functions from a specified database.
* Save a Function to the database with output.
* Ability to Run a [pgTAP](http://pgtap.org) test, or all open test files.
* Pgplsql highlighting, and pgTAP output panel highlighting.
* Quick Switch between file and test with <kbd>CMD</kbd>+<kbd>.</kbd>
* Quick Create new plpgsql functions with <kbd>CMD</kbd>+<kbd>ALT</kbd>+<kbd>o</kbd>.
* Common Completions and Snippets for `plpgsql` files

![gif](https://raw.github.com/danmanstx/pfe/master/images/pfe.gif)

## Usage

### Set Database Information

* Invoke via <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Set Databse Info`)
* set database option values


![Sample Database Info File](https://raw.github.com/danmanstx/pfe/master/images/settings.png)

### Load Database functions

* Invoke via <kbd>F1</kbd> or `Tools` -> `Postgresql Function Editor` -> `Load Database Functions`
* Loads the database functions in the side bar seperated by folders which one for each schema.


### Save a Function to The Database

* Invoke via <kbd>F2</kbd> or `Tools` -> `Postgresql Function Editor` -> `Save Database Function`
* Saves the function to the database and opens a panel with the command output.

![Saved Function](https://raw.github.com/danmanstx/pfe/master/images/save.png)

### Run [pgTAP](http://pgtap.org) Test(s)

#### Run test in active tab

* Invoke via <kbd>F3</kbd> or `Tools` -> `Postgresql Function Editor` -> `Run pgTAP Test`
* Saves the function to the database and opens a panel with the test output.

![Test Output](https://raw.github.com/danmanstx/pfe/master/images/test.png)

#### Run all opened tests

* Invoke via <kbd>F4</kbd> or `Tools` -> `Postgresql Function Editor` -> `Run All Opened Tests`
* Saves the active function to the database and opens a panel with the test output for all open test.

### Quick Switch/Create File

* Invoke via <kbd>CMD</kbd>+<kbd>.</kbd> or <kbd>CMD</kbd>+<kbd>Ctrl</kbd>+<kbd>.</kbd> for same pane split.
* Attempts to switch to or create the alternating file/test based on the schema and function name.
* this expects either a `public`/`testing` schema, or `foo` and `foo_testing` schemas as an example.

### Create New Function

* Invoke via <kbd>CMD</kbd>+<kbd>ALT</kbd>+<kbd>o</kbd>
* Brings up a list of schemas, and then allows you to specify the exact function you would like. Then use <kbd>F2</kbd> to save this function into the current database.

## Dependencies

* [Sublime Text 3](http://www.sublimetext.com) and [Package Manager](https://packagecontrol.io),
* [pgTAP](http://pgtap.org) for pgTAP testing
* passwordless access to database either through hba_conf file or .pgpass file.

## How to install on a Mac

* install [package manager](https://packagecontrol.io/installation)
* clone repo for pfe in packages directory

```bash
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
git clone https://github.com/danmanstx/pfe.git
```

* before closing sublime add `pfe` to your `installed packages` located here:<br>
  `Sublime text --> Preferences --> Package Settings --> Package Control --> Settings - User`

**COMING SOON** install with [Package Control](http://wbond.net/sublime_packages/package_control)

## Options

Sample options below.

Go to `Preferences` -> `Package Settings` -> `Postgresql Function Editor`->`Settings - User` and add this to the file or copy and edit from `Settings - Default` :

```json
{
  "function_folder": "/tmp/postgresFunctions",
  "host": "localhost",
  "database": "database",
  "user": "postgresql",
  "port": "5432",
}
```

## Changelog

### v1.0.0

* Initial release

## Acknowledgments

* Inspired by [Suran Systems](http://www.suran.com) Textmate Postgresql Bundle.
* Quick Switching Inspired by [Ruby Test](https://github.com/maltize/sublime-text-2-ruby-tests).
* Quick File Creation Inspired By [Sublime Quick File Creator](https://github.com/noklesta/SublimeQuickFileCreator)
* No more ruby or gems! Thanks to [Traveling Ruby](http://phusion.github.io/traveling-ruby/)

## Roadmap

* Add more plpgsql Snippets for better autocompletion.
* Add ability to save recently used databases.
* Add linux/Windows Traveling Ruby Packages.
* Creation of atom plugin because sublime's future is uncertain.

## Copyright and license

Copyright © 2015 Danny Peters, @[danmanstx](http://twitter.com/danmanstx)

Licensed under the [**GNU GPL**](https://gnu.org/licenses/gpl.html) license.
