import os
import data_layer
import sqlite3

def main():

	conn = data_layer.get_connection('test.db')
	root_dir = 'C:/dev/Markup/Markup_Demo/'
	set_filenames = set()

	for dirpath, dirnames, filenames in os.walk(root_dir):
		print dirpath
		rel_path = abs_path_to_rel_path(root_dir, dirpath)
		folder_array = path_to_folder_array(rel_path)
		set_filenames.update(folder_array)
	
	data_layer.append_filenames(conn, set_filenames)
	
	conn.commit();
		
def abs_path_to_rel_path(root_dir, abs_path):
	start = len(root_dir)
	end   = len(abs_path)
	rel_path = abs_path[start:end]
	rel_path = rel_path.replace("\\", "/")
	return rel_path

def path_to_folder_array(path):
	return path.rsplit("/")

main()