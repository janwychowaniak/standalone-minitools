
public class SzybkCzyt.Spostrzeg.LiczbyOsobno.IntegerRandTEST : Object {
	
    public static void main (string[] args)
    {
//~ 		IntegerRand gen = new IntegerRand();
		uint number;
		int i;
//~ 		
//~ 		for (i=0; i<10; i++)
//~         {
//~ 	        number = gen.get_number(1, 20);
//~ 			stdout.printf ("%u\n", number);
//~ 		}
//~ 
//~ 		stdout.printf ("\n");

		IntegerRand another_gen = new IntegerRand();
//~ 		for (i=0; i<10; i++)
//~         {
//~ 	        number = another_gen.get_number(15, 30);
//~ 			stdout.printf ("%u\n", number);
//~ 		}
//~ 		
//~ 		stdout.printf ("\n");
//~ 		for (i=0; i<20; i++)
//~         {
//~ 	        number = another_gen.get_number(1, 3);
//~ 			stdout.printf ("%u\n", number);
//~ 		}
//~ 
		stdout.printf ("\n");
		for (i=0; i<20; i++)
        {
	        number = another_gen.get_1toX_number(3);
			stdout.printf ("%u\n", number);
		}
		
    }
}

