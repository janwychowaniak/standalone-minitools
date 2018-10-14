using Gee;


const string 	DATA_FILE_NAME 		= "data.txt";
const string 	DATA_FILE_BACKUP 	= DATA_FILE_NAME+".backup";
const string 	passed_char 		= "!";
const string 	to_pass_char 		= ".";
const int 		total_display_width = 120;



extern int days_between (int end_year, int end_month, int end_day, int start_year, int start_month, int start_day);
extern int days_from_now(int year, int month, int day);

extern int get_current_year ();
extern int get_current_month ();
extern int get_current_day ();

const int		DATE_ERR_CODE		= -65536;		// odpowiednik define'a z date_operations.c
													// TODO - ostatecznie nie uzyty po tej stronie. zakladam, ze biblioteka "time.h" sobie zawsze poradzi.

public int main(string[] args) {
	bool 	d_flag 		= false,
			l_flag 		= false,
			a_flag 		= false;
	string	d_val_str	= null;
	int		d_val		= 0;
	string	a_str_date	= null,
			a_str_text	= null;
			
	bool	had_switch	= false;
	
	int i,n;
	for(i=n=1; i<args.length; i=n)
	{
		if (had_switch) break;
		n++;
		if (args[i].has_prefix("-") && args[i].length>1)	// jesli napotkano przelacznik
		{
			had_switch = true;	// dopuszcza podanie tylko jednego prelacznika
			switch(args[i].get_char(1))		// jaki to dokladnie?
			{
				default : 	stderr.printf("Invalid option: %s\n", args[i]); return 1;
				case 'l':	l_flag = true; break;
				case 'd':
					if ((d_val_str = args[n++]) == null) {	// d_val_str = wartosc podana po -d
						stderr.printf("Missing argument to -d option.\n");
						return 1;
					}
					d_val = d_val_str.to_int();
					if (d_val <= 0) {	// to lapie przypadek, gdy po -d podano glupote
						stderr.printf("Invalid d_val, must be greater than 0.\n");
						return 1;
					}
					d_flag = true;
					break;
				case 'a':
					if (((a_str_text = args[n+1]) == null) || a_str_text.has_prefix("-")) {
						// drugi arg nieobecny lub bedacy przelacznikiem
						stderr.printf("Missing second argument to -a option.\n");
						return 1;
					}
					if ((args[n]) == null) {
						// pierwszy arg nieobecny
						stderr.printf("Missing first argument to -a option.\n");
						return 1;
					}
					a_str_date = args[n];
					n+=2;
					a_flag = true;
					break;
			}
		}
	}
	
	if (!(d_flag || l_flag || a_flag)) {
		usage();
		return 0;
	}
	
	// na tym etapie "d_val" i "a_str_text" zwalidowane, "a_str_date" wymaga walidacji

	Celownik.Date arg_date = {0, 0, 0};
	if (a_flag) {
		try {
			arg_date = validate_date(a_str_date);
		} catch (Celownik.DateError de) {
			stderr.printf ("Celownik.DateError: %s\n", de.message);
			return 1;
		}
	}

	var argsCarrier = new Celownik.ArgsCarrier();
	argsCarrier.l_flag 		= l_flag;
	argsCarrier.d_flag 		= d_flag;
	argsCarrier.d_val 		= d_val;
	argsCarrier.a_flag 		= a_flag;
	argsCarrier.a_str_date 	= a_str_date;
	argsCarrier.a_date 		= arg_date;
	argsCarrier.a_str_text 	= a_str_text;
	
	// wszystko zwalidowane, co tylko jest w uzyciu
	
	if (a_flag && !is_in_future(arg_date)) {
		stderr.printf("Argument date not (enough;)) in future: %s.\n", a_str_date);
		return 1;
	}
	
	try {
		what_next(argsCarrier);
	} catch (Celownik.Aborter a) {
		stderr.printf ("Celownik.Aborter: %s\n", a.message);
		return 1;
	}
	

	return 0;
}


errordomain Celownik.Aborter {
	READ_FILE_PROBLEM,
	WRITE_FILE_PROBLEM,
	DATA_FORMAT_PROBLEM,
	BACKUP_FILE_PROBLEM
}


bool is_in_future(Celownik.Date arg_date) {
	return days_from_now(arg_date.year, arg_date.month, arg_date.day) > 0;
}

