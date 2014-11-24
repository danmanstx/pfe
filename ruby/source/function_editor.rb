require 'pg'
require 'fileutils'

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
  PG::Connection.open(dbname: database, host: host, port: port, user: user)
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
  connection = test_connection(host, database, port, user)
  return connection if connection.is_a?(String)
  @function = create_function_string(file)

  result = connection.exec(@function)
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
  connection.exec('BEGIN;')
  result = connection.exec(function)
  connection.exec('ROLLBACK;')
  result.each { |line | results += line['runtests'].to_s + "\n" }
  return results
  rescue Exception => e
    return e
end
