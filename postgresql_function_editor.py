import sublime, sublime_plugin, os, os.path,tarfile,subprocess

SETTINGS_FILE = 'postgresql_function_editor.sublime-settings'
pfe_settings = None

def plugin_loaded():
  global pfe_settings,ruby_manager,ruby_cmd,ruby_files_dir
  pfe_settings = sublime.load_settings(SETTINGS_FILE)
  ruby_cmd = sublime.packages_path() + "/pfe/pfe-1.0.0-osx/pfe"
  if os.path.isfile(ruby_cmd):
    pass
  else:
    tar = tarfile.open(sublime.packages_path() + '/pfe/pfe-1.0.0-osx.tar.gz')
    tar.extractall(sublime.packages_path() + '/pfe/')
    tar.close()

class LoadDatabaseFunctionsCommand(sublime_plugin.WindowCommand):
  def run(self):
    dir = pfe_settings.get("function_folder", "/tmp/postgresFunctions")
    cmd_str = pfe_settings.get('host') + ' ' + pfe_settings.get('database')
    cmd_str = cmd_str + ' ' + str(pfe_settings.get('port')) + ' ' + pfe_settings.get('user') + ' ' + dir + ' create'

    process = subprocess.Popen([ruby_cmd, cmd_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    subdir = [os.path.join(dir,o) for o in os.listdir(dir) if os.path.isdir(os.path.join(dir,o))]
    project_data = {'folders': []}
    for dir in subdir:
        project_data['folders'].append({'path': dir})
    self.window.set_project_data(project_data)
    self.window.run_command("refresh_folder_list")

    sublime.message_dialog(str(output.decode('ascii')))

class SaveDatabaseFunctionCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    # ruby_file = "'"+ ruby_files_dir + "save_database_function.rb'"
    cmd_str = pfe_settings.get('host') + ' ' + pfe_settings.get('database')
    cmd_str = cmd_str + ' ' + str(pfe_settings.get('port')) + ' ' + pfe_settings.get('user') + ' "" '
    cmd_str = cmd_str + ' save ' + sublime.active_window().active_view().file_name().replace(" ","\\ ")
    process = subprocess.Popen([ruby_cmd, cmd_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    self.output_view = self.window.get_output_panel("textarea")
    self.output_view.settings().set("color_scheme", "Packages/pfe/color.tmTheme")
    self.output_view.set_syntax_file("Packages/pfe/scheme.tmLanguage")
    self.window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": "using " + pfe_settings.get('database')+ " on "+ pfe_settings.get('host')})
    self.output_view.run_command("append", {"characters": "\nfilename: "+ sublime.active_window().active_view().file_name().split('/').pop()+ "\n\n"})
    self.output_view.run_command("append", {"characters": "RESULT:\n"})
    self.output_view.run_command("append", {"characters": str(output.decode('ascii'))})
    self.output_view.set_read_only(True)

class runAllFunctionTestsCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    cmd_out = ""
    for view in sublime.active_window().views():
      if not(view.file_name().split('/').pop().startswith("test_")):
        continue
      cmd_str = pfe_settings.get('host') + ' ' + pfe_settings.get('database')
      cmd_str = cmd_str + ' ' + str(pfe_settings.get('port')) + ' ' + pfe_settings.get('user') + ' "" '
      cmd_str = cmd_str + ' test ' + view.file_name().replace(" ","\\ ")
      process = subprocess.Popen([ruby_cmd, cmd_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = process.communicate()
      cmd_out = cmd_out + str(output.decode('ascii'))
    self.output_view = self.window.get_output_panel("textarea")
    self.output_view.settings().set("color_scheme", "Packages/pfe/color.tmTheme")
    self.output_view.set_syntax_file("Packages/pfe/scheme.tmLanguage")
    self.window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": "using " + pfe_settings.get('database') + " on "+ pfe_settings.get('host')})
    self.output_view.run_command("append", {"characters": "\n\nRESULT:\n"})
    self.output_view.run_command("append", {"characters": cmd_out})
    self.output_view.set_read_only(True)

class runFunctionTestCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    cmd_out = "This is not a test."
    if sublime.active_window().active_view().file_name().split('/').pop().startswith("test_"):
      cmd_str = pfe_settings.get('host') + ' ' + pfe_settings.get('database')
      cmd_str = cmd_str + ' ' + str(pfe_settings.get('port')) + ' ' + pfe_settings.get('user') + ' "" '
      cmd_str = cmd_str + ' test ' + sublime.active_window().active_view().file_name().replace(" ","\\ ")
      process = subprocess.Popen([ruby_cmd, cmd_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = process.communicate()
      cmd_out = str(output.decode('ascii'))
    self.output_view = self.window.get_output_panel("textarea")
    self.output_view.settings().set("color_scheme", "Packages/pfe/color.tmTheme")
    self.output_view.set_syntax_file("Packages/pfe/scheme.tmLanguage")
    self.window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": "using " + pfe_settings.get('database') + " on "+ pfe_settings.get('host')})
    self.output_view.run_command("append", {"characters": "\nfilename: "+ sublime.active_window().active_view().file_name().split('/').pop()+ "\n\n"})
    self.output_view.run_command("append", {"characters": "RESULT:\n"})
    self.output_view.run_command("append", {"characters": cmd_out})
    self.output_view.set_read_only(True)

class runSchemaTestCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    cmd_out = "This is not a test."
    if sublime.active_window().active_view().file_name().split('/').pop().startswith("test_"):
      cmd_str = pfe_settings.get('host') + ' ' + pfe_settings.get('database')
      cmd_str = cmd_str + ' ' + str(pfe_settings.get('port')) + ' ' + pfe_settings.get('user') + ' "" '
      cmd_str = cmd_str + ' test_schema ' + sublime.active_window().active_view().file_name().replace(" ","\\ ")
      process = subprocess.Popen([ruby_cmd, cmd_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = process.communicate()
      cmd_out = str(output.decode('ascii'))
    self.output_view = self.window.get_output_panel("textarea")
    self.output_view.settings().set("color_scheme", "Packages/pfe/color.tmTheme")
    self.output_view.set_syntax_file("Packages/pfe/scheme.tmLanguage")
    self.window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": "using " + pfe_settings.get('database') + " on "+ pfe_settings.get('host')})
    self.output_view.run_command("append", {"characters": "\nfilename: "+ sublime.active_window().active_view().file_name().split('/').pop()+ "\n\n"})
    self.output_view.run_command("append", {"characters": "RESULT:\n"})
    self.output_view.run_command("append", {"characters": cmd_out})
    self.output_view.set_read_only(True)

class CreateNewFunctionCommand(sublime_plugin.WindowCommand):
  def run(self, should_split_view):
    pfe_settings.set('should_split_view', should_split_view)
    current_file = sublime.active_window().active_view().file_name()
    schema = sublime.active_window().active_view().file_name().split('/').pop(-2)
    file_name = sublime.active_window().active_view().file_name().split('/').pop()
    if (schema == "testing") or (schema == "public"):
        if schema == "testing":
          new_file = "../"+"public" + "/" + file_name[5:]
        else:
          new_file = "../"+"testing" + "/" + "test_" + file_name
    else:
      if(file_name.startswith("test_")):
        print(file_name)
        new_file = "../" + schema.rstrip("testing").rstrip("_") + "/" + file_name[5:]
      else:
        new_file = "../" + schema + "_testing" + "/" + "test_" + file_name

    if self.window.find_open_file(new_file):
      if should_split_view is True:
        self.split_view()
      self.window.open_file(new_file)
    else:
      self.window.show_input_panel("file_name:",
                                  new_file,
                                  self.on_done, None, None)

  def on_done(self, input):
    split_view = pfe_settings.get('should_split_view')
    if split_view is True:
      self.split_view()
    newFile = self.window.open_file(input)
    newFile.run_command("new_function_load")

  def split_view(self):
    if self.window.num_groups() == 1:
      self.window.run_command('set_layout',
                      {
                      "cols": [0.0, 0.5, 1.0],
                      "rows": [0.0, 1.0],
                      "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
                      })
    self.window.run_command('focus_group', {"group": 1})
    # self.window.run_command('move_to_group', {"group": 1})

class NewFunctionLoadCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      sublime.set_timeout(lambda: self.create_function(self.view), 10)

    def create_function(self, view):
      if not self.view.is_loading():
          if self.view.file_name().split('/').pop().split('.')[0].startswith("test_"):
            self.view.run_command('insert_test_text',{ 'filename': self.view.file_name()})
          else:
            self.view.run_command('insert_function_text',{ 'filename': self.view.file_name()})
      else:
          sublime.set_timeout(lambda: self.create_function(self.view), 10)

class InsertTestText(sublime_plugin.TextCommand):
  def run(self, edit, filename):
    if self.view.size() == 0:
      file_array = filename.split('/')
      schema = file_array[3]
      function_name = file_array[4].split('.')[0]
      function = "-- DROP FUNCTION IF EXISTS {0}.{1}() CASCADE;\n\nCREATE OR REPLACE FUNCTION {0}.{1}()\nRETURNS SETOF text AS\n$BODY$\nDECLARE\n\nBEGIN\n\n\tRETURN NEXT pgTAP.pass('dummy test');\n\nEND;\n$BODY$\nLANGUAGE 'plpgsql' VOLATILE\nCOST 100;".format(schema,function_name)
      self.view.insert(edit, 0, function)

class InsertFunctionText(sublime_plugin.TextCommand):
  def run(self, edit, filename):
    if self.view.size() == 0:
      file_array = filename.split('/')
      schema = file_array[3]
      function_name = file_array[4].split('.')[0]
      function = "-- DROP FUNCTION IF EXISTS {0}.{1}() CASCADE;\n\nCREATE OR REPLACE FUNCTION {0}.{1}()\nRETURNS void AS\n$BODY$\nDECLARE\n\nBEGIN\n\n\nEND;\n$BODY$\nLANGUAGE 'plpgsql' VOLATILE\nCOST 100;".format(schema,function_name)
      self.view.insert(edit, 0, function)

class SetDatabaseCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set database:",
                                  pfe_settings.get("database"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("database", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")

class SetHostCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set host:",
                                  pfe_settings.get("host"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("host", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")


class SetPortCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set port:",
                                  pfe_settings.get("port"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("port", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")


class SetUserCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set user:",
                                  pfe_settings.get("user"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("user", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")

class SetPasswordCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set user:",
                                  pfe_settings.get("password"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("password", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")

class GetSyntaxCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      syntax = self.view.encoding()

#
# BELOW IS FROM SUBLIME QUICK CREATE FILE, but has been modified
#

class QuickCreateFileCreatorBase(sublime_plugin.WindowCommand):
    relative_paths = []
    full_torelative_paths = {}
    rel_path_start = ''

    def doCommand(self):
        self.build_relative_paths()
        if len(self.relative_paths) == 1:
            self.selected_dir = self.relative_paths[0]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)
        elif len(self.relative_paths) > 1:
            self.move_current_directory_to_top()
            self.window.show_quick_panel(self.relative_paths, self.dir_selected)
        else:
            view = self.window.active_view()
            self.selected_dir = os.path.dirname(view.file_name())
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)

    def build_relative_paths(self):
        folders = self.window.folders()
        view = self.window.active_view()
        self.relative_paths = []
        self.full_torelative_paths = {}
        for path in folders:
            rootfolders = os.path.split(path)[-1]
            self.rel_path_start = os.path.split(path)[0]
            self.full_torelative_paths[rootfolders] = path
            self.relative_paths.append(rootfolders)


            for base, dirs, files in os.walk(path):
                for dir in dirs:
                    relative_path = os.path.relpath(os.path.join(base, dir), self.rel_path_start)
                    self.full_torelative_paths[relative_path] = os.path.join(base, dir)
                    self.relative_paths.append(relative_path)

    def move_current_directory_to_top(self):
        view = self.window.active_view()
        if view and view.file_name():
            cur_dir = os.path.relpath(os.path.dirname(view.file_name()), self.rel_path_start)
            if cur_dir in self.full_torelative_paths:
                i = self.relative_paths.index(cur_dir)
                self.relative_paths.insert(0, self.relative_paths.pop(i))
            else:
                self.relative_paths.insert(0, os.path.dirname(view.file_name()))
        return

    def dir_selected(self, selected_index):
        function_prefix = ''
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            if self.selected_dir.endswith('_testing'):
                function_prefix = 'test_'
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, function_prefix, self.file_name_input, None, None)

    def file_name_input(self, file_name):
        full_path = os.path.join(self.selected_dir, file_name)

        if os.path.lexists(full_path):
            sublime.error_message('File already exists:\n%s' % full_path)
            return
        else:
            self.create_and_open_file(full_path + '.plpgsql')

        self.window.run_command("refresh_folder_list")

    def create(self, filename):
        base, filename = os.path.split(filename)
        self.create_folder(base)

    def create_folder(self, base):
        if not os.path.exists(base):
            parent = os.path.split(base)[0]
            if not os.path.exists(parent):
                self.create_folder(parent)
            os.mkdir(base)

class QuickCreateFileCommand(QuickCreateFileCreatorBase):
    INPUT_PANEL_CAPTION = 'Function Name:'

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path):
        if not os.path.exists(path):
            self.create(path)
        newFile = self.window.open_file(path)
        newFile.run_command("new_function_load")
