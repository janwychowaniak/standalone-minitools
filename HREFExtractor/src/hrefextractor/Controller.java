package hrefextractor;

import java.util.ArrayList;

/**
 * Klasa Controller spina ze soba wszystkie pozostale komponenty aplikacji. 
 * @author jan
 */
public class Controller {

	/**
	 * Glowny "Entry-point" programu.
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length == 0) {
			printUsage();
			return;
		}
		// input konsolowy
		CLIInputValidator cliInputValidator = new CLIInputValidator(args);
		String includesKeyword = null, excludesKeyword = null, outputFile = null, sourceFile = null;
		try {
			includesKeyword = cliInputValidator.getIncludesKeyword();
			excludesKeyword = cliInputValidator.getExcludesKeyword();
			outputFile = cliInputValidator.getOutputFileKeyword();
			sourceFile = cliInputValidator.getSourceFile();
		} catch (Exception e) {	emergencyTerminate(e);	}
		// zrobione
	
		// wczytywanie i wstepna rafinacja sourceFile'a
		ArrayList<String> rawHrefLines = null;
		try {
			rawHrefLines = new FileReader(sourceFile).getFilteredLines();
		} catch (Exception e) {	emergencyTerminate(e);	}
		if (rawHrefLines == null) emergencyTerminate("Brak tekstu do przeparsowania - pusty plik wejscowy.");
		// zrobione
		
		// wlasciwy parser
		ArrayList<String> parsedLinks = new Parser().parse(rawHrefLines);
		if (parsedLinks == null) emergencyTerminate("Brak linkow - nic nie znaleziono.");
		// zrobione
		
		// rafinacja
		parsedLinks = new Refiner(parsedLinks, includesKeyword, excludesKeyword).refine();
		if (parsedLinks == null) emergencyTerminate("Brak linkow - nic nie znaleziono.");
		// zrobione
		
		// prezentacja wynikow
		if (outputFile != null) {
			try {
				new FileWriter(outputFile, parsedLinks).storeToFile();
			} catch (Exception e) {	emergencyTerminate(e);	}
		} else new ConsolePrinter().print(parsedLinks);
		// zrobione
	}


	private static void printUsage() {
		System.out.println();
		System.out.println("Narzedzie do wyparsowywania linkow HTML-owych ze zrodla strony podanego w pliku tekstowym.");
		System.out.println("Argumenty (kolejnosc bez znaczenia):");
		System.out.println("\t[ -z \"zawiera to\" [ -n \"nie zawiera tego\"]] plikZrodlowy [ -o plikWynikowy]");
		System.out.println();
	}


	private static void emergencyTerminate(String msg) {
		System.err.println(msg);
		System.exit(1);
	}

	private static void emergencyTerminate(Exception e) {
		System.err.println(e.getMessage());
		System.exit(1);
	}

}
