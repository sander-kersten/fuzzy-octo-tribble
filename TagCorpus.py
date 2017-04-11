from readtxt import readtxt
from nltk import ToktokTokenizer
tokenize = ToktokTokenizer().tokenize

def IndexLastComma(Tokens):
    assert ',' in Tokens
    i = len(Tokens)-1
    while Tokens[i] != ',':
        i-=1
    return i

def RemoveDoubleTags(Text):
    while ("><" in Text):
        try:
            OpenTag = ("<"+Text.split("><")[0].split("<")[-1]+">")
            CloseTag = OpenTag.replace("<", "</")
            NewText = Text.split(OpenTag*2, 1)
            NewText[1] = NewText[1].replace(CloseTag, "", 1)
            Text = NewText[0]+OpenTag+NewText[1]
        except IndexError:
            return Text
    return Text

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

Categories=dict([(x[0], x[-1]) for x in readtxt('/home/sander/Studie/Stage/fuzzy-octo-tribble/DutchDataUMLS/Concept_categories_UMLS.txt')[1:]])
Found=list(set(readtxt('/home/sander/Studie/Stage/fuzzy-octo-tribble/FoundConcepts.txt')))
FoundConcepts=dict()
CUI=dict()
for F in Found:
    cui = F[0]
    Lines = eval(F[2])
    Concept = F[1]
    CUI[Concept] = cui
    for L in Lines:
        if L not in FoundConcepts:
            FoundConcepts[L] = [Concept]
        else:
            FoundConcepts[L].append(Concept)

TextLines = open('/home/sander/Studie/Stage/fuzzy-octo-tribble/Wikicorpus/FULL_WIKI').read().split('\n')

for FC in FoundConcepts:
    concepts = FoundConcepts[FC]
    for concept in concepts:
        variants = Variants(concept)
        for variant in variants:
            if variant in TextLines[int(FC)-1]:
                cui = CUI[concept]
                try:
                    category = Categories[cui]
                    NewLine = TextLines[int(FC)-1].replace(variant, '<'+category+'>'+concept+'</'+category+'>')
                    TextLines[int(FC)-1] = NewLine
                except KeyError:
                    print("No category found for CUI "+cui+" ("+concept+")")
                    continue

NewText = '\n'.join([RemoveDoubleTags(l) for l in TextLines])
with open('/home/sander/Studie/Stage/fuzzy-octo-tribble/Wikicorpus/FULL_WIKI_TAGGED', 'w') as F:
    F.write(NewText)

