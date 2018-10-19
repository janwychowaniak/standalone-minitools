using Gee;

/**
 * Bierze liczbe wzorcowa, dokonuje losowania pozycji, zamian i zwraca
 * tablice bedace wierszami do wyswietlenia na ekran.
 */ 
public class SzybkCzyt.Spostrzeg.LiczbyOsobno.Grupowacz : Object {
	
	private int liczba_wzorcowa;
	private int dlugosc_wierszy;
	private int liczba_dobrych;
	private SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand local_gen;
	
	public Grupowacz(int _liczba_wzorcowa, int _dlugosc_wierszy) {
		liczba_wzorcowa	 = _liczba_wzorcowa;
		dlugosc_wierszy	 = _dlugosc_wierszy;
		local_gen		 = new SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand();
		liczba_dobrych	 = (int)(dlugosc_wierszy/3) + (local_gen.get_0toX_number(2)-1);
	}
	
	public SzybkCzyt.Spostrzeg.LiczbyOsobno.ListyWynikowe generuj_listy() {
		var listy = SzybkCzyt.Spostrzeg.LiczbyOsobno.ListyWynikowe() {
			lista_1 = new ArrayList<int>(),
			lista_2 = new ArrayList<int>(),
			lista_3 = new ArrayList<int>(),
			liczba_wzorcowa_dla_list = liczba_wzorcowa
		};
		bool[] mapa_dobrych_lista_1 = {};
		bool[] mapa_dobrych_lista_2 = {};
		bool[] mapa_dobrych_lista_3 = {};
		for(int i=0; i<dlugosc_wierszy; i++) {
			mapa_dobrych_lista_1 += false; 
			mapa_dobrych_lista_2 += false; 
			mapa_dobrych_lista_3 += false; 
		}
		
		// moga sie nakladac. to zasadniczo nie przeszkadza.
		for(int i=0; i<liczba_dobrych; i++) {
			mapa_dobrych_lista_1[local_gen.get_0toX_number(dlugosc_wierszy-1)] = true;
			mapa_dobrych_lista_2[local_gen.get_0toX_number(dlugosc_wierszy-1)] = true;
			mapa_dobrych_lista_3[local_gen.get_0toX_number(dlugosc_wierszy-1)] = true;
		}
		
		for(int i=0; i<dlugosc_wierszy; i++) {
			if (mapa_dobrych_lista_1[i])	{ listy.lista_1.add(liczba_wzorcowa); }
			else 							{ listy.lista_1.add(zmien_liczbe()); }
			if (mapa_dobrych_lista_2[i])	{ listy.lista_2.add(liczba_wzorcowa); }
			else 							{ listy.lista_2.add(zmien_liczbe()); }
			if (mapa_dobrych_lista_3[i])	{ listy.lista_3.add(liczba_wzorcowa); }
			else 							{ listy.lista_3.add(zmien_liczbe()); }
		}
		
		return listy;
	}
	
	// -------------------------------------------------------------------------------
	
	private int zmien_liczbe() {
		switch(local_gen.get_1toX_number(4)) {
			case 1:	return zmiania_liczby_1(liczba_wzorcowa);
			case 2:	return zmiania_liczby_2(liczba_wzorcowa);
			case 3:	return zmiania_liczby_3(liczba_wzorcowa);
			case 4:	return zmiania_liczby_4(liczba_wzorcowa);
		};
		return 0;
	}
	
}
