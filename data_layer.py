import sqlite3

def get_connection(database_name):
	conn   = sqlite3.connect(database_name)
	if not is_database_initialised(conn):
		initialise_database(conn)
	
	return conn
	
def is_database_initialised(conn):
	for row in select(conn, "is_database_initialised"):
		numTables = row[0]
		if numTables > 0:
			return True
		else:
			return False
			
def initialise_database(conn):
	cursor = conn.cursor()
	
	create(conn, "create_table_filename")
	create(conn, "create_table_filepath")
	create(conn, "create_table_job")
	
	conn.commit()
	
def get_sql(filename):
	path = "sql/" + filename + ".sql"
	return open(path, "r").read()
	
def create(conn, query_name):
	sql = get_sql(query_name)
	cursor = conn.cursor()
	return cursor.execute(sql)
	
def select(conn, query_name, params=[]):
	sql = get_sql(query_name)
	cursor = conn.cursor()
	return cursor.execute(sql, params)
	
def insert(conn, query_name, values):
	sql = get_sql(query_name)
	cursor = conn.cursor()
	return cursor.execute(sql, values)

def insert_multiple(conn, query_name, list):
	sql = get_sql(query_name)
	cursor = conn.cursor()
	for data in list:
		cursor.execute(sql, data)
	
def delete(conn, query_name, values):
	sql = get_sql(query_name)
	cursor = conn.cursor()
	return cursor.execute(sql)

def obj_to_query_string(obj):
	if type(obj) is list:
		return list_to_query_string(obj)
	if type(obj) is set:
		return set_to_query_string(obj)
	
def list_to_query_string(list):
	return str(list)[1:-1]

def set_to_query_string(set):
	return str(set)[5:-2]
	
#############################################################################
# Business Logic from here down
#############################################################################



#############################################################################
# Filename table queries
#############################################################################

def select_filenames(conn, filenames):
	cursor = conn.cursor()
	str_filenames = obj_to_query_string(filenames)
	query = '''SELECT rowid, filename
				FROM filename
				WHERE filename IN ('''+str_filenames+''')'''
	#print query
	return cursor.execute(query).fetchall()
	
def select_filenames_as_dict(conn, filenames):
	dict = {}
	for row in select_filenames(conn, filenames):
		print row
		dict[row[1]] = row[0]
	
	return dict
	

def select_all_filenames(conn):
	cursor = conn.cursor()
	query = '''SELECT rowid, filename
				FROM filename'''
	return cursor.execute(query).fetchall()
	
def select_all_filenames_as_dict(conn):
	dict = {}
	for row in select_all_filenames(conn):
		dict[row[1]] = row[0]
	
	return dict
	
def insert_filename(conn, filename):
	cursor = conn.cursor()
	insert(conn, "insert_filename", [filename])
	#cursor.execute("INSERT into filename values('" + filename + "')")

def insert_filenames(conn, filenames):
	list_of_lists = []
	for filename in filenames:
		list_of_lists.append([filename])
		
	insert_multiple(conn, "insert_filename", list_of_lists)
	conn.commit()
	
def append_filenames(conn, filenames):
	s = set(filenames)
	rows = select_filenames(conn, filenames)
	for row in rows:
		s.remove(row[1])
	
	insert_filenames(conn, s)
	
	
#############################################################################
# Filepath table queries
#############################################################################
	
def select_filepaths(conn, filepaths):
	cursor = conn.cursor()
	str_filepaths = obj_to_query_string(filepaths)
	query = '''SELECT path_key, filename_id, is_file, rowid
				FROM filepath
				WHERE path_key IN ('''+str_filepaths+''')'''
				
	return cursor.execute(query).fetchall()
	
def select_filepaths_as_dict(conn, filepaths):
	dict = {}
	for row in select_filepaths(conn, filepaths):
		dict[row[0]] = row[1]
	
	return dict

def select_all_filepaths(conn):
	cursor = conn.cursor()
	query = '''SELECT path_key, filename_id, is_file, rowid
				FROM filepath'''
	return cursor.execute(query).fetchall()
	
def insert_filepath(conn, path_key, filename_id=None, is_file=False):
	cursor = conn.cursor()
	insert(conn, "insert_filepath", (path_key, filename_id, is_file))

def insert_filepaths(conn, filepath_rows):
	insert_multiple(conn, "insert_filepath", filepath_rows)
	conn.commit()
	
def append_filepaths(conn, filepath_rows):
	
	# Get list of paths to be inserted
	new_path_keys = set()
	for row in filepath_rows:
		path_key = row[0]
		new_path_keys.add(path_key)

	# Get the paths that already exist in the DB
	existing_path_keys = set()
	existing_rows = select_filepaths(conn, new_path_keys)
	for row in existing_rows:
		existing_path_keys.add(row[0])
	
	# Determine the rows to insert
	rows_to_append = []
	
	for row in filepath_rows:
		if not row[0] in existing_path_keys:
			rows_to_append.append(row)
	
	insert_filepaths(conn, rows_to_append)