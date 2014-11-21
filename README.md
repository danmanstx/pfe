# Sublime Text Postgresql Function Editor

Plugin for Sublime Text 3 editor that helps you work directly with postgresql database functions and run pgTAP test.

## Features

* Load functions from a specified database
* Save a Function to the database with output
* Ability to Run a [pgTAP](http://pgtap.org) test

![gifgifgif](https://raw.github.com/danmanstx/pfe/master/images/pfe.gif)

## Usage

### Set Database Information

* Invoke via <kbd>⌃</kbd>+<kbd>⇧</kbd>+<kbd>D</kbd> / <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Set Databse Info`) or right-click menu
* set json values for `host`, `databse`, `user`, `port`


![Sample Database Info File](https://raw.github.com/danmanstx/pfe/master/images/settings.png)

### Load Database functions

* Invoke via <kbd>F1</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Load Database Functions`) or right-click menu
* Loads the database functions in the side bar seperated by folders which one for each schema


### Save a Function to The Database

* Invoke via <kbd>F2</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Save Database Function`) or right-click menu
* Saves the function to the database and opens a panel with the command output

![Saved Function](https://raw.github.com/danmanstx/pfe/master/images/save.png)

### Run [pgTAP](http://pgtap.org) Test

* Invoke via <kbd>F3</kbd> (menu: `Tools` -> `Postgresql Function Editor` -> `Run pgTAP Test`) or right-click menu
* Saves the function to the database and opens a panel with the command output

![Test Output](https://raw.github.com/danmanstx/pfe/master/images/test.png)


### dependencies

* Sublime Text 3
* working ruby install with support for [rvm](http://rvm.io), [macports](http://www.macports.org), and system ruby
* [Ruby gem PG](https://rubygems.org/gems/pg)

## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/danmanstx/pfe/issues).

**COMING SOON** install with [Package Control](http://wbond.net/sublime_packages/package_control):

1. checkout the repo and install it in your sublime text Packages folder.
2. Restart ST editor (if required)

## Options

Sample options below.

Go to `Preferences` -> `Settings - User` and add this to the file:

`{
  "function_folder": "/tmp/postgresFunctions",
  "host": "localhost",
  "database": "database",
  "user": "postgresql",
  "password": "",
  "port": "5432",
  "ruby_manager": "rvm"
}`

## Changelog

### v1.0.0

* Initial release

## Acknowledgments

Inspired by [Suran Systems](http://www.suran.com) Textmate Postgresql Bundle.

## Copyright and license

Copyright © 2013 @[danmanstx](http://twitter.com/danmanstx)

Licensed under the [**GNU GPL**](https://gnu.org/licenses/gpl.html) license.