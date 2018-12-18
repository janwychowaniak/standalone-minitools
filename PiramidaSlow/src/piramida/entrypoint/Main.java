package piramida.entrypoint;

import java.util.ArrayList;
import piramida.dict.DictionaryFileNotFoundException;
import java.util.logging.Level;
import java.util.logging.Logger;
import piramida.ctrl.BadDictsLocationException;
import piramida.ctrl.BadNumberArgumentsException;
import piramida.ctrl.Controller;


public class Main {
    /**
     * @param args
     */
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new RuntimeException("Wrong args number: "+args.length+"!=6");   // TODO - troche nieladnie chyba
        }
        int lowerBoundary = Integer.parseInt(args[0]);
        int upperBoundary = Integer.parseInt(args[1]);
        int spread = Integer.parseInt(args[2]);
        String dictPath = args[3];
        boolean kropki = new Boolean(args[4]).booleanValue();
        boolean dlugosci = new Boolean(args[5]).booleanValue();

        // TODO nazwy tych argumentow konfuduja
        Controller ctlr = new Controller(lowerBoundary, upperBoundary, spread, dictPath, kropki, dlugosci);

        try {
            ctlr.validateArgs();
        } catch (BadNumberArgumentsException ex) {
            Logger.getLogger(Controller.class.getName()).log(Level.SEVERE, null, ex);
            return;
        } catch (BadDictsLocationException ex) {
            Logger.getLogger(Controller.class.getName()).log(Level.SEVERE, null, ex);
            return;
        }
        try {
            ArrayList<String> finalPrintout = ctlr.perform();
            for (String string : finalPrintout) {
                System.out.println(string);
            }
        } catch (DictionaryFileNotFoundException ex) {
            Logger.getLogger(Controller.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
