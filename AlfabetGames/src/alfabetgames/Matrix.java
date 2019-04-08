package alfabetgames;

import java.util.HashSet;
import java.util.Set;


public class Matrix {

    private static final int ROWS = 4;
    private static final int COLS = 6;
    private Letter[][] lettersMatrix = new Letter[ROWS][COLS];

       
    public Matrix() {
        Letter [] verticalCache = new Letter[COLS];
        Letter horizontalCache;

        for (int row = 0; row < ROWS; row++) {
            horizontalCache = null;
            for (int col = 0; col < COLS; col++) {
                LettersSet set = new LettersSet();
                if(verticalCache[col] != null) set.exclude(verticalCache[col]);
                if(horizontalCache != null) set.exclude(horizontalCache);
                Letter newLetter = set.getRandomLetter();
                lettersMatrix[row][col] = verticalCache[col] = horizontalCache = newLetter;
            }
        }
    }

    public void display() {
        String [] alfabet = {"ABCDEF", "GHIJKL", "MNOPRS", "TUWXYZ"};
        for (int row = 0; row < ROWS; row++) {
            System.out.println(alfabet[row]);
            for (int col = 0; col < COLS; col++) {
                System.out.print(lettersMatrix[row][col]);
            }
            System.out.println();
        }
    }
    
}
