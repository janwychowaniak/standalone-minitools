package hrefextractor;

import java.io.BufferedReader;
import java.io.File;
import java.util.ArrayList;
import java.util.Locale;


/**
 * Klasa odpowiada za wczytanie zadaego pliku zrodlowego metoda String-per-linijka i wstepne przesianie
 * poprzez odrzucenie linijek nie zawierajacych znacznika "html".
 * NOTE: Nie wiem, czy to dobrze, ze to przesianie mam miejsce tu, nie w parserze.
 */
public class FileReader {

	private final String sourceFilePath;
	private static final String KEYWORD = "href";

	
	/**
	 * Testy tylko.
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<String> listaPlikow = new ArrayList<String>();
		listaPlikow.add("/home/jan/eclipse_workspace/HREFExtractor/testdata/minitest");
		listaPlikow.add("/home/jan/eclipse_workspace/HREFExtractor/testdata/nieMaMnie");
		listaPlikow.add("/home/jan/eclipse_workspace/HREFExtractor/testdata/binarny.png");
		listaPlikow.add("/home/jan/eclipse_workspace/HREFExtractor/testdata/binarnyNieczytelny.png");
		listaPlikow.add("../../testdata/minitest");
		listaPlikow.add("../testdata/minitest");
		listaPlikow.add("../../../testdata/minitest");
		listaPlikow.add("/home/jan/eclipse_workspace/HREFExtractor/testdata/hrefy");
		
		
		for (String plik : listaPlikow) {
			FileReader reader = new FileReader(plik);
			ArrayList<String> hrefLines = null;
			try {
				hrefLines = reader.getFilteredLines();
			} catch (Exception e) {
				System.err.println("\nProblem z \""+plik+"\": ");
				System.err.println(e.getMessage());
				continue;
			}
			
			System.out.println("\nW pliku \""+plik+"\" odkryto:");
			if (hrefLines == null) {
				System.out.println("Nic, pusty");
				continue;
			}
			for (String linia : hrefLines) {
				System.out.println("Linia: "+ linia);
			}
		}
		
		System.out.println(FileReader.class.getCanonicalName());
		String classPath = System.getProperty("java.class.path");
        System.out.println("java.class.path = " + classPath);
	}

	
	public FileReader(String filePath) {
		this.sourceFilePath = filePath;
	}

	/**
	 * Filtruje linijki z "readLines" pod katem posiadania znacznika. Dziala case-insensitive
	 * dla formy znacznika w pliku. Klasowy agregator wyjatkow. 
	 * @return	ArrayList<String> linijek ze znacznikiem, lub null, jesli nie bedzie zadnej.
	 * @throws Exception 
	 */
	public ArrayList<String> getFilteredLines() throws Exception {
		ArrayList<String> allLines = readLines();
		ArrayList<String> filteredLines = new ArrayList<String>();
		
		for (String line : allLines) {
			if (line.toLowerCase(Locale.ENGLISH).contains(KEYWORD)) {
				filteredLines.add(line);
			}
		}
		if (filteredLines.isEmpty()) filteredLines = null;
		return filteredLines;
	}


	/**
	 * Dokonuje wlasciwego dostepu do pliku po uprzednim sprawdzeniu, czy ten istnieje i jest normalnym
	 * plikiem.
	 * @return	ArrayList<String> linijek z pliku. Pusta, jesli i plik pusty.
	 * @throws Exception	jesli plik nie istnieje, nie jest normalny, czytelny lub inne i/o problemy.
	 */
	private ArrayList<String> readLines() throws Exception {
		File sourceFile = new File(sourceFilePath);
		if (!sourceFile.isFile()) {
			throw new Exception("Sciezka zrodlowa nie istnieje lub nie jest plikiem.");
		}

		ArrayList<String> lines = new ArrayList<String>();
		BufferedReader sourceInputStream = null;
        try {
            sourceInputStream = new BufferedReader(new java.io.FileReader(sourceFile));	// throws FileNotFoundException
            String line;
            while ((line = sourceInputStream.readLine()) != null) {	// throws IOException
            	lines.add(line);
            }
        } finally {
            if (sourceInputStream != null) {
                sourceInputStream.close();
            }
        }

		return lines;
	}

}
