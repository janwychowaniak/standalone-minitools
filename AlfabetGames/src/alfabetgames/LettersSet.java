package alfabetgames;

import java.util.HashSet;
import java.util.Set;


public class LettersSet {

    private Set<Letter> letters;

    LettersSet() {
        letters = new HashSet<Letter>();
        letters.add(new LetterL());
        letters.add(new LetterP());
        letters.add(new LetterO());
    }

    public void exclude(Letter letter) {
        letters.remove(letter);
    }

    public Letter getRandomLetter() {
        Letter [] lettersArray = letters.toArray(new Letter[1]);
        return lettersArray[new java.util.Random().nextInt(lettersArray.length)];
    }

}
