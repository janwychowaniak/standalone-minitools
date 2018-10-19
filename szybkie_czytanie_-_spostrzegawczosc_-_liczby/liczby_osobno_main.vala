
int	liczba_cyfr		 = 0;
int	dlugosc_wierszy	 = 0;
	
string generate_err_mrg(string arg) {
	string err_msg = "\t" + arg + " <liczba_cyfr> <dlugosc wiersza>";
	return err_msg;
}

/*
 * shufflowanie cyfr
 */ 
int zmiania_liczby_1 (int liczba_wzorcowa) {
	string	 liczba_string			 = liczba_wzorcowa.to_string();
	int		 liczba_cyfr			 = (int)liczba_string.length;
	bool[]	 miejsca_zuzyte_stara	 = {};
	bool[]	 miejsca_zajete_nowa	 = {};
	for (int i=0; i<liczba_cyfr; i++) {
		miejsca_zuzyte_stara += false;
		miejsca_zajete_nowa	 += false;
	}
	string[] nowa_string_arr		 = new string[liczba_cyfr];
	bool	 koniec					 = false;
	var		 local_gen				 = new SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand();
	
	while (!koniec) {
		int brana_cyfra_indeks = -1;
		do { brana_cyfra_indeks = local_gen.get_0toX_number(liczba_cyfr-1); } while (miejsca_zuzyte_stara[brana_cyfra_indeks]);
		miejsca_zuzyte_stara[brana_cyfra_indeks] = true;
		int nowe_miejsce_indeks = -1;
		do { nowe_miejsce_indeks = local_gen.get_0toX_number(liczba_cyfr-1); } while (miejsca_zajete_nowa[nowe_miejsce_indeks]);
		miejsca_zajete_nowa[nowe_miejsce_indeks] = true;
		nowa_string_arr[nowe_miejsce_indeks] = liczba_string[brana_cyfra_indeks:brana_cyfra_indeks+1];
		
		bool czy_koniec = true;
		foreach (bool miejsce in miejsca_zuzyte_stara) {
			czy_koniec = czy_koniec && miejsce;
		}
		if (czy_koniec) { koniec = true; }
	}
	string nowa_string = "";
	foreach (string cyfra in nowa_string_arr) { nowa_string += cyfra; }
	
	return nowa_string.to_int();
}

/*
 * zmiana wartosci losowej cyfry
 */ 
int zmiania_liczby_2 (int liczba_wzorcowa) {
	string	 liczba_string			 = liczba_wzorcowa.to_string();
	int		 liczba_cyfr			 = (int)liczba_string.length;
	var		 local_gen				 = new SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand();
	int		 cyfra_do_podm_indeks	 = local_gen.get_0toX_number(liczba_cyfr-1);
	int		 cyfra_do_podm_wartosc	 = local_gen.get_0toX_number(9);
	
	string nowa_string = liczba_string[0:cyfra_do_podm_indeks] + cyfra_do_podm_wartosc.to_string() + liczba_string[cyfra_do_podm_indeks+1:liczba_cyfr];
	return nowa_string.to_int();
}

/*
 * shuffling i zmiana jednej cyfry
 */
int zmiania_liczby_3 (int liczba_wzorcowa) {
	return zmiania_liczby_2(zmiania_liczby_1(liczba_wzorcowa));
}

/*
 * zmiana dwoch cyfr (moga sie nakladac, co nie przeszkadza)
 */
int zmiania_liczby_4 (int liczba_wzorcowa) {
	return zmiania_liczby_2(zmiania_liczby_2(liczba_wzorcowa));
}

void wyswietl_listy(SzybkCzyt.Spostrzeg.LiczbyOsobno.ListyWynikowe listy) {
	stdout.printf("%d\n\n", listy.liczba_wzorcowa_dla_list);
    foreach (int liczba in listy.lista_1) {
		stdout.printf("%d\t", liczba);
	}
	stdout.printf("\n\n");
    foreach (int liczba in listy.lista_2) {
		stdout.printf("%d\t", liczba);
	}
	stdout.printf("\n\n");
    foreach (int liczba in listy.lista_3) {
		stdout.printf("%d\t", liczba);
	}
	stdout.printf("\n\n\n");
}




public static int main(string[] args) {
	
	if (args.length != 3) {
		stderr.printf("%s\n\n", generate_err_mrg(args[0]));
		return -1;
	}
	liczba_cyfr		 = args[1].to_int();
	dlugosc_wierszy	 = args[2].to_int();
	if (liczba_cyfr*dlugosc_wierszy==0) {
		stderr.printf("\t*** Ktorys z argumentow nieprawidlowy.\n");
		return -1;
	}
	liczba_cyfr 	= (liczba_cyfr>=3)?(liczba_cyfr):(3);
	liczba_cyfr 	= (liczba_cyfr<=5)?(liczba_cyfr):(5);
	dlugosc_wierszy = (dlugosc_wierszy>=10)?(dlugosc_wierszy):(10);
	
	var gen = new SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRand();

	
	int liczba_wzorcowa = 0;
	switch (liczba_cyfr) {
		case 3:
			liczba_wzorcowa = gen.get_number(100, 999);
			break;
		case 4:
			liczba_wzorcowa = gen.get_number(1000, 9999);
			break;
		case 5:
			liczba_wzorcowa = gen.get_number(10000, 99999);
			break;
	}
	
	var gruposz = new SzybkCzyt.Spostrzeg.LiczbyOsobno.Grupowacz(liczba_wzorcowa, dlugosc_wierszy);
	wyswietl_listy(gruposz.generuj_listy());
	
	return 0;
}
