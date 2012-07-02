import os
import data_layer
import sqlite3

def main():

	conn = data_layer.get_connection('test.db')
	root_dir = 'C:/dev/Markup/Markup_Demo/'
	set_filenames = set()
	
	#list_path_arrays = get_tree_segment_paths(conn, root_dir, "MarkupEJB/ejbModule/aib/")
	list_path_arrays = get_tree_segment_paths(conn, "C:/", "")
	
	for path_array in list_path_arrays:
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
	return path.rsplit("/")

def get_tree_segment_paths(conn, repo_path, tree_segment_rel_path):
	
	tree_segment_rel_path_array = path_to_folder_array(tree_segment_rel_path)
	tree_segment_depth = len(tree_segment_rel_path_array)
	tree_segment_root_path = repo_path + tree_segment_rel_path
	list_path_arrays = []
	
	print tree_segment_root_path
	
	for current_dirpath, dirnames, filenames in os.walk(tree_segment_root_path):
	
		print current_dirpath
		
		current_file_rel_path       = abs_path_to_rel_path(repo_path, current_dirpath)
		current_file_rel_path_array = path_to_folder_array(current_file_rel_path)
		list_path_arrays.append(current_file_rel_path_array)
		depth_within_tree_segment = len(current_file_rel_path_array) - tree_segment_depth
		
		# Don't go any more than 3 folders deep
		if depth_within_tree_segment >= 3:
			# This stops the walk from going deeper
			del dirnames[:]
	
	return list_path_arrays
	
def get_batch_of_paths(root_path, starting_path):
	pass
	
def os_walk(root_path, start_point_rel_path):
	
	walker = os.walk(root_path)
	
	for current_dirpath, dirnames, filenames in walker:
		current_rel_path = abs_path_to_rel_path(root_path, current_dirpath)
		current_rel_path_array = path_to_folder_array(current_rel_path)
		start_point_rel_path_array = path_to_folder_array(start_point_rel_path)
		print current_dirpath
		print current_rel_path_array
		print start_point_rel_path_array
	
	

os_walk("C:/dev", "html/jsonDropdowns")