require 'pg'
require 'fileutils'

@host = ARGV[0] || 'localhost'
@database = ARGV[1] || 'database'
@port = ARGV[2] || '5432'
@user = ARGV[3] || 'postgresql'
@function_directory = ARGV[4] || '/tmp/postgresFunctions'
@action = ARGV[5] || 'save'
@file = ARGV[6].gsub('%^%', ' ') unless ARGV[6].nil?

def time
  start = Time.now
  yield
  puts "functions loaded\ntook #{(Time.now - start).round(4)} seconds"
end

def file_type(lang)
  case lang
  when '14' then 'sql'
  when '183355' then 'plperlu'
  else 'plpgsql'
  end
end

def volatile_type(volatile)
  case volatile
  when 's' then 'STABLE'
  when 'i' then 'IMMUTABLE'
  else 'VOLATILE'
  end
end

def test_connection(host, database, port, user)
  @connection = PGconn.open(dbname: database, host: host, port: port, user: user)
  rescue Exception => e
    puts "unable to connect\nto: #{database}\non: #{host}\nport: #{port}\n\nerror:\n\n#{e}"
end

def create_function_string(file)
  function = ''
  File.open(file, 'r') do |f|
    f.each_line do |line|
      function += line
    end
  end
  function
end

def save_function(host, database, port, user, file, use_std_out=true)
  @connection = test_connection(host, database, port, user)
  return @connection if @connection.is_a?(String)
  @function = create_function_string(file)

  result = @connection.exec(@function)
  if use_std_out
    puts result.cmd_status
  else
    return result.cmd_status
  end
  rescue Exception => e
    if use_std_out
      puts e
    else
      return e
    end
end

def run_single_test(connection, schema, test)
  function = "SELECT * FROM pgtap.runtests('#{schema}','#{test}'); "
  results = ''
  connection.set_notice_processor { |msg| results += "#{msg.to_s.split('CONTEXT:')[0]}" }
  connection.exec('BEGIN;')
  result = connection.exec(function)
  connection.exec('ROLLBACK;')
  result.each { |line| results += line['runtests'].to_s + "\n" }
  return results
  rescue Exception => e
    return e
end

def test_schema(connection, schema)
  function = "SELECT * FROM pgtap.runtests('#{schema}','^test'); "
  results = ''
  connection.set_notice_processor { |msg| results += "#{msg.to_s.split('CONTEXT:')[0]}" }
  connection.exec('BEGIN;')
  result = connection.exec(function)
  connection.exec('ROLLBACK;')
  result.each { |line| results += line['runtests'].to_s + "\n" }
  return results
  rescue Exception => e
    return e
end

case @action
when 'test'
  saved_function = save_function(@host, @database, @port, @user, @file, false)
  puts saved_function
  # return saved_function if saved_function.include? 'ERROR'

  @connection = test_connection(@host, @database, @port, @user)
  return @connection if @connection.is_a?(String)

  file = @file.split('/').pop(2)
  schema = file[0]
  test = file[1].split('.').first

  puts run_single_test(@connection, schema, test)
when 'test_schema'
  @connection = test_connection(@host, @database, @port, @user)
  return @connection if @connection.is_a?(String)

  file = @file.split('/').pop(2)
  schema = file[0]

  puts test_schema(@connection, schema)
when 'save'
 save_function(@host, @database, @port, @user, @file)

when 'create'
  time do
    FileUtils.rm_rf @function_directory if Dir.exist? @function_directory
    Dir.mkdir(@function_directory, 0755)
    Dir.chdir(@function_directory)

    @connection = test_connection(@host, @database, @port, @user)
    return @connection if @connection.is_a?(String)

    schemas = @connection.exec("SELECT schema_name FROM information_schema.schemata WHERE (schema_owner=$1 AND schema_name not in ('contrib','pgtap','pgagent')) OR schema_name='public';", [@user])
    @select = 'nspname as schema,provolatile as volatile, prosrc as body,
               proname as name,procost as cost,prolang as lang,
               pg_catalog.pg_get_function_arguments(p.oid) as args,
               pg_get_function_identity_arguments(p.oid) as drop_args,
               pg_catalog.pg_get_function_result(p.oid) as return_type'

    schemas.each { |schema| Dir.mkdir(schema['schema_name'], 0755) }

    schemas.each do |schema|
      functions = @connection.exec("SELECT #{@select} FROM pg_catalog.pg_proc p LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE  n.nspname ='#{schema['schema_name']}';")
      functions.each do |function|
        file_type = file_type(function['lang'])
        post_text = "$BODY$\nLANGUAGE '#{file_type}' #{volatile_type(function['volatile'])}\nCOST #{function['cost']};"
        Dir.chdir(@function_directory + '/' + function['schema'])
        header = "-- DROP FUNCTION IF EXISTS  #{function['schema']}.#{function['name']}(#{function['drop_args']}) CASCADE;\n\n"

        arguments_for_file_name = function['args'].slice(0,199); # There is a 260 character limit on file names. We will allocate 200 for the aguments
        arguments_for_file_name = arguments_for_file_name.gsub('/', ''); # Remove any path delimiters from the file name

        function_name_for_file_name = function['name'].slice(0,49); # There is a 260 character limit on file names. We will allocate 50 for the function name, leaving 10 for the () and .suffix
        
        function_file_name =  function_name_for_file_name + "(" + arguments_for_file_name + ")" + ".#{file_type}"
        IO.write(function_file_name , "#{header}CREATE OR REPLACE FUNCTION #{function['schema']}.#{function['name']}(#{function['args']})\nRETURNS #{function['return_type']} AS\n$BODY$" + function['body'] + post_text)
      end
    end
  end
end

