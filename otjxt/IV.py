from dataclasses import dataclass
from typing import List, Tuple
@dataclass
class IV:
    id:str
    attrw_list:List[str]

def read_table(attrw,infile):
    iv=[]
    with open(infile, 'r') as f:
        attribute_name = f.readline().strip('\n').split('|')
        l=len(attrw)
        print(l)
        n=[]
        for m in range(l):
            for i in range(len(attribute_name)):
                if (attribute_name[i] == attrw[m]):
                    n.append(i)

        print(n)



        for line in f:
            tmp_value = []
            attribute_value = line.strip('\n').split('|')
            tmp_id = attribute_value[0]
            for m in range(l):
                tmp_value.append(attribute_name[n[m]] +"="+ attribute_value[n[m]])

            iv.append(IV(tmp_id,tmp_value))
    return iv


# infile="./customer100.tbl"
# attrw=['custkey','selectivity']

# infile= "./testa.tbl"
#
# attrw=["tid","abc"]
# iv=read_table(attrw,infile)
# print(iv)
