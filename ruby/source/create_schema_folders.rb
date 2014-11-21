require_relative 'function_editor'

time do
  host = ARGF.argv[0] || 'localhost'
  database = ARGF.argv[1] || 'cdmdata3'
  port = ARGF.argv[2] || '5432'
  user = ARGF.argv[3] || 'postgres'
  tmp_dir = '/tmp/postgresFunctions/'

  FileUtils.rm_rf tmp_dir if Dir.exist? tmp_dir
  Dir.mkdir(tmp_dir, 0755)
  Dir.chdir(tmp_dir)

  connection = test_connection(host, database, port, user)
  return connection if connection.is_a?(String)

  schemas = connection.exec("SELECT schema_name FROM information_schema.schemata WHERE (schema_owner=$1 AND schema_name not in ('contrib','pgtap','pgagent')) OR schema_name='public';", [user])
  @select = 'nspname as schema,provolatile as volatile, prosrc as body,
             proname as name,procost as cost,prolang as lang,
             pg_catalog.pg_get_function_identity_arguments(p.oid) as args,
             pg_catalog.pg_get_function_result(p.oid) as return_type '

  schemas.each { |schema| Dir.mkdir(schema['schema_name'], 0755) }

  schemas.each do |schema|
    functions = connection.exec("SELECT #{@select} FROM pg_catalog.pg_proc p LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE  n.nspname ='#{schema['schema_name']}';")
    functions.each do |function|
      file_type = file_type(function['lang'])
      post_text = "$BODY$\nLANGUAGE '#{file_type}' #{volatile_type(function['volatile'])}\nCOST #{function['cost']};"
      Dir.chdir(tmp_dir + function['schema'])
      header = "-- DROP FUNCTION IF EXISTS  #{function['schema']}.#{function['name']}(#{function['args']}) CASCADE;\n\n"
      IO.write(function['name'] + ".#{file_type}" , "#{header}CREATE OR REPLACE FUNCTION #{function['schema']}.#{function['name']}(#{function['args']})\nRETURNS #{function['return_type']} AS\n$BODY$" + function['body'] + post_text)
    end
  end
end
