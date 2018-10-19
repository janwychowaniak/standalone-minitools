
/**
 * W miare elegancki wrapper na funkcje generujaca liczbe naturalna z
 * zadanego zakresu.
 */ 
public class SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand : Object {
	
	/**
	 * Nie rzuca zadnych wyjatkow, zwraca -1 jako kod bledow.
	 */
    public int get_number(uint range_limit_min, uint range_limit_max) {
		int err_code = -1;
		if (range_limit_min < 0)				{ return err_code; }
		if (range_limit_max < 1)				{ return err_code; }
		if (range_limit_max < range_limit_min)	{ return err_code; }
		return Random.int_range ((int32)range_limit_min, (int32)range_limit_max + 1); // int_range zwraca tez "int32"
	}
	
	public int get_1toX_number(uint upper_bound) {
		return get_number(1, upper_bound);
	}
	
	public int get_0toX_number(uint upper_bound) {
		return get_number(1, upper_bound+1) - 1;
	}
	
}
