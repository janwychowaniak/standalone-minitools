#include <time.h> 
 
/* struct tm z time.h:
		tm_sec		seconds after the minute	0-61*
		tm_min		minutes after the hour		0-59
		tm_hour		hours since midnight		0-23
	tm_mday		day of the month			1-31
	tm_mon		months since January		0-11
	tm_year		years since 1900	
		tm_wday		days since Sunday			0-6
		tm_yday		days since January 1		0-365
		tm_isdst	Daylight Saving Time flag
*/

#define DATE_ERR_CODE	-65536		/* taka dosc niemozliwa wartosc, musialbym prgram uruchomic 65536 dni (179.5 lat) po minieciu celu. */



/* utility. Daje ujemna liczbe dla daty "start" pozniejszej niz "end" */
int calculate_days_diff(time_t end, time_t start)
{
	return (int) difftime(end, start) / (60 * 60 * 24);
}


/* API.
 * Daje ujemna liczbe dla daty "start" pozniejszej niz "end" */
int days_between(int end_year, int end_month, int end_day, int start_year, int start_month, int start_day)
{
    struct tm end_date 			= {0,0,0, end_day   ,end_month  -1, end_year  -1900};
    struct tm start_date 		= {0,0,0, start_day ,start_month-1, start_year-1900};
    time_t    time_end_date 	= mktime(&end_date);
    time_t    time_start_date 	= mktime(&start_date);

    if ( time_start_date == (time_t)(-1) || time_end_date == (time_t)(-1))
    {
        return DATE_ERR_CODE;
    }
    return calculate_days_diff(time_end_date, time_start_date);
}


/* API. 
 * Funkcja typu "ile dni zostalo od dzis do ... (jakiejs daty przyszlej)",
 * czyli daje ujemna liczbe dla daty wczesniejszej niz dzisiejsza */
int days_from_now(int year, int month, int day)
{
    struct tm given_date 	= {0,0,0,day,month-1,year-1900};
    time_t time_given_date 	= mktime(&given_date);

    if ( time_given_date == (time_t)(-1))
    {
        return DATE_ERR_CODE;
    }
    return calculate_days_diff(time_given_date, time(NULL));
}
