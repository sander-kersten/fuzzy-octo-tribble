import whoosh.index as index
from readtxt import readtxt
from whoosh.qparser import QueryParser
from nltk import ToktokTokenizer
#from pattern.nl import attributive, predicative, parse

tokenize = ToktokTokenizer().tokenize

def IndexLastComma(Tokens):
    assert ',' in Tokens
    i = len(Tokens)-1
    while Tokens[i] != ',':
        i-=1
    return i


def Variants(Concept):

    TC = tokenize(Concept)

    # Lowercase all tokens except for capitalized abbreviations  
    TokenizedConcept = [] 
    for Token in TC:
        if Token.upper() == Token:
            TokenizedConcept.append(Token)
        else:
            TokenizedConcept.append(Token.lower())    

    Variants = [Concept]
    
    # First variant removes specification between brackets.
    # But is this always sound???

    if ('(' in TokenizedConcept and ')' in TokenizedConcept):
        variant = []
        i=0
        while (TokenizedConcept[i] != '('):
            variant.append(TokenizedConcept[i])
            i+=1
        while (TokenizedConcept[i] != ')'): i+=1
        for Token in TokenizedConcept[i+1:]:
            variant.append(Token)
        Variants.append(' '.join(variant))

    # Second possibility puts the part after the last comma in front.
    # E.g. 'wolf, prarie-

    if (',' in TokenizedConcept):
        CommaIndex = IndexLastComma(TokenizedConcept)
        variant = TokenizedConcept[CommaIndex+1:] + TokenizedConcept[:CommaIndex]
        if TokenizedConcept[-1].endswith('-'):
            #Variants.append([variant[0]+variant[1]] + variant[2:])                             #  'Wolf, prairie-' != 'Prairie-wolf'
            Variants.append(' '.join([variant[0][:-1]+variant[1]] + variant[2:]))                         #  ['Prairiewolf'] == 'Prairiewolf'
        else:
            Variants.append(' '.join(variant))

    # TODO: Inflection of adjectives: 'kooldioxide verhoogd' => 'verhoogde kooldioxide'  (And more)

    if ('-' in Concept):
        Variants.append(Concept.replace('-', ''))

    return Variants


def SearchConcept(Concept, Parser):
    s = myindex.searcher()
    Found = []
    for V in Variants(Concept):
        q = Parser.parse(V)
        Found += [str(x)[:-3].split('wiki')[-1].split("'")[0] for x in list(s.search(q, limit=None))]
    return Found

Concepts = readtxt('DutchDataUMLS/Concepts_UMLS.txt')[1:153862]
myindex = index.open_dir("WikiIndex")
qp = QueryParser("content", schema=myindex.schema)
FoundConcepts = []
c=1

OutFile = open('FoundConcepts.txt', 'a')

for C in Concepts:
    print(str(c)+" of "+str(len(Concepts))+" processed.\n")
    Found = SearchConcept(C[1], qp)
    if Found != []:
        FoundConcepts.append((C[0], C[1], Found))
        OutFile.write(C[0]+'\t'+C[1]+'\t'+str(Found)+'\n')
    c+=1

OutFile.close()


"""
LineDict = {}

for F in FoundConcepts:
    for l in F[2]:
        if l not in LineDict:
            LineDict[l] = [(F[0], F[1])]
        else:
            LineDict[l].append((F[0], F[1]))

with open('Lines_Concepts.txt', 'w') as F:
    for L in LineDict:
        F.write(L+'\t'+

"""
