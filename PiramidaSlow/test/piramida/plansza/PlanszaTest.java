package piramida.plansza;

import piramida.plansza.Plansza;
import static org.junit.Assert.*;

import java.util.ArrayList;
import org.junit.Before;

import org.junit.Test;

public class PlanszaTest {

    private ArrayList<String> phraseList = new ArrayList<String>();

    @Before
    public void setUpTestArray() {
        phraseList.add("test");
        phraseList.add("kolacja");
        phraseList.add("stonoga niemrawa stonoga");
        phraseList.add("stonoga niemrawa stonoga niemrawa ");
        phraseList.add("stonoga niemrawa przemoc nie jest srodkiem do studni");
    }

    @Test
    public void testPrintoutKropkiDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                      test                                      (4)");
        expected.add("                                        *                                       ");
        expected.add("                                     kolacja                                    (7)");
        expected.add("                                        *                                       ");
        expected.add("                            stonoga niemrawa stonoga                            (24)");
        expected.add("                                        *                                       ");
        expected.add("                       stonoga niemrawa stonoga niemrawa                        (34)");
        expected.add("                                        *                                       ");
        expected.add("              stonoga niemrawa przemoc nie jest srodkiem do studni              (52)");
        expected.add("                                        *                                       ");

        Plansza pyramid = new Plansza(phraseList, true, true);
        ArrayList<String> actual = pyramid.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutKropkiBezDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                      test                                      ");
        expected.add("                                        *                                       ");
        expected.add("                                     kolacja                                    ");
        expected.add("                                        *                                       ");
        expected.add("                            stonoga niemrawa stonoga                            ");
        expected.add("                                        *                                       ");
        expected.add("                       stonoga niemrawa stonoga niemrawa                        ");
        expected.add("                                        *                                       ");
        expected.add("              stonoga niemrawa przemoc nie jest srodkiem do studni              ");
        expected.add("                                        *                                       ");

        Plansza pyramid = new Plansza(phraseList, true, false);
        ArrayList<String> actual = pyramid.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutBezKropekDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                      test                                      (4)");
//        expected.add("                                        *                                       ");
        expected.add("                                     kolacja                                    (7)");
//        expected.add("                                        *                                       ");
        expected.add("                            stonoga niemrawa stonoga                            (24)");
//        expected.add("                                        *                                       ");
        expected.add("                       stonoga niemrawa stonoga niemrawa                        (34)");
//        expected.add("                                        *                                       ");
        expected.add("              stonoga niemrawa przemoc nie jest srodkiem do studni              (52)");
//        expected.add("                                        *                                       ");

        Plansza pyramid = new Plansza(phraseList, false, true);
        ArrayList<String> actual = pyramid.printout();
        assertEquals(expected, actual);
    }

    @Test
    public void testPrintoutBezKropekBezDlugosci() {
        ArrayList<String> expected = new ArrayList<String>();
        expected.add("                                      test                                      ");
//        expected.add("                                        *                                       ");
        expected.add("                                     kolacja                                    ");
//        expected.add("                                        *                                       ");
        expected.add("                            stonoga niemrawa stonoga                            ");
//        expected.add("                                        *                                       ");
        expected.add("                       stonoga niemrawa stonoga niemrawa                        ");
//        expected.add("                                        *                                       ");
        expected.add("              stonoga niemrawa przemoc nie jest srodkiem do studni              ");
//        expected.add("                                        *                                       ");

        Plansza pyramid = new Plansza(phraseList, false, false);
        ArrayList<String> actual = pyramid.printout();
        assertEquals(expected, actual);
    }
}
