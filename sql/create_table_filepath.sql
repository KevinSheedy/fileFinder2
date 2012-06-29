CREATE TABLE
	filepath
	(
		path_key text UNIQUE,
		filename_id integer,
		is_file boolean,
		FOREIGN KEY(filename_id) REFERENCES foldername(rowid)
	)