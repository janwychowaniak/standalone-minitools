using Gee;
    

public int main(string[] args) {
    test1();
    return 0;
}


void test1() {
	var lines			= new ArrayList<string> ();
	var records			= new ArrayList<Celownik.Record?> ();
	lines.add("2004-12-21 2005-03-25 Patrzac przed siebie raz dwa trzy");
	lines.add("2006-12-21 2007-03-25 Patrzac przed siebie raz dwa trzy cztery");
	
	foreach (string line in lines) {
		Celownik.Record record = {null, null, null, 0, 0, 0, 0, 0, 0};
		record = parse_line(line);
		records.add(record);
	}
	assert(records[0].start_date_str == "2004-12-21");
	assert(records[0].end_date_str == "2005-03-25");
	assert(records[0].text == "Patrzac przed siebie raz dwa trzy");
	assert(records[0].start_date_year == 2004);
	assert(records[0].start_date_month == 12);
	assert(records[0].start_date_day == 21);
	assert(records[0].end_date_year == 2005);
	assert(records[0].end_date_month == 3);
	assert(records[0].end_date_day == 25);

	assert(records[1].start_date_str == "2006-12-21");
	assert(records[1].end_date_str == "2007-03-25");
	assert(records[1].text == "Patrzac przed siebie raz dwa trzy cztery");
	assert(records[1].start_date_year == 2006);
	assert(records[1].start_date_month == 12);
	assert(records[1].start_date_day == 21);
	assert(records[1].end_date_year == 2007);
	assert(records[1].end_date_month == 3);
	assert(records[1].end_date_day == 25);
}
