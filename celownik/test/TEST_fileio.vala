using Gee;

int main () {
	try {
		backup_data_file("data.txt.backup", "data.txt");
	} catch (Celownik.FileError e) {
		stdout.printf ("FileError.COPY_FAIL: %s\n", e.message);
		return 1;
	} catch (Error e) {
		stdout.printf ("Error (not Celownik.FileError): %s\n", e.message);
		return 1;
	}
//~ 	return 0;
	ArrayList<string> lines = null;
	stdout.printf ("reading...\n");
	try {
		lines = read_file_contents("data.txt");
	} catch (Celownik.FileError e) {
		if (e is Celownik.FileError.NO_FILE) {
			stdout.printf ("FileError.NO_FILE: %s\n", e.message);
		} else {
			stdout.printf ("WTF?: %s\n", e.message);
			GLib.error("GLib.error: %s\n", e.message);
		}
		return 1;
	} catch (Error e) {
		stdout.printf ("Error (not Celownik.FileError): %s\n", e.message);
		return 1;
	}
    
    foreach (string line in lines) {
        stdout.printf ("%s\n", line);
    }
    append_line(lines);

	stdout.printf ("writing...\n");
	try {
		write_to_file("data.txt", lines);
	} catch (Celownik.FileError e) {
		stdout.printf ("FileError.NO_FILE_CREATED: %s\n", e.message);
		return 1;
	} catch (Error e) {
		stdout.printf ("Error (not Celownik.FileError): %s\n", e.message);
		return 1;
	}

    return 0;
}

void append_line(ArrayList<string> to_what) {
	to_what.add("line from prog");
}


/*
errordomain Celownik.FileError {
	NO_FILE,
	NO_FILE_CREATED,
	CLOSE_PROBLEM
}

ArrayList<string> read_file_contents (string file_name) throws Celownik.FileError, Error {
	var file 			= File.new_for_path (file_name);
	var lines			= new ArrayList<string> ();
	
    if (!file.query_exists ())
		throw new Celownik.FileError.NO_FILE("File '%s' doesn't exist.\n", file.get_path ());

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
		throw new Celownik.FileError.CLOSE_PROBLEM("Stream closing problem by the '%s' file with reading.\n", file.get_path ());
    return lines;
}

void write_to_file (string file_name, ArrayList<string> lines_to_write) throws Celownik.FileError, Error {
	var file 					 = File.new_for_path (file_name);
	var file_stream 			 = file.replace (null, false, FileCreateFlags.NONE);
	bool failure 				 = false;
	
	if (!file.query_exists ()) 
		throw new Celownik.FileError.NO_FILE_CREATED("Failed to create '%s'.\n", file.get_path ());
	
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
		throw new Celownik.FileError.CLOSE_PROBLEM("Stream closing problem by the '%s' file with writing.\n", file.get_path ());
}
*/
