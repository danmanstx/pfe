import sublime, sublime_plugin, os, os.path

SETTINGS_FILE = 'postgresql_function_editor.sublime-settings'
pfe_settings = None

def plugin_loaded():
  global pfe_settings,ruby_manager,ruby_cmd,ruby_files_dir
  pfe_settings = sublime.load_settings(SETTINGS_FILE)
  ruby_manager = pfe_settings.get('ruby_manager', '')

  if ruby_manager == 'rvm':
    ruby_cmd = "~/.rvm/bin/rvm-auto-ruby ";
  elif ruby_manager == 'port':
    ruby_cmd = '/opt/local/bin/ruby ';
  else:
    ruby_cmd = '/usr/bin/ruby ';

  ruby_files_dir = sublime.packages_path() + "/pfe/ruby/source/"

class LoadDatabaseFunctionsCommand(sublime_plugin.WindowCommand):
  def run(self):
    ruby_file = "'"+ ruby_files_dir + "create_schema_folders.rb'"
    cmd_str = ruby_cmd + ruby_file  + ' ' + pfe_settings.get('host') + ' ' + pfe_settings.get('database')
    cmd_str = cmd_str + ' ' + pfe_settings.get('port') + ' ' + pfe_settings.get('user')
    output = os.popen(cmd_str).read()
    dir=pfe_settings.get("tmp_folder", "/tmp/postgresFunctions")
    subdir= [os.path.join(dir,o) for o in os.listdir(dir) if os.path.isdir(os.path.join(dir,o))]
    project_data = {'folders': []}
    for dir in subdir:
        project_data['folders'].append({'path': dir})
    self.window.set_project_data(project_data)
    self.window.run_command("refresh_folder_list")
    sublime.message_dialog(str(output))

class SaveDatabaseFunctionCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    ruby_file = "'"+ ruby_files_dir + "save_database_function.rb'"
    cmd_str = ruby_cmd + ruby_file + ' ' + pfe_settings.get('host')
    cmd_str = cmd_str + ' ' + pfe_settings.get('database') + ' ' + pfe_settings.get('port') + ' ' + pfe_settings.get('user')
    cmd_str = cmd_str + ' ' + sublime.active_window().active_view().file_name().replace(" ","\\ ")
    cmd_out = os.popen(cmd_str).read()
    self.output_view = self.window.get_output_panel("textarea")
    self.output_view.settings().set("color_scheme", "Packages/pfe/color.tmTheme")
    self.output_view.set_syntax_file("Packages/pfe/scheme.tmLanguage")
    self.window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": "using " + pfe_settings.get('database')+ " on "+ pfe_settings.get('host')})
    self.output_view.run_command("append", {"characters": "\nfilename: "+ sublime.active_window().active_view().file_name().split('/').pop()+ "\n\n"})
    self.output_view.run_command("append", {"characters": "RESULT:\n"})
    self.output_view.run_command("append", {"characters": cmd_out})
    self.output_view.set_read_only(True)


class runFunctionTestCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime.active_window().active_view().run_command("save")
    ruby_file = "'"+sublime.packages_path() + "/pfe/ruby/source/run_function_test.rb'"
    cmd_str = ruby_cmd + ruby_file + ' ' + pfe_settings.get('host')
    cmd_str = cmd_str + ' ' + pfe_settings.get('database') + ' ' + pfe_settings.get('port') + ' ' + pfe_settings.get('user')
    cmd_str = cmd_str + ' ' + sublime.active_window().active_view().file_name().replace(" ","\\ ")
    cmd_out = os.popen(cmd_str).read()
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

class SetRubyManagerCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("set ruby manager:",
                                  pfe_settings.get("ruby_manager"),
                                  self.on_done, None, None)

  def on_done(self, input):
    pfe_settings.set("ruby_manager", input)
    sublime.save_settings("postgresql_function_editor.sublime-settings")
