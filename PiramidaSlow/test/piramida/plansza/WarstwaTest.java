package piramida.plansza;

import java.util.ArrayList;
import piramida.plansza.Tekst;
import piramida.plansza.Warstwa;
import piramida.plansza.Kropka;
import static org.junit.Assert.*;

import org.junit.Test;

public class WarstwaTest {

    @Test
    public void testPrintoutKropkiDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                  Testowy Text                                  (12)");
        expected.add("                                        *                                       ");

        String testText = "Testowy Text";
        Warstwa layer = new Warstwa(new Tekst(testText), new Kropka(), true, true);
        ArrayList<String> actual = layer.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutKropkiBezDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                  Testowy Text                                  ");
        expected.add("                                        *                                       ");

        String testText = "Testowy Text";
        Warstwa layer = new Warstwa(new Tekst(testText), new Kropka(), true, false);
        ArrayList<String> actual = layer.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutBezKropekDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                  Testowy Text                                  (12)");
//        expected.add("                                        *                                       ");

        String testText = "Testowy Text";
        Warstwa layer = new Warstwa(new Tekst(testText), new Kropka(), false, true);
        ArrayList<String> actual = layer.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutBezKropekBezDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                  Testowy Text                                  ");
//        expected.add("                                        *                                       ");

        String testText = "Testowy Text";
        Warstwa layer = new Warstwa(new Tekst(testText), new Kropka(), false, false);
        ArrayList<String> actual = layer.printout();
        assertEquals(expected, actual);
    }
}
