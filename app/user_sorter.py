from app.loc_worker import Location_Worker

def User_Sorter(gender, ed, coastal, reg):

    m = list([u'1', u'0'])
    res = [(i, j, k, l) for i in m for j in m for k in m for l in m]

    i = 0

    for i in range(len(res)):
        if (gender, ed, coastal, reg) == res[i]:
            return i 
        
