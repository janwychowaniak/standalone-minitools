package piramida.dict;

import java.io.BufferedReader;
import java.io.File;
import java.util.ArrayList;

public class DictLoader {

    private final String dictFilesFolderAbsPath;
    private final String dictFilesNamesPrefix = "dict_";

    public DictLoader(String dictFilesFolder) {
        this.dictFilesFolderAbsPath = dictFilesFolder;
    }

    public ArrayList<String> loadDict(int phraseLength) throws DictionaryFileNotFoundException {
        String dictFileAbsPath = dictFilesFolderAbsPath + File.separator + dictFilesNamesPrefix + phraseLength;
        try {
            return readDictFile(new File(dictFileAbsPath));
        } catch (Exception e) {
            throw new DictionaryFileNotFoundException(dictFileAbsPath + ": "+e.getMessage()+
                    ", or no such dictionary file, prosze ja Ciebie, czlowieku.");
        }
    }

    /**
     * Dokonuje wlasciwego dostepu do pliku po uprzednim sprawdzeniu, czy ten istnieje i jest normalnym
     * plikiem.
     * @return	ArrayList<String> linijek z pliku. Pusta, jesli i plik pusty.
     * @throws Exception	jesli plik nie istnieje, nie jest normalny, czytelny lub inne i/o problemy.
     */
    private ArrayList<String> readDictFile(File sourceFile) throws Exception {
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
