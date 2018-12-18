package piramida.plansza;

import piramida.plansza.Kropka;
import static org.junit.Assert.*;

import org.junit.Test;

public class KropkaTest {

	private String testchar = "*";
	
	@Test
	public void testGetTekst() {
		Kropka dot = new Kropka();
		assertEquals(dot.getContent(), testchar);
	}

	@Test
	public void testGetIloscZnakow() {
		Kropka dot = new Kropka();
		assertEquals(dot.getLength(), testchar.length());
	}

}
