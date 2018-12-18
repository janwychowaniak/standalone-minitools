package piramida.plansza;

import java.util.ArrayList;

public class Warstwa {

    private Tekst text;
    private Kropka dot;
    private boolean kropki;         // czy wyswietli kropki
    private boolean dlugosci;       // czy wyswietli dlugosci
    private static String SPACE_CHAR = " ";
    private static int TOTAL_WIDTH = 80;

    public Warstwa(Tekst text, Kropka dot, boolean kropki, boolean dlugosci) {
        this.text = text;
        this.dot = dot;
        this.kropki = kropki;
        this.dlugosci = dlugosci;
    }

    public ArrayList<String> printout() {
        ArrayList<String> warstwa = new ArrayList<String>();
        warstwa.add(printLayerElement(text));
        if (kropki) warstwa.add(printLayerElement(dot));
        return warstwa;
    }

    private String printLayerElement(Tekst text) {
        StringBuilder builder = new StringBuilder();
        int firstWordHalfLength = text.getLength() / 2;
        int firstSpacesPortionAmount = TOTAL_WIDTH / 2 - firstWordHalfLength;

        for (int i = 1; i <= firstSpacesPortionAmount; i++) {
            builder.append(SPACE_CHAR);
        }
        builder.append(text.getContent());
        for (int i = firstSpacesPortionAmount + text.getLength() + 1; i <= TOTAL_WIDTH; i++) {
            builder.append(SPACE_CHAR);
        }
        if (text instanceof Kropka) {
            return builder.toString();
        }
        if (dlugosci) builder.append("(").append(text.getLength()).append(")");
        return builder.toString();
    }
}
