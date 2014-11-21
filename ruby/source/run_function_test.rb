require_relative 'function_editor'
require 'stringio'

host = ARGF.argv[0] || 'localhost'
database = ARGF.argv[1] || 'database'
port = ARGF.argv[2] || '5432'
user = ARGF.argv[3] || 'posgresql'
file = ARGF.argv[4].gsub(' ', '\\ ')
puts file
saved_function = save_function(host, database, port, user, file, false)
return saved_function if saved_function.include? 'ERROR'

connection = test_connection(host, database, port, user)
return connection if connection.is_a?(String)

file = file.split('/').pop(2)
schema = file[0]
test = file[1].split('.').first

puts run_single_test(connection, schema, test)
