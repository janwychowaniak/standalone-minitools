package piramida.ctrl;

import java.io.File;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

import piramida.plansza.Plansza;
import piramida.dict.CountSpreader;
import piramida.dict.DictionaryFileNotFoundException;
import piramida.dict.Librarian;

public class Controller {

    private int lowerBoundary;
    private int upperBoundary;
    private int spread;
    private String dictPath;
    private boolean kropki;         // czy wyswietli kropki
    private boolean dlugosci;       // czy wyswietli dlugosci

    public Controller(int lowerBoundary, int upperBoundary, int spread, String dictPath, boolean kropki, boolean dlugosci) {
        this.lowerBoundary = lowerBoundary;
        this.upperBoundary = upperBoundary;
        this.spread = spread;
        this.dictPath = dictPath;
        this.kropki = kropki;
        this.dlugosci = dlugosci;
    }


    public void validateArgs()
            throws BadNumberArgumentsException, BadDictsLocationException {
        // TODO - ponizsze 80 juz sie gdzies przewija. jesli bede to kiedyc przetwarzal, warto uporzadkowac magiczne liczby.
        if ((lowerBoundary < 3) || (upperBoundary > 80) || (lowerBoundary > upperBoundary) || (spread < 1)) {
            throw new BadNumberArgumentsException("*** Uporzadkuj parametry liczbowe, Grzegorz! Ma byc <3;80>.");
        }
        if (!(new File(dictPath).isDirectory())) {
            throw new BadDictsLocationException("*** Cos nie ma takiej lokalizacji na slowniki, Apoloniusz!");
        }

    }

    public ArrayList<String> perform()
            throws DictionaryFileNotFoundException {
        ArrayList<Integer> countRange = new CountSpreader().generateRange(lowerBoundary, upperBoundary, spread);
        Librarian lib = new Librarian(dictPath, countRange);
        ArrayList<String> resultList = lib.generatePhraseSet();
        Plansza pyramid = new Plansza(resultList, kropki, dlugosci);
        return pyramid.printout();
    }
}
