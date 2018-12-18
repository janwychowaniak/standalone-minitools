package piramida.dict;

import java.util.ArrayList;

public class CountSpreader {
	
	public ArrayList<Integer> generateRange(int begin, int end, int count) {
		ArrayList<Integer> range = new ArrayList<Integer>();
		int spread = end + 1 - begin;
		for (int i = 0; i < count; i++) {
			range.add(begin + i*spread/count); 
		}
		return range;
	}
}
