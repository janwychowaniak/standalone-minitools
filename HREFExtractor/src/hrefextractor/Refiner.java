package hrefextractor;

import java.util.ArrayList;

/**
 * Klasa operuje na liscie ArrayList<String>, majac mozliwosc wyszukania String'ow zawierajacych
 * lub nie zawierajacych podanej frazy (frazy, nie regexa).
 * @author jan
 *
 */
public class Refiner {

	private ArrayList<String> linksList;
	private final String filterPattern;
	private final String excludePattern;

	/**
	 * @param linksList			Lista do przeszukania
	 * @param filterPattern		fraza, ktora wynik wyszukiwania ma zawierac
	 * @param excludePattern	fraza, ktorej wynik wyszukiwania ma nie zawierac
	 */
	public Refiner(ArrayList<String> linksList, String filterPattern, String excludePattern) {
		this.linksList = linksList;
		this.filterPattern = filterPattern;
		this.excludePattern = excludePattern;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<String> testlinks = new ArrayList<String>();
		testlinks.add("about:blank?favicon.gif");
		testlinks.add("www.google.pl");
		testlinks.add("http://oaoao?a7%a$=s@d=!f-&6-87=6-a8/");
		testlinks.add("http://niebezpiecznik.pl/podeslij-newsa/");
		testlinks.add("http://niebezpiecznik.pl/info/");
		testlinks.add("http://niebezpiecznik.pl/kontakt/");
		
		Refiner refiner = new Refiner(testlinks, "pl", "nik");
		ArrayList<String> filtered = refiner.filter();
		ArrayList<String> excluded = refiner.exclude();
		ArrayList<String> refined = refiner.refine();
		
		if (filtered != null) {
			System.out.println("Filtered:");
			for (String link : filtered) {
				System.out.println(link);
			}
			System.out.println();
		}

		if (excluded != null) {
			System.out.println("Excluded:");
			for (String link : excluded) {
				System.out.println(link);
			}
			System.out.println();
		}
		
		if (refined != null) {
			System.out.println("Refined:");
			for (String link : refined) {
				System.out.println(link);
			}
		}
	}

	/**
	 * Ma za zadanie wyfiltrowac linki zawierajace podana fraze, a z nich potem wyrzucic te,
	 * ktore zawieraja druga podana fraze. Patterny dla filtrowania i wylaczania moga byc null'ami,
	 * wowczas dany etap jest pomijany.
	 * @return	ArrayList<String> z ewentualnie wyfiltrowanymi lub/i wylaczonymi linijkami,
	 * tudziez null, jesli odpadna wszystkie
	 */
	public ArrayList<String> refine() {
		if (filterPattern != null) 	linksList = filter();
		if (linksList == null) return null;
		if (excludePattern != null) linksList = exclude();
		return linksList;
	}

	/**
	 * @return	ArrayList<String> elementow nie zawierajacych podanej frazy, lub null, jesli takowych nie stwierdzono
	 */
	private ArrayList<String> exclude() {
		ArrayList<String> excludedList = new ArrayList<String>();
		for (String link : linksList) {
			if (!link.contains(excludePattern)) excludedList.add(link);
		}
		
		if (excludedList.isEmpty()) excludedList = null;
		return excludedList;
	}

	/**
	 * @return	ArrayList<String> elementow zawierajacych podana fraze, lub null, jesli takowych nie stwierdzono
	 */
	private ArrayList<String> filter() {
		ArrayList<String> filteredList = new ArrayList<String>();
		for (String link : linksList) {
			if (link.contains(filterPattern)) filteredList.add(link);
		}
		
		if (filteredList.isEmpty()) filteredList = null;
		return filteredList;
	}

}