void what_next(Celownik.ArgsCarrier argsCarrier) throws Celownik.Aborter {
	var lines = new ArrayList<string> ();
	
	stdout.printf("Reading data file ... ");
	try {
		lines = read_file_contents(DATA_FILE_NAME);
	} catch (Celownik.FileError e) {
		stdout.printf("fail.\n");
		stderr.printf ("Celownik.FileError: %s\n", e.message);
		throw new Celownik.Aborter.READ_FILE_PROBLEM("Celownik.Aborter.READ_FILE_PROBLEM - '%s' ... Terminating.", 
			DATA_FILE_NAME);
	} catch (Error e) {
		stdout.printf("fail.\n");
		stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
		throw new Celownik.Aborter.READ_FILE_PROBLEM("Celownik.Aborter.READ_FILE_PROBLEM - '%s' ... Terminating.",
			DATA_FILE_NAME);
	}
	stdout.printf("done.\n");
	
	
	if (argsCarrier.d_flag) 
	{
		try {
			backup_data_file(DATA_FILE_BACKUP, DATA_FILE_NAME);
		} catch (Celownik.FileError e) {
			stderr.printf ("Celownik.FileError.COPY_FAIL: %s\n", e.message);
			throw new Celownik.Aborter.BACKUP_FILE_PROBLEM("Celownik.Aborter.BACKUP_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		} catch (Error e) {
			stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
			throw new Celownik.Aborter.BACKUP_FILE_PROBLEM("Celownik.Aborter.BACKUP_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		}

		stdout.printf("Deleting record ... ");
		if (argsCarrier.d_val > lines.size) {
			stdout.printf("fail, no record of such number.\n");	
			return;
		}
		lines.remove_at(argsCarrier.d_val-1);

		try {
			write_to_file(DATA_FILE_NAME, lines);
		} catch (Celownik.FileError e) {
			if (e is Celownik.FileError.NO_FILE_CREATED) {
				stderr.printf ("Celownik.FileError.NO_FILE_CREATED: %s\n", e.message);
			} else if (e is Celownik.FileError.CLOSE_PROBLEM) {
				stderr.printf ("Celownik.FileError.CLOSE_PROBLEM: %s\n", e.message);
			}
			throw new Celownik.Aborter.WRITE_FILE_PROBLEM("Celownik.Aborter.WRITE_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		} catch (Error e) {
			stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
			throw new Celownik.Aborter.WRITE_FILE_PROBLEM("Celownik.Aborter.WRITE_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		}
		stdout.printf("done.\n");
	} 
	else if (argsCarrier.l_flag) 
	{
		stdout.printf("Generating records ... ");
		ArrayList<Celownik.Record?> records = null;
		try {
			records = compose_records(lines);
		} catch (Celownik.DateError de) {
			stdout.printf("fail.\n");
			stderr.printf ("Celownik.DateError: %s\n", de.message);
			throw new Celownik.Aborter.DATA_FORMAT_PROBLEM("Celownik.Aborter.DATA_FORMAT_PROBLEM - by '%s' ... Terminating.",
				DATA_FILE_NAME);
		}
		stdout.printf("done.\n");
		list_records(records);
	}
	else if (argsCarrier.a_flag) // w sumie podobny kod, jak dla przypadku "argsCarrier.d_flag", mozna by wyekstraktowac.
	{
		try {
			backup_data_file(DATA_FILE_BACKUP, DATA_FILE_NAME);
		} catch (Celownik.FileError e) {
			stderr.printf ("Celownik.FileError.COPY_FAIL: %s\n", e.message);
			throw new Celownik.Aborter.BACKUP_FILE_PROBLEM("Celownik.Aborter.BACKUP_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		} catch (Error e) {
			stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
			throw new Celownik.Aborter.BACKUP_FILE_PROBLEM("Celownik.Aborter.BACKUP_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		}
		
		stdout.printf("Adding record ... ");
		int y = get_current_year(),
			m = get_current_month(),
			d = get_current_day();
		string current_date = 	y.to_string()+"-"+
								((m<10)?("0"+m.to_string()):(m.to_string()))+"-"+
								((d<10)?("0"+d.to_string()):(d.to_string()));
		string new_line = 	current_date +" "+ 
							argsCarrier.a_str_date +" "+ 
							argsCarrier.a_str_text;
		lines.add(new_line);

		try {
			write_to_file(DATA_FILE_NAME, lines);
		} catch (Celownik.FileError e) {
			if (e is Celownik.FileError.NO_FILE_CREATED) {
				stderr.printf ("Celownik.FileError.NO_FILE_CREATED: %s\n", e.message);
			} else if (e is Celownik.FileError.CLOSE_PROBLEM) {
				stderr.printf ("Celownik.FileError.CLOSE_PROBLEM: %s\n", e.message);
			}
			throw new Celownik.Aborter.WRITE_FILE_PROBLEM("Celownik.Aborter.WRITE_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		} catch (Error e) {
			stderr.printf ("Error (not Celownik.FileError): %s\n", e.message);
			throw new Celownik.Aborter.WRITE_FILE_PROBLEM("Celownik.Aborter.WRITE_FILE_PROBLEM - '%s' ... Terminating.", 
				DATA_FILE_NAME);
		}
		stdout.printf("done.\n");
	}
	
}

/* Parsuje linie z pliku danych, tworzac rekordy */
ArrayList<Celownik.Record?> compose_records(ArrayList<string> lines) throws Celownik.DateError {
	var records	= new ArrayList<Celownik.Record?> ();
	foreach (string line in lines) {
		Celownik.Record record = {null, null, null, 0, 0, 0, 0, 0, 0};
		record = parse_line(line);
		records.add(record);
	}
	return records;
}
