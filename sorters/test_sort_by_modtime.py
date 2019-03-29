from sort_by_modtime import unique_values
from sort_by_modtime import sort_dict_by_val




def test_unique_values():

    dict_vals_unique = {}
    dict_vals_nonunique = {}

    dict_vals_unique['AUD0056.3gp'] = 1388141568
    dict_vals_unique['AUD0057.3gp'] = 1388144212
    dict_vals_unique['AUD0058.3gp'] = 1388146678

    dict_vals_nonunique['AUD0056.3gp'] = 1388141568
    dict_vals_nonunique['AUD0057.3gp'] = 1388144212 # <--
    dict_vals_nonunique['AUD0058.3gp'] = 1388144212 # <--
    dict_vals_nonunique['AUD0059.3gp'] = 1388146678

    assert unique_values(dict_vals_unique.values())
    assert not unique_values(dict_vals_nonunique.values())



def test_sort_dict_by_val():

    x_orig      = {"1":2, "3":4, "4":3, "2":1, "0":0}
    x_valsorted = [("0",0), ("2",1), ("1",2), ("4",3), ("3",4)]

    assert sort_dict_by_val (x_orig) == x_valsorted

