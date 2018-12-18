package piramida.dict;

import piramida.dict.DictLoader;
import piramida.common.TestConstants;
import static org.junit.Assert.*;

import java.util.ArrayList;

import org.junit.Test;

public class DictLoaderTest {

    @Test
    public void testLoadDict() {
        DictLoader loader = new DictLoader(TestConstants.DICTS_PATH_VALID);

        ArrayList<String> slownik3 = null;
        try {
            slownik3 = loader.loadDict(3);
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }

        System.out.println("Odczytal oto (10 pierwszych):");
        for (int i = 0; i < 10; i++) {
            System.out.println(slownik3.get(i));
        }
    }

    @Test(expected = Exception.class)
    public void testLoadDictExc() throws Exception {
        DictLoader loader = new DictLoader(TestConstants.DICTS_PATH_INVALID);

        ArrayList<String> slownik3 = loader.loadDict(3);
    }
}
