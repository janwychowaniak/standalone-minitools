package piramida.plansza;

import java.util.ArrayList;

public class Plansza {

    private ArrayList<Warstwa> pyramid = new ArrayList<Warstwa>();

    public Plansza(ArrayList<String> phraseList, boolean kropki, boolean dlugosci) {
        for (String phrase : phraseList) {
            pyramid.add(new Warstwa(new Tekst(phrase), new Kropka(), kropki, dlugosci));
        }
    }

    public ArrayList<String> printout() {
        ArrayList<String> planszaPrintout = new ArrayList<String>();
        for (Warstwa layer : pyramid) {
            planszaPrintout.addAll(layer.printout());
//            ArrayList<String> layerPrintout = layer.printout();
        }
        return planszaPrintout;
    }
}
