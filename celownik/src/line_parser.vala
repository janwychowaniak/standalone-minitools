// klasa nie sprawdza poprawnosci danych z pliku, bo zaklada,
// ze nie bedzie on modyfikowany recznie, a program umie sobie
// wygenerowac plik poprawnie


Celownik.Record parse_line (string line) throws Celownik.DateError {
	string[] tokens 		= line.split(" ");
	string[] text_tokens 	= tokens[2:tokens.length];
	string   text_str		= string.joinv(" ", text_tokens);
	
	Celownik.Date local_start_date 	= validate_date(tokens[0]);
	Celownik.Date local_end_date 	= validate_date(tokens[1]);
	
	return Celownik.Record() {	start_date_str 	= tokens[0], 
								end_date_str   	= tokens[1], 
								text			= text_str,
								start_date_year = local_start_date.year, 
								start_date_month= local_start_date.month, 
								start_date_day	= local_start_date.day, 
								end_date_year	= local_end_date.year,
								end_date_month	= local_end_date.month,
								end_date_day	= local_end_date.day
							 };
}
