# Postgresql Function Editor - Sublime Plugin

Plugin for Sublime Text 3 editor that helps you work directly with postgresql database functions and run pgTAP test.
Currently under heavy development which can be tracked at [trello](https://trello.com/b/aNujDnId/posgresql-function-editor-sublime-text)

## Features

* Load functions from a specified database.
* Save a Function to the database with output.
* Ability to Run a [pgTAP](http://pgtap.org) test, or all open test files.
* Pgplsql highlighting, and pgTAP output panel highlighting.
* Quick Switch between file and test with <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd>.

![gifgifgif](https://raw.github.com/danmanstx/pfe/master/images/pfe.gif)

## Usage

### Set Database Information

* Invoke via <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Set Databse Info`)
* set database option values


![Sample Database Info File](https://raw.github.com/danmanstx/pfe/master/images/settings.png)

### Load Database functions

* Invoke via <kbd>F1</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Load Database Functions`)
* Loads the database functions in the side bar seperated by folders which one for each schema


### Save a Function to The Database

* Invoke via <kbd>F2</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Save Database Function`)
* Saves the function to the database and opens a panel with the command output

![Saved Function](https://raw.github.com/danmanstx/pfe/master/images/save.png)

### Run [pgTAP](http://pgtap.org) Test

* Invoke via <kbd>F3</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Run pgTAP Test`)
* Saves the function to the database and opens a panel with the command output

![Test Output](https://raw.github.com/danmanstx/pfe/master/images/test.png)


## Dependencies

* Sublime Text 3
* working ruby install with support for [rvm](http://rvm.io), [macports](http://www.macports.org), and system ruby **be sure to set in user settings**
* [Ruby gem PG](https://rubygems.org/gems/pg)
* [pgTAP](http://pgtap.org) for pgTAP testing

## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/danmanstx/pfe/issues).

**COMING SOON** install with [Package Control](http://wbond.net/sublime_packages/package_control):

1. checkout the repo and install it in your sublime text Packages folder, most likely found here `cd "$HOME/Library/Application Support/Sublime Text 3/Packages"`
2. Restart ST editor (if required)

## Options

Sample options below.

Go to `Preferences` -> `Settings - User` and add this to the file:

<pre>
{
  "function_folder": "/tmp/postgresFunctions",
  "host": "localhost",
  "database": "database",
  "user": "postgresql",
  "password": "",
  "port": "5432",
  "ruby_manager": "rvm"
}
</pre>

## Changelog

### v1.0.0

* Initial release

## Acknowledgments

* Inspired by [Suran Systems](http://www.suran.com) Textmate Postgresql Bundle.
* Inspired by [Ruby Test](https://github.com/maltize/sublime-text-2-ruby-tests).

## Copyright and license

Copyright © 2014 @[danmanstx](http://twitter.com/danmanstx)

Licensed under the [**GNU GPL**](https://gnu.org/licenses/gpl.html) license.