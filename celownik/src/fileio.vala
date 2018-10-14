using Gee;


//~ 	reading...
//~ 	try {
//~ 		lines = read_file_contents("data.txt");
//~ 	} catch (Celownik.FileError e) {
//~ 		stderr.printf ("Celownik.FileError: %s\n", e.message);
//~ 		return 1;
//~ 	} catch (Error e) {
//~ 		stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
//~ 		return 1;
//~ 	}
//~     
//~ 
//~ 	writing...
//~ 	try {
//~ 		write_to_file("data.txt", lines);
//~ 	} catch (Celownik.FileError e) {
//~ 		stdout.printf ("Celownik.FileError: %s\n", e.message);
//~ 		return 1;
//~ 	} catch (Error e) {
//~ 		stdout.printf ("Error (not Celownik.FileError): %s\n", e.message);
//~ 		return 1;
//~ 	}



errordomain Celownik.FileError {
	NO_FILE,
	NO_FILE_CREATED,
	CLOSE_PROBLEM,
	COPY_FAIL
}



ArrayList<string> read_file_contents (string file_name) throws Celownik.FileError, Error {
	var file 			= File.new_for_path (file_name);
	var lines			= new ArrayList<string> ();
	
    if (!file.query_exists ())
		throw new Celownik.FileError.NO_FILE("File '%s' doesn't exist.", file.get_path ());

	DataInputStream dis = null;
    try {
        dis = new DataInputStream (file.read());
        string line;
        while ((line = dis.read_line (null)) != null)
            lines.add(line);
    } finally {
        if (null != dis) try { dis.close (null); } catch { lines = null;}	// nie mam ladniejszego pomyslu na obsluge tu
    }
    if (lines == null) 
		throw new Celownik.FileError.CLOSE_PROBLEM("Stream closing problem by the '%s' file with reading.", file.get_path ());
    return lines;
}


void write_to_file (string file_name, ArrayList<string> lines_to_write) throws Celownik.FileError, Error {
	var file 					 = File.new_for_path (file_name);
	var file_stream 			 = file.replace (null, false, FileCreateFlags.NONE);
	bool failure 				 = false;
	
	if (!file.query_exists ()) 
		throw new Celownik.FileError.NO_FILE_CREATED("Failed to create '%s'.", file.get_path ());
	
	DataOutputStream data_stream = null;
	try {
		data_stream = new DataOutputStream (file_stream);
		foreach (string line in lines_to_write) {
	        data_stream.put_string(line+"\n");
	    }
	} finally {
        if (null != data_stream) try { data_stream.close (null); } catch { failure = true;}	// podobniez
    }
    if (failure) 
		throw new Celownik.FileError.CLOSE_PROBLEM("Stream closing problem by the '%s' file with writing.", file.get_path ());
}


void backup_data_file(string dest_name, string file_name) throws Error {
	var backup_dest  = File.new_for_path (dest_name);
	var file 		 = File.new_for_path (file_name);
	stdout.printf("Backing-up data file ... ");

    if (!file.query_exists ()) {
		stdout.printf("no file to backup.\n");
		return;
	}

    file.copy (backup_dest, FileCopyFlags.OVERWRITE);

	if (!backup_dest.query_exists ()) 
		throw new Celownik.FileError.COPY_FAIL("Failed to backup '%s'.", file.get_path ());
		
	stdout.printf("done.\n");
}
