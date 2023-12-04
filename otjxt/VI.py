from dataclasses import dataclass
from typing import List, Tuple


def my_function(id_list: List[Tuple]):
    pass
@dataclass

class VI  :
    keyword: str
    id_list:List[List]


def read_intable(attrw,infile):
    vi=[]
    l=len(attrw)

    with open(infile, 'r') as f:
        for line in f:
            tmp_id=[]

            attribute_value = line.strip('\n').split('|')
            tmp_value = attribute_value[0]
            for i in range(1, len(attribute_value)):
                if(i%(2*l+1)==1):
                    li=[]
                    for m in range(2*l+1):
                        li.append(attribute_value[i+m])


                    tmp_id.append(li)


            vi.append(VI(tmp_value,tmp_id))



    return vi



# infile="./incustomer100.tbl"
# attrw=['custkey','selectivity']


# infile= "./intesta.tbl"
#
# attrw=["tid","abc"]
#
# vi=read_intable(attrw,infile)
# print(vi)

