require_relative 'function_editor'

host = ARGF.argv[0] || 'localhost'
database = ARGF.argv[1] || 'cdmdata3'
port = ARGF.argv[2] || '9566'
user = ARGF.argv[3] || 'suran_admin'
file = ARGF.argv[4].gsub(' ', '\\ ')

saved_function = save_function(host, database, port, user, file, false)
return saved_function if saved_function.include? 'ERROR'

connection = test_connection(host, database, port, user)
return connection if connection.is_a?(String)

file = file.split('/').pop(2)
schema = file[0]
test = file[1].split('.').first

function = "SELECT * FROM pgtap.runtests('#{schema}','#{test}'); "
results = ''
begin
  connection.exec('BEGIN;')
  result = connection.exec(function)
  connection.exec('ROLLBACK;')
  result.each { |line | results += line['runtests'].to_s + "\n" }
  puts results
rescue PG::SyntaxError => e
  puts e
end
