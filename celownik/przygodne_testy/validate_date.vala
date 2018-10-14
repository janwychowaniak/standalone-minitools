    
public int main(string[] args) {
    Celownik.Date date = {0, 0, 0};
    try {
	    date = validate_time("2004-11-04");
	} catch (Celownik.DateError e) {
	    stdout.printf("Error: %s\n", e.message);
	}
	stdout.printf("year = %d, month = %d, day = %d\n", date.year, date.month, date.day);

    return 0;
}


errordomain Celownik.DateError {
	BAD_LENGTH,
	BAD_FORMAT,
	BAD_CHARS,
	BAD_RANGES
}

Celownik.Date validate_time(string date_str) throws Celownik.DateError
{
	if (date_str.length != 10)
		throw new Celownik.DateError.BAD_LENGTH("Bad date string length.");
	if (date_str[4] != '-' || date_str[7] != '-')
		throw new Celownik.DateError.BAD_FORMAT("Bad date string format.");
	
	int year 	= date_str[0:4].to_int(), 
		month 	= date_str[5:7].to_int(), 
		day 	= date_str[8:10].to_int();
	
	if (year < 1000 || year > 9999) 
		throw new Celownik.DateError.BAD_RANGES("Bad year range.");
	if (month < 1 || month > 12) 
		throw new Celownik.DateError.BAD_RANGES("Bad month range.");
	if (day < 1 || day > 31) 
		throw new Celownik.DateError.BAD_RANGES("Bad day range.");
	
	return { year, month, day };
}


struct Celownik.Date {
	public int year;
	public int month;
	public int day;
}
