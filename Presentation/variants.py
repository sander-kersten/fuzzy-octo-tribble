from nltk import ToktokTokenizer
from readtxt import readtxt
from pattern.nl import attributive, predicative, parse

ConceptsFile = '/home/sander/Studie/Stage/fuzzy-octo-tribble/Entities/Concepts_UMLS.txt'
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

    Variants = [TokenizedConcept]
    
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
            variant.append(Token)J
        Variants.append(variant)

    # Second possibility puts the part after the last comma in front.
    # E.g. 'wolf, prarie-

    if (',' in TokenizedConcept):
        CommaIndex = IndexLastComma(TokenizedConcept)
        variant = TokenizedConcept[CommaIndex+1:] + TokenizedConcept[:CommaIndex]
        if TokenizedConcept[-1].endswith('-'):
            #Variants.append([variant[0]+variant[1]] + variant[2:])                             #  'Wolf, prairie-' != 'Prairie-wolf'
            Variants.append([variant[0][:-1]+variant[1]] + variant[2:])                         #  ['Prairiewolf'] == 'Prairiewolf'
        else:
            Variants.append(variant)

    # TODO: Inflection of adjectives: 'kooldioxide verhoogd' => 'verhoogde kooldioxide'  (And more)

    return Variants

### Test Concepts
TestConcepts = ['bloedsomloopaandoening (NAO)', 'Wolf, prairie-', 'Techniek, celkweek-', 'Epstein-Barr-virustest', 'atrium-septumdefect', 'kooldioxide verhoogd', 'ACTH stimulatietest abnormaal', 'vagotomie, hoogselectieve', 'Weefsel- en orgaanverwijdering', 'vernauwing van slokdarm']

#print(Variants(TestConcepts[1]))

def GenerateVariants(ConceptsFile):
    Concepts = dict([(x,y) for (y, x) in readtxt(ConceptsFile)])
    for C in Concepts:
        # TODO

