require_relative 'function_editor'

host = ARGF.argv[0] || 'localhost'
database = ARGF.argv[1] || 'cdmdata3'
port = ARGF.argv[2] || '5432'
user = ARGF.argv[3] || 'postgres'
file = ARGF.argv[4].gsub(' ', '\\ ')

save_function(host, database, port, user, file)
