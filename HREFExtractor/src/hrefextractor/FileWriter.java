package hrefextractor;

import java.io.BufferedWriter;
import java.io.File;
import java.util.ArrayList;


/**
 * Klasa ma za zadanie zapisac ArrayList<String> do pliku linijka-per-string, po uprzednim sprawdzeniu
 * poprawnosci lokalizacji.
 * @author jan
 */
public class FileWriter {

	private final String outputFilePath;
	private final ArrayList<String> links;

	public FileWriter(String outputFilePath, ArrayList<String> links) {
		this.outputFilePath = outputFilePath;
		this.links = links;
	}

	/**
	 * Testy.
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<String> linieTestowe = new ArrayList<String>();
		linieTestowe.add("linia testowa 1");
		linieTestowe.add("linia testowa 2");
		linieTestowe.add("linia testowa 3");
		linieTestowe.add("linia testowa 4");
		linieTestowe.add("linia testowa 5");
		linieTestowe.add("linia testowa 6");
		linieTestowe.add("linia testowa 8");
		
		String outputFilePath = "/home/jan/eclipse_workspace/HREFExtractor/testdata/testOutput";
		String outputPathKatalog = "/home/jan/eclipse_workspace/HREFExtractor/testdata";
		String outputPathNieistniejaca = "/home/jan/eclipse_workspace/HREFExtractor/testdata/nieMaTakiejSciezki/plik";
		
		try {
			new FileWriter(null, null).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n------------\n");
		
		try {
			new FileWriter(null, linieTestowe).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n------------\n");
				
		try {
			new FileWriter(outputFilePath, null).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n------------\n");
		
		try {
			new FileWriter(outputPathKatalog, linieTestowe).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n------------\n");
		
		try {
			new FileWriter(outputPathNieistniejaca, linieTestowe).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n------------\n");
		
		try {
			new FileWriter(outputFilePath, linieTestowe).storeToFile();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}

	}

	/**
	 * Zapisuje ArrayList Stringow do pliku. Jesli plik istnieje, nowa zawartosc zostaje dopisana na koncu,
	 * jesli nie istnieje, jest tworzony.
	 * @throws Exception	jesli argumenty klasy zawieraja null, jesli sciezka zapisu bedzie niepoprawna
	 * (katalog, nieistniejaca sciezka do pliku docelowego) lub przy problemach natury i/o
	 */
	public void storeToFile() throws Exception {
		if (outputFilePath == null) throw new Exception("Sciezka pliku wyjsciowego == null");
		if (links == null) 			throw new Exception("Lista linkow == null");
		
		File outputFile = new File(outputFilePath);
		
		if (outputFile.isDirectory()) throw new Exception(outputFile.getCanonicalPath()+": Sciezka pliku wyjsciowego to folder");	// w sumie niepotrzebne, new java.io.FileWriter zalatwia sprawe
		if (outputFile.getParentFile() != null) {				// pominiecie testu dla przypadku, gdyby podano tylko nazwe pliku, majac w domysle aktualna lokalizacje
			if (!outputFile.getParentFile().isDirectory())
				throw new Exception(outputFile.getParent()+": folder sciezki wyjsciowej nie istnieje");	// to chyba tez w sumie
		}
		

		BufferedWriter outputStream = null;

		try {
			outputStream = new BufferedWriter(new java.io.FileWriter(outputFile, true));
			for (String link : links) {
				outputStream.append(link);
				outputStream.newLine();
			}
		} finally {
			if (outputStream != null) outputStream.close();
		}
	}

}
