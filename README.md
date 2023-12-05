# OTJXT
Practical Equi-Joins over Encrypted Database    
`SELECT * FORM T1 JOIN T2 ON att1=att2 WHERE w1 and w2`   

# Running Experiments
* [invertindex.py](https://github.com/Joel-Q-Xu/OTJXT/blob/master/otjxt/invertindex.py)： Construct an inverted index     
* [VI.py](https://github.com/Joel-Q-Xu/OTJXT/blob/master/otjxt/VI.py)： Read processed data

  
In [otjxt.py](https://github.com/Joel-Q-Xu/OTJXT/blob/master/otjxt/otjxt.py), we run an equi-join on [TPC-H](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf) data. We only use the _order table and _customer table.
