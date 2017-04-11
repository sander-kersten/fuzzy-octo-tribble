def readtxt(File):
    Txt = open(File).read().split('\n')
    if '\t' not in Txt[0]:
        Txt = Txt[1:]
    if '\t' not in Txt[-1]:
        Txt = Txt[:-1]
    n = Txt[0].count('\t')
    assert all([n == t.count('\t') for t in Txt])
    return [tuple(t.split('\t')) for t in Txt]