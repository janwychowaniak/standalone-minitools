    
public int main(string[] args) {
    test0();
    test1();
    test2();
    
    return 0;
}


void test0()
{
    var tested = new Celownik.ArgsCarrier();

	assert(!tested.l_flag);
	assert(!tested.d_flag);
	assert(tested.d_val==0);
	assert(!tested.a_flag);
	assert(tested.a_str_date==null);
	assert(tested.a_str_text==null);
}
	
void test1()
{
    var tested = new Celownik.ArgsCarrier();
    tested.l_flag = true;

	 assert(tested.l_flag);
	assert(!tested.d_flag);
	assert(tested.d_val==0);
	assert(!tested.a_flag);
	assert(tested.a_str_date==null);
	assert(tested.a_str_text==null);
}

void test2()
{
    var tested = new Celownik.ArgsCarrier();
    tested.d_flag = true;
    tested.d_val=5;

	assert(!tested.l_flag);
	 assert(tested.d_flag);
	 assert(tested.d_val==5);
	assert(!tested.a_flag);
	assert(tested.a_str_date==null);
	assert(tested.a_str_text==null);
}
