using Gee;


void list_records(ArrayList<Celownik.Record?> records) {
	int number = 0;
	
	stdout.printf("\n");
	foreach (Celownik.Record record in records) {
		number++;
		string entire_record_display = "";
		// header
		string header = @"@:$number";
		entire_record_display += header;
		entire_record_display += "\n";
		// cel
		string cel_text = record.text;
		entire_record_display += cel_text;
		entire_record_display += "\n";
		// dates
		string dates_row = record.start_date_str;
		dates_row += get_spaces(total_display_width-2*record.start_date_str.length);
		dates_row += record.end_date_str;
		entire_record_display += dates_row;
		entire_record_display += "\n";
		// time bar
		int duration  = days_between( record.end_date_year,   record.end_date_month,   record.end_date_day, 
									  record.start_date_year, record.start_date_month, record.start_date_day);
		int remaining = days_from_now(record.end_date_year, record.end_date_month, record.end_date_day);
		int timebar_length = total_display_width-4;
		int to_pass_chars_amount = (int)(timebar_length*(double)remaining/(double)duration);
		int passed_chars_amount = timebar_length - (int)(timebar_length*(double)remaining/(double)duration);
		string timebar = "[ ";
		timebar += get_chars(passed_char, passed_chars_amount);
		timebar += get_chars(to_pass_char, to_pass_chars_amount);
		timebar += " ]";
		entire_record_display += timebar;
		entire_record_display += "\n";
		// dur/rem
		string dur_str = @"Duration: $duration";
		string rem_str = @"Remaining: $remaining";
		string dur_rem_row = "";
		dur_rem_row += dur_str;
		dur_rem_row += get_spaces(total_display_width-dur_str.length-rem_str.length);
		dur_rem_row += rem_str;
		entire_record_display += dur_rem_row;
		entire_record_display += "\n";
		
		// print
		stdout.printf("%s\n", entire_record_display);
	}
}

string get_spaces(int how_much) {
	string spaces = "";
	for(int i=0; i<how_much; i++)
		spaces += " ";
	return spaces;
}

string get_chars(string what, int how_much) {
	string chars = "";
	for(int i=0; i<how_much; i++)
		chars += what;
	return chars;
}
