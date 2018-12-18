package piramida.plansza;

import piramida.plansza.Tekst;
import static org.junit.Assert.*;

import org.junit.Test;

public class TestTekst {

	private String testtext = "whatever";

	@Test
	public void testGetTekst() {
		Tekst dot = new Tekst(testtext);
		assertEquals(dot.getContent(), testtext);
	}

	@Test
	public void testGetIloscZnakow() {
		Tekst dot = new Tekst(testtext);
		assertEquals(dot.getLength(), testtext.length());
	}

}
