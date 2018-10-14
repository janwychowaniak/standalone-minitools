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


struct tm* local_time_tm = NULL;

/* --------------------------------------- */

/* utility. Ustawia "local_time_tm" (raz) */
void set_local_date ()
{
	if (local_time_tm != NULL) return;
    time_t time_now;

    time_now 		= time (NULL);
    local_time_tm 	= localtime (&time_now);
}

/* --------------------------------------- */

/* API */
int get_current_year ()
{
	set_local_date();
	return local_time_tm->tm_year + 1900;
}

/* API */
int get_current_month ()
{
	set_local_date();
	return local_time_tm->tm_mon + 1;
}

/* API */
int get_current_day ()
{
	set_local_date();
	return local_time_tm->tm_mday;
}

