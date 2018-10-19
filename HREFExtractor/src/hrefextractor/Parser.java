package hrefextractor;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Klasa przesukuje otrzymany ArrayList<String>, linijka-per-String, i wyparsowywuje linki internetowe.
 * Ma wbity na sztywno REGEX.
 * @author jan
 *
 */
public class Parser {

	private static final String REGEX = "(href=\"(.*?)\")";

	/**
	 * Testy
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<String> lines = new ArrayList<String>();
		BufferedReader sourceInputStream = null;
		
        try {
            sourceInputStream = new BufferedReader(new java.io.FileReader("/home/jan/eclipse_workspace/HREFExtractor/testdata/hrefy_proste"));	// throws FileNotFoundException
            String line;
            while ((line = sourceInputStream.readLine()) != null) {	// throws IOException
            	lines.add(line);
            }
        } catch (Exception e) {
			System.err.println("\nProblem z plikiem: ");
			System.err.println(e.getMessage());
        } finally {
            if (sourceInputStream != null) {
                try {
					sourceInputStream.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
            }
        }
        
        ArrayList<String> links = new Parser().parse(lines);
        if (links == null) {
			System.out.println("Nie ma linkow zadnych tu.");
			return;
		}
        for (String link : links) {
			System.out.println(link);
		}
	}

	/**
	 * Przesukiwanie jest case-insensitive. Stosowane sa Capturing Groups celem obdarcia znalezionego linka
	 * ze szronu HTML-owego.
	 * @param lines	ArrayList<String> z ukrytymi w tych Stringach linkami do znalezienia
	 * @return		ArrayList<String> z wyekstraktowanymi linkami (link-per-String) lub null, jesli takowych nie stwierdzono
	 */
	public ArrayList<String> parse(ArrayList<String> lines) {
		ArrayList<String> links = new ArrayList<String>();
		Pattern pattern = Pattern.compile(REGEX, Pattern.CASE_INSENSITIVE);
		
		for (String line : lines) {
			Matcher matcher = pattern.matcher(line);
			while(matcher.find()) {
				links.add(matcher.group(2));
			}
		}

		if (links.isEmpty()) links = null;
		return links;
	}

}
