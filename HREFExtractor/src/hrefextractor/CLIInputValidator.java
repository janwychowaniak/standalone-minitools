package hrefextractor;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Klasa sluzy do interperetacji argumentow zadanych z wiersza polecen. Argumenty maja postac:
 * [ -z "zawiera to" [ -n "nie zawiera tego"]] zrodlo [ -o outputFile]
 * (kolejnosc dowolna).
 * Sercem klasy jest prywatna metoda "parseInput" implementujaca algorytm interpretowania
 * inputu i ekstrakcji parametrow. Interfejs klasy pozwala jedynie na odpytanie o zadany argument. Kazda
 * metoda interfejsu na poczatku sprawdza, czy wejscie zostalo przeparsowane, uruchamiajac te operacje,
 * jesli nie.
 * Klasa dziala bezblednie dla poprawnych inputow, jak rowniez prawidlowo rozpoznaje kilka typowych
 * bledow. W przypadku niepoprawnosci jakiegos rodzaju w inpucie, rzuca wyjatkami z kazdej metody
 * publicznej.
 * @author jan
 *
 */
public class CLIInputValidator {

	/**
	 * Testy li tylko.
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) {
		ArrayList<String[]> inputArgsArray = new ArrayList<String[]>();

		String[] sampleInput1 = {"zrodlo"};
		String[] sampleInput2 = {"-z", "zawiera to", "zrodlo"};
		String[] sampleInput3 = {"-n", "nie zawiera tego", "zrodlo"};
		String[] sampleInput4 = {"zrodlo", "-o", "outputFile"};
		String[] sampleInput5 = {"-n", "nie zawiera tego", "zrodlo", "-o", "outputFile"};
		String[] sampleInput6 = {"-z", "zawiera to", "zrodlo", "-o", "outputFile"};
		String[] sampleInput7 = {"-z", "zawiera to", "-n", "nie zawiera tego", "zrodlo"};
		String[] sampleInput8 = {"-z", "zawiera to", "-n", "nie zawiera tego", "zrodlo", "-o", "outputFile"};

		inputArgsArray.add(sampleInput1);
		inputArgsArray.add(sampleInput2);
		inputArgsArray.add(sampleInput3);
		inputArgsArray.add(sampleInput4);
		inputArgsArray.add(sampleInput5);
		inputArgsArray.add(sampleInput6);
		inputArgsArray.add(sampleInput7);
		inputArgsArray.add(sampleInput8);

//		for (String[] sampleInput : inputArgsArray) {
//			CLIInputValidator validator = new CLIInputValidator(sampleInput);
//			
//			String includes = null;
//			String excludes = null;
//			String outputFile = null;
//			String sourceFile = null;
//			try {
//				includes = validator.getIncludesKeyword();
//				excludes = validator.getExcludesKeyword();
//				outputFile = validator.getOutputFileKeyword();
//				sourceFile = validator.getSourceFile();
//			} catch (Exception e) {}
//
//			System.out.println("----\n");
//			System.out.print("For input ");
//			for (String string : sampleInput)	System.out.print(string+ " ");
//			System.out.println();
//			
//			System.out.println("Control words:");
//			System.out.println("-z " + includes);
//			System.out.println("-n " + excludes);
//			System.out.println("-o " + outputFile);
//			
//			System.out.println("sourcefile:");
//			System.out.println(sourceFile);
//		}
		
		
		ArrayList<String[]> zlosliwyInputArray = new ArrayList<String[]>();
		
		String[] sampleInput11 = {"-z", "zawiera to", "-n", "nie zawiera tego", "-o", "outputFile"};	// brak zrodla
		String[] sampleInput12 = {"-z", "-n", "nie zawiera tego", "zrodlo"};							// brak tresci kontrolki
		String[] sampleInput13 = {"-n", "nie zawiera tego", "zrodlo", "-o"};							// j/w - kontrolka na koncu
		String[] sampleInput14 = {"-n", "nie zawiera tego", "zrodlo", "zrodlo2", "-o", "outputFile"};	// kilka zrodel
		String[] sampleInput15 = {"-z", "zawiera to", "-byk", "nie zawiera tego", "zrodlo"};			// nieznana kontrolka
		
		zlosliwyInputArray.add(sampleInput11);
		zlosliwyInputArray.add(sampleInput12);
		zlosliwyInputArray.add(sampleInput13);
		zlosliwyInputArray.add(sampleInput14);
		zlosliwyInputArray.add(sampleInput15);

		for (String[] sampleInput : zlosliwyInputArray) {
			CLIInputValidator validator = new CLIInputValidator(sampleInput);
			
			String includes = null;
			String excludes = null;
			String outputFile = null;
			String sourceFile = null;
			try {
				includes = validator.getIncludesKeyword();
				excludes = validator.getExcludesKeyword();
				outputFile = validator.getOutputFileKeyword();
				sourceFile = validator.getSourceFile();
			} catch (Exception e) {System.out.println(e.getMessage());}

			System.out.print("For input ");
			for (String string : sampleInput)	System.out.print(string+ " ");
			System.out.println();
			
			System.out.println("Control words:");
			System.out.println("-z " + includes);
			System.out.println("-n " + excludes);
			System.out.println("-o " + outputFile);
			
			System.out.println("sourcefile:");
			System.out.println(sourceFile);
			System.out.println("----\n");
		}
	}



	private static final String INCLUDES_CONTROL = "-z";
	private static final String EXCLUDES_CONTROL = "-n";
	private static final String OUTPUT_FILE_CONTROL = "-o";
	
	private String[] rawInput;
	private String sourceFile = null;
	private HashMap<String, String> controlsMap = new HashMap<String, String>();

	
	public CLIInputValidator(String[] input) {
		rawInput = input;
	}

	/**
	 * @return	String z keywordem lub null, jesli nie bylo go w argumentach.
	 * @throws Exception
	 */
	public String getIncludesKeyword() throws Exception {
		ensureParsed();
		return controlsMap.get(INCLUDES_CONTROL);
	}
	
