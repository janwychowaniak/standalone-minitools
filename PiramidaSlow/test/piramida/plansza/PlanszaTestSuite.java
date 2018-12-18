package piramida.plansza;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;


@RunWith(Suite.class)
@Suite.SuiteClasses({   piramida.plansza.WarstwaTest.class,
                        piramida.plansza.TestTekst.class,
                        piramida.plansza.KropkaTest.class,
                        piramida.plansza.PlanszaTest.class
                    })
public class PlanszaTestSuite {

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

}
