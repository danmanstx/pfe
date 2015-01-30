# Postgresql Function Editor - Sublime Plugin

Plugin for Sublime Text 3 editor that helps you work directly with postgresql database functions and run pgTAP test.
Currently under heavy development. [trello board](https://trello.com/b/aNujDnId/posgresql-function-editor-sublime-text)

*Warning:* If you experience problems or have enhancements please [file an issue](https://github.com/danmanstx/pfe/issues).

## Features

* Load functions from a specified database.
* Save a Function to the database with output.
* Ability to Run a [pgTAP](http://pgtap.org) test, or all open test files.
* Pgplsql highlighting, and pgTAP output panel highlighting.
* Quick Switch between file and test with <kbd>CMD</kbd>+<kbd>.</kbd>.

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

#### Run all tests opened

* Invoke via <kbd>F4</kbd> or `Tools` -> `Postgresql Function Editor` -> `Run All Opened Tests`
* Saves the active function to the database and opens a panel with the test output for all open test.

### Quick Switch/Create File

* Invoke via <kbd>CMD</kbd>+<kbd>.</kbd> or <kbd>CMD</kbd>+<kbd>Ctrl</kbd>+<kbd>.</kbd> for same pane split.
* Attempts to switch to or create the alternating file/test based on the schema and function name.
* this expects either a `public`/`testing` schema, or `foo` and `foo_testing` schemas as an example.

## Dependencies

* Sublime Text 3
* working ruby install with support for [rvm](http://rvm.io), [macports](http://www.macports.org), and system ruby **be sure to set in user settings**
* [Ruby gem PG](https://rubygems.org/gems/pg) `gem install pg`
* [pgTAP](http://pgtap.org) for pgTAP testing

## How to install on a Mac

1. install [rvm](https://rvm.io)<br>
  `gpg --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3`
`\curl -sSL https://get.rvm.io | bash -s stable`
2. install ruby in rvm<br>
`rvm install 2.1.5`
3. [install postgresql app](http://postgresapp.com)
4. use header from postgresql app with rvm ruby to install `gem pg`<br>
  `gem install pg -- --with-pg-include='/Applications/Postgres.app/Contents/Versions/9.4/include/' --with-pg-config=/Applications/Postgres.app/Contents/Versions/9.4/bin/pg_config`
5. install [sublime](http://www.sublimetext.com/3) *if needed*
6. install [package manager](https://packagecontrol.io/installation) *if needed*
7. run the following to install Xcode command line tools *if needed*<br>
  `xcode-select --install`
8. clone repo for pfe <br>
  `git clone https://github.com/danmanstx/pfe.git`
9. before closing sublime add `pfe` to your `installed packages` located here:<br>
  `Sublime text --> Preferences --> Package Settings --> Package Control --> Settings - User`

**COMING SOON** install with [Package Control](http://wbond.net/sublime_packages/package_control)

## Options

Sample options below.

Go to `Preferences` -> `Package Settings` -> `Postgresql Function Editor`->`Settings - User` and add this to the file or copy and edit from `Settings - Default` :

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
* Quick Switching Inspired by [Ruby Test](https://github.com/maltize/sublime-text-2-ruby-tests).

## Copyright and license

Copyright © 2014 Danny Peters, @[danmanstx](http://twitter.com/danmanstx)

Licensed under the [**GNU GPL**](https://gnu.org/licenses/gpl.html) license.