	/**
	 * @return	String z keywordem lub null, jesli nie bylo go w argumentach.
	 * @throws Exception
	 */
	public String getExcludesKeyword() throws Exception {
		ensureParsed();
		return controlsMap.get(EXCLUDES_CONTROL);
	}
	
	/**
	 * @return	String z keywordem lub null, jesli nie bylo go w argumentach.
	 * @throws Exception
	 */
	public String getOutputFileKeyword() throws Exception {
		ensureParsed();
		return controlsMap.get(OUTPUT_FILE_CONTROL);
	}

	/**
	 * @return	String z zadana nazwa pliku zrodlowego.
	 * @throws Exception
	 */
	public String getSourceFile() throws Exception {
		ensureParsed();
		return sourceFile;
	}

	/**
	 * Sprawdza czy dokonano parsowania inputu w surowej postaci, takiej jaka przychodzi do klasy,
	 * uruchamiajac je jesli nie. Okresla to na pdst. obecnosci argumentu pliku zrodlowego.
	 * Jednoczesnie klasowy koncentrator wyjatkow.
	 * @throws Exception	wszystkie klasowe.
	 */
	private void ensureParsed() throws Exception {
		if (sourceFile == null) {
			try {
				parseInput(rawInput);
			} catch (IndexOutOfBoundsException e) {
				throw new Exception("Pusty przelacznik.");							// lek na pusty przelacznik na koncu
			} 
		}
		if (sourceFile == null) throw new Exception("Brak pliku zrodlowego.");		// lek na niepodanie pliku zrodlowego
	}
	
	/**
	 * Implementuje algorytm interpretowania inputu i ekstrakcji parametrow.
	 * @param input
	 * @throws Exception
	 */
	private void parseInput(String[] input) throws Exception {
		int offset = 0;
		int length = input.length;

		while (offset < length) {
			if (isValidControl(input[offset])) {
				controlsMap.put(input[offset], input[offset+1]);
				offset += 2;								// moze tu wyskoczyc poza tablice, jesli pusta kontrolka bedzie na koncu
			} else {
				if (looksLikeControl(input[offset])) {
					throw new Exception("Nieznana kontrolka.");
				} else {
					if (sourceFile==null) {
						sourceFile = input[offset];
						offset++;
					} else {
						throw new Exception("Kilka plikow zrodlowych. Wolno jeden.");
					}
				}
			}
		}
	}

	
	private boolean looksLikeControl(String word) {
		return word.startsWith("-");
	}

	private boolean isValidControl(String word) {
		return (word.equals(INCLUDES_CONTROL) || word.equals(EXCLUDES_CONTROL) || word.equals(OUTPUT_FILE_CONTROL));
	}

}
