package piramida.plansza;


public class Tekst {
	
	private String content;
	private int length;
	
	public Tekst(String text) {
		this.content = text;
		this.length = text.length();
	}

	public String getContent() {
		return content;
	}

	public int getLength() {
		return length;
	}
	
	
}
