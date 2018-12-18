package piramida.ctrl;

import piramida.entrypoint.Main;
import piramida.common.TestConstants;

import org.junit.Test;

public class ControllerTest {

	@Test
	public void testMain() {
		int lowerBoundary = 19;
		int upperBoundary = 23;
		int spread = 10;
		String dictPath = TestConstants.DICTS_PATH_VALID;
		
		Main.main(new String[] {""+lowerBoundary, ""+upperBoundary, ""+spread, dictPath, "true", "true"});
                System.out.println("--------------------------------------------------------");
		Main.main(new String[] {""+lowerBoundary, ""+upperBoundary, ""+spread, dictPath, "true", "false"});
                System.out.println("--------------------------------------------------------");
		Main.main(new String[] {""+lowerBoundary, ""+upperBoundary, ""+spread, dictPath, "false", "true"});
                System.out.println("--------------------------------------------------------");
		Main.main(new String[] {""+lowerBoundary, ""+upperBoundary, ""+spread, dictPath, "false", "false"});
                System.out.println("--------------------------------------------------------");

	}

}
