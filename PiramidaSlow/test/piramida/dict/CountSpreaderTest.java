package piramida.dict;

import piramida.dict.CountSpreader;
import java.util.ArrayList;

import org.junit.Test;

public class CountSpreaderTest {

	@Test
	public void testGenerateRange() {
		System.out.println("Range 1: (0, 10, 3)");
		ArrayList<Integer> range1 = new CountSpreader().generateRange(0, 10, 3);
		for (Integer integer : range1) {
			System.out.println(""+integer);
		}
		System.out.println();

		System.out.println("Range 2: (0, 3, 10)");
		ArrayList<Integer> range2 = new CountSpreader().generateRange(0, 3, 10);
		for (Integer integer : range2) {
			System.out.println(""+integer);
		}
		System.out.println();

		System.out.println("Range 3: (0, 10, 11)");
		ArrayList<Integer> range3 = new CountSpreader().generateRange(0, 10, 11);
		for (Integer integer : range3) {
			System.out.println(""+integer);
		}
		System.out.println();

		System.out.println("Range 4: (3, 20, 35)");
		ArrayList<Integer> range4 = new CountSpreader().generateRange(3, 20, 35);
		for (Integer integer : range4) {
			System.out.println(""+integer);
		}
		System.out.println();

	}

}
