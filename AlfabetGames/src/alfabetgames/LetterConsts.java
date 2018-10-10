/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package alfabetgames;

/**
 *
 * @author jan
 */
public enum LetterConsts {
    L("l"),
    P("p"),
    O("o");

    private String letter;
    private LetterConsts(String letter) {
        this.letter = letter;
    }

    public String getLetter(){
        return letter;
    }

    @Override
    public String toString() {
        return letter;
    }


}
