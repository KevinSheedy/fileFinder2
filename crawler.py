import os
import data_layer
import sqlite3

def index_one_batch():

	conn = data_layer.get_connection('test.db')
	root_dir = 'C:/dev/Markup/Markup_Demo/'
	set_filenames = set()
	
	#list_path_arrays = get_tree_segment_paths(conn, root_dir, "MarkupEJB/ejbModule/aib/")
	list_paths = get_batch_of_paths(root_dir, "")
	list_path_arrays = []
	
	for path in list_paths:
		path_array = path_to_folder_array(path)
		list_path_arrays.append(path_array)
		for filename in path_array:
			set_filenames.add(filename)
	
	data_layer.append_filenames(conn, set_filenames)
	dict_filenames = data_layer.select_filenames_as_dict(conn, set_filenames)
	
	
	list_path_keys = []
	
	for path_array in list_path_arrays:
		path_key = get_path_key(path_array, dict_filenames)
		list_path_keys.append(path_key)
		print path_key
		
	print len(set_filenames)
	print len(dict_filenames)
	
	

	#for dirpath, dirnames, filenames in os.walk(root_dir):
	#	print dirpath
	#	rel_path = abs_path_to_rel_path(root_dir, dirpath)
	#	folder_array = path_to_folder_array(rel_path)
	#	set_filenames.update(folder_array)
	#
	#data_layer.append_filenames(conn, set_filenames)
	
	conn.commit();
	
def get_path_key(path_array, dict_filenames):
	path_key = ""
	filename_ids = []
	
	
	
	for filename in path_array:
		if not dict_filenames.has_key(filename):
			print "key not found"
		filename_ids.append(str(dict_filenames[filename]))
	
	for id in filename_ids:
		path_key += id
		path_key += "_"
	
	#return "".join(filename_ids)
	return path_key
		
		
def abs_path_to_rel_path(root_dir, abs_path):
	start = len(root_dir)
	end   = len(abs_path)
	rel_path = abs_path[start:end]
	rel_path = rel_path.replace("\\", "/")
	return rel_path

def path_to_folder_array(path):
	return path.rsplit("\\")

	
def get_batch_of_paths(root_path, starting_path):
	root_path = os.path.abspath(root_path)
	walker = get_os_walker(root_path, starting_path)
	batch_size = 1000
	i = 0
	batch = []
	for current_dirpath, dirnames, filenames in walker:
		
		#for dir in dirnames:
		#	path = os.path.join(current_dirpath, dir)
		#	path = os.path.abspath(path)
		#	batch.append(path)
			
		for file in filenames:
			path = os.path.join(current_dirpath, file)
			path = os.path.abspath(path)
			rel_path = path[len(root_path) + 1:]
			batch.append(rel_path)
			i+=1
			if i >= batch_size:
				return batch
		
	return batch


def get_os_walker(root_path, start_point_rel_path):
	root_path         = os.path.abspath(root_path)
	search_path       = os.path.join(root_path, start_point_rel_path)
	search_path       = os.path.abspath(search_path)
	search_path_array = get_path_array(search_path, root_path)
	
	walker = os.walk(root_path)
	for current_dirpath, dirnames, filenames in walker:
		
		# Bottomed out
		if len(dirnames) == 0:
			return walker
		
		current_path_array = get_path_array(current_dirpath, root_path)
		depth              = len(current_path_array)
		
		if depth >= len(search_path_array):
			return walker
		
		search_folder = search_path_array[depth]
	
		for dirname in list(dirnames):
		
			#Found the folder
			if dirname.lower() == search_folder:
				if depth == (len(search_path_array) - 1):
					return walker
				break
				
			#Passed the folder
			if dirname.lower() > search_folder:
				return walker
			
			#Haven't reached the folder yet
			dirnames.remove(dirname)
				
def get_path_array(path, base_path):
	path      = os.path.abspath(path).lower()
	base_path = os.path.abspath(base_path).lower()
	rel_path  = path[len(base_path) + 1:]
	
	if rel_path == "":
		return []
	
	path_array = rel_path.split("\\")
	
	return path_array
				
index_one_batch()
