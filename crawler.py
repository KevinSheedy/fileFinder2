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
	
def dbg():
	root_path = "C:/dev"
	walker = os.walk(root_path)
	i = 0
	
	for current_dirpath, dirnames, filenames in walker:
		print current_dirpath
		print dirnames
		print filenames
		i+=1
		if i > 1:
			print "return####################################################################"
			return walker
	
#walker = dbg()
#for current_dirpath, dirnames, filenames in walker:
#	print current_dirpath
#	print dirnames
#	print filenames

#path = os.path.abspath("C://dev///html")
#print path
#os_walk("C:/dev", "html/jsonDropdowns")

def get_os_walker(root_path, start_point_rel_path):
	root_path         = os.path.abspath(root_path)
	search_path       = os.path.join(root_path, start_point_rel_path)
	search_path       = os.path.abspath(search_path)
	search_path_array = get_path_array(search_path, root_path)
	
	print "search_path_array:", search_path_array
	
	walker = os.walk(root_path)
	for current_dirpath, dirnames, filenames in walker:
		
		# Bottomed out
		if len(dirnames) == 0:
			return walker
		
		current_path_array = get_path_array(current_dirpath, root_path)
		print "current_path_array:", current_path_array
		
		depth = len(current_path_array)
		print "depth:", depth
		
		if depth >= len(search_path_array):
			return walker
		
		search_folder = search_path_array[depth]
		print "search_folder:" + search_folder
		i = 0
	
		for dirname in list(dirnames):
			print "compare", search_folder, dirname
			#Found the folder
			if dirname.lower() == search_folder:
				print "found folder"
				if depth == (len(search_path_array) - 1):
					print "return walker"
					return walker
				break
			if dirname.lower() > search_folder:
				print "passed folder", dirname, search_folder
				return walker
			dirnames.remove(dirname)
				
def get_path_array(path, base_path):
	path      = os.path.abspath(path).lower()
	base_path = os.path.abspath(base_path).lower()
	rel_path  = path[len(base_path) + 1:]
	
	if rel_path == "":
		return []
	
	path_array = rel_path.split("\\")
	
	return path_array
				
walker = get_os_walker("C:/dev", "html/jsonDropdown")

print "got walker"
for current_dirpath, dirnames, filenames in walker:
	print current_dirpath, dirnames


#print get_path_array("C:////dev/\\aardvark/apple/", "C:\dev")