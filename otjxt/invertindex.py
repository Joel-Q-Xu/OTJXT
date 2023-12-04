

def invert_index(attrw,file,outfile):
    dct = dict()

    with open(file, 'r') as f:
        attribute_name = f.readline().strip('\n').split('|')
        l = len(attrw)
        print(l)
        n = []
        for m in range(l):
            for i in range(len(attribute_name)):
                if (attribute_name[i] == attrw[m]):
                    n.append(i)

        print(n)

        for line in f:
            attribute_value = line.strip('\n').split('|')
            tmp_id=attribute_value[0]
            for m in range(l):
                tmp_id += "|"+attribute_name[n[m]] +"|"+ attribute_value[n[m]]
            tmp_value = [attribute_name[i] +"="+ attribute_value[i]
                         for i in range(1, len(attribute_name))]



            for value in tmp_value:
                dct[value] = dct.get(value, []) + [tmp_id]




    with open(outfile, 'w') as f:
        for key, value in dct.items():
            lst = [key] + value
            f.write("|".join(lst) + "\n")


# attrw=["custkey","selectivity"]
# file1 = "./customer100.tbl"
# outfile1="./incustomer100.tbl"
# file2 = "./orders100.tbl"
# outfile2="./inorders100.tbl"

# file1 = "./testa.tbl"
# outfile1="./intesta.tbl"
# file2 = "./testb.tbl"
# outfile2="./intestb.tbl"
# attrw=["tid","abc"]

attrw=["custkey"]
file1 = "data/0.05/customer.tbl"
outfile1="indata/0.05/incustomer.tbl"
file2 = "data/0.05/orders.tbl"
outfile2="indata/0.05/inorders.tbl"

# attrw="custkey"
# file1 = "data/0.09/customer.tbl"
# outfile1="indata/0.09/incustomer.tbl"
# file2 = "data/0.09/orders.tbl"
# outfile2="indata/0.09/inorders.tbl"
invert_index(attrw,file1,outfile1)
invert_index(attrw,file2,outfile2)


