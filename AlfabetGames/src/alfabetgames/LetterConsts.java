package alfabetgames;


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
