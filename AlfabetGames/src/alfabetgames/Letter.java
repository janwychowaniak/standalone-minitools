/*
 * $Author$
 * $Revision$
 */


package alfabetgames;

/**
 *
 * @author jan
 */
public abstract class Letter {
    private final String letter;

    public Letter(LetterConsts letter) {
        this.letter = letter.toString();
    }

    @Override
    public String toString() {
        return this.letter;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Letter other = (Letter) obj;
        if ((this.letter == null) ? (other.letter != null) : !this.letter.equals(other.letter)) {
            return false;
        }
        return true;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 29 * hash + (this.letter != null ? this.letter.hashCode() : 0);
        return hash;
    }


}
