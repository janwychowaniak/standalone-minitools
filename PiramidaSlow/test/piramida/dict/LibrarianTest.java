package piramida.dict;

import piramida.dict.CountSpreader;
import piramida.dict.Librarian;
import static org.junit.Assert.*;

import java.util.ArrayList;

import org.junit.Ignore;
import org.junit.Test;

public class LibrarianTest {

	@Test
	public void testGeneratePhraseSet() {
		ArrayList<Integer> countRange = new CountSpreader().generateRange(3, 10, 18);
		Librarian lib = new Librarian("/home/jan/eclipse_workspace/PiramidaSlow/dicts", countRange);
		ArrayList<String> resultList;
		try {
			resultList = lib.generatePhraseSet();
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
		
		System.out.print("countRange: ");
		for (Integer number : countRange) {
			System.out.print(number + ", ");
		}
		System.out.println();

		System.out.println("Generated phrases:");
		for (String phrase : resultList) {
			System.out.println(phrase+ ", ");
		}
	}

//	@Ignore
//	@Test
//	public void testLoadDicts() {
//		Librarian lib = new Librarian("/home/jan/eclipse_workspace/PiramidaSlow/dicts", new CountSpreader().generateRange(3, 10, 8));
//		try {
//			lib.loadDicts();
//		} catch (Exception e) {
//			e.printStackTrace();
//			return;
//		}
//		
//		System.out.println("countRange: ");
//		for (Integer number : lib.countRange) {
//			System.out.print(number + ", ");
//		}
//		
//		System.out.println();
//		System.out.println("lib contents:");
//		for (Integer number : lib.dictsMap.keySet()) {
//			System.out.print("number " + number+": ");
//			for (String phrase : lib.dictsMap.get(number)) {
//				System.out.print(phrase +", ");
//			}
//			System.out.println();
//		}
//	}
//
//	@Ignore
//	@Test
//	public void testGetRandomPhrase() {
//		Librarian lib = new Librarian("/home/jan/eclipse_workspace/PiramidaSlow/dicts", new CountSpreader().generateRange(3, 10, 8));
//		try {
//			lib.loadDicts();
//		} catch (Exception e) {
//			e.printStackTrace();
//			return;
//		}
//
//		System.out.println("Random phrase: "+lib.getRandomPhrase(2));
//	}

}
