public class Celownik.ArgsCarrier : GLib.Object {
					
	public bool 			d_flag 		{ get; set; default = false; }
	public bool 			l_flag 		{ get; set; default = false; }
	public bool 			a_flag 		{ get; set; default = false; }
	
	public int 				d_val 		{ get; set; default = 0; }
	public Celownik.Date 	a_date 		{ get; set; default = Celownik.Date() {year=0, month=0, day=0}; }	//TODO - czy to jest w koncu potrzebne do czegos?
	public string 			a_str_date 	{ get; set; default = null; }
	public string 			a_str_text 	{ get; set; default = null; }

}

