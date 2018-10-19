package hrefextractor;

import java.util.ArrayList;

/**
 * Klasa po prostu wyswietla otrzymany ArrayList<String>, linijka-per-String.
 * @author jan
 *
 */
public class ConsolePrinter {

	private static final String NO_RESULT_MSG = "Brak rezultatow.";

	/**
	 * Testy
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<String> argumenty = new ArrayList<String>();
		argumenty.add("linia 1");
		argumenty.add("linia 2");
		argumenty.add("linia 3");
		
		new ConsolePrinter().print(argumenty);
		System.out.println("-------");
		new ConsolePrinter().print(new ArrayList<String>());
		System.out.println("-------");
		new ConsolePrinter().print(null);
		System.out.println("-------");
	}

	public void print(ArrayList<String> lines) {
		if (lines == null || lines.isEmpty()) {
			System.out.println(NO_RESULT_MSG);
			return;
		}

		for (String line : lines) {
			System.out.println(line);
		}
	}

}
