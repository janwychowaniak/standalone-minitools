package piramida.dict;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.SortedSet;
import java.util.TreeSet;

public class Librarian {

    // TODO pasowaloby poprawic, by nie ladowal slownikow za kazdym razem gdy zostanie wywolany controller, lecz raz na app (statyczny inicjalizator?)
	private final String dictFilesFolderAbsPath;
	private ArrayList<Integer> countRange;
	private HashMap<Integer, ArrayList<String>> dictsMap;

	public Librarian(String dictFilesFolder, ArrayList<Integer> countRange) {
		this.dictFilesFolderAbsPath = dictFilesFolder;
		this.countRange = countRange;
		dictsMap = new HashMap<Integer, ArrayList<String>>();
	}
	
	public ArrayList<String> generatePhraseSet() throws DictionaryFileNotFoundException {
		loadDicts();
		ArrayList<String> resultList = new ArrayList<String>();

		for (Integer countItem : countRange) {
			resultList.add(getRandomPhrase(countItem));
		}
		return resultList;
	}
	
	private void loadDicts () throws DictionaryFileNotFoundException {
		SortedSet<Integer> countSet = new TreeSet<Integer>();
		DictLoader loader = new DictLoader(dictFilesFolderAbsPath);
		
		for (Integer integer : countRange) 	countSet.add(integer);
		for (Integer integer : countSet) 	dictsMap.put(integer, loader.loadDict(integer));
	}
	
	private String getRandomPhrase (Integer distNr) {
		ArrayList<String> chosenDict = dictsMap.get(distNr);
		int chosenIndex = new Random().nextInt(chosenDict.size());
		return chosenDict.get(chosenIndex);
	}
}

