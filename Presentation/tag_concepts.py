from readtxt import *
from nltk import ToktokTokenizer
from unidecode import unidecode

WikiFile = '/home/sander/Studie/Stage/fuzzy-octo-tribble/Entities/FULL_WIKI'
ConceptsFile = '/home/sander/Studie/Stage/fuzzy-octo-tribble/Entities/Concepts_UMLS.txt'
tokenize = ToktokTokenizer().tokenize
Lines = [x.strip() for x in open(WikiFile).read().split('\n') if x.strip() != ""]
Concepts = dict(readtxt(ConceptsFile))
TokenizedConcepts = [(tokenize(unidecode(Concepts[c])), c) for c in Concepts]

def tag_line(Text, TokenizedConcepts={}):
    Tokens = tokenize(unidecode(Text))
    newText = []
    Found = False
    FoundTokens = []
    i = 0
    T = 0
    while (T < len(Tokens)):
        if Found:
            if (len(Candidates) == 1 and len(Candidates[0][0]) == 1):
                cui=Candidates[0][1]
                newText.append("<concept cui='"+cui+"' category=''>")
                newText += FoundTokens
                newText.append("</concept>")
                FoundTokens = []
                i=0
                Found = False
            elif len(Candidates) > 1:
                NewCandidate = []
                for C in Candidates:
                    j=0
                    J=0
                    if NewCandidate == [] and len(C[0]) == 1:
                        NewCandidate = C
                    else:
                        for tok in C[0][1:]:
                            if tok.lower() != Tokens[T+j].lower(): break
                            j+=1
                        if j == len(C[0]) - 1 and j > J:
                            J=j
                            NewCandidate = C
                try:
                    cui=NewCandidate[1]
                    FoundTokens = NewCandidate[0]
                    newText.append("<concept cui='"+cui+"' category=''>")
                    newText += FoundTokens
                    newText.append("</concept>")
                    Found = False
                    T+=len(FoundTokens)-1
                    FoundTokens = []
                except IndexError:
                    newText += FoundTokens
                    FoundTokens = []
                    Found = False
        if T < len(Tokens):
            if Tokens[T].upper() == Tokens[T]:
                Candidates = [tc for tc in TokenizedConcepts if tc[0][0] == Tokens[T]]
            else:
                Candidates = [tc for tc in TokenizedConcepts if tc[0][0].lower() == Tokens[T].lower()]
            if Candidates == []:
                i = 0
                newText.append(Tokens[T])
            else:
                Found = True
                i+=1
                FoundTokens.append(Tokens[T])
            T += 1
        else:
            newText += FoundTokens
     ## End of main loop
    if Found:
        if (len(Candidates) == 1 and FoundTokens == Candidates[0]) or FoundTokens in [c[0] for c in Candidates]:
            if len(Candidates) == 1:
                cui=Candidates[0][1]
            else:
                cui=Candidates[[c[0] for c in Candidates].index(FoundTokens)][1]
            newText.append("<concept cui='"+cui+"' category=''>")
            newText += FoundTokens
            newText.append("</concept>")
            FoundTokens = []
            i=0
            Found = False
    return ' '.join(newText)


#TestConcepts = {"ziekte van Alzheimer": "C2", "ziekte van Pfeiffer": "C1", "ziekte": "C3"}

TestSentence = "De ziekte van alzheimer kan niet worden genezen, in tegenstelling tot de ziekte van pfeiffer."
print(tag_line(TestSentence, TokenizedConcepts))

#TestSentence = "De ziekte kan niet worden genezen."
#print tag_line(TestSentence, TestConcepts)

print("Tagging "+str(len(Lines))+" lines")
j=258
for l in Lines[258:]:
    j+=1
    if not (l.startswith("<doc") or l.startswith('</doc')):
        l = tag_line(l.strip(), TokenizedConcepts)+'\n\n'
    with open('Tagged.1.txt', 'a') as F:
        F.write(l)
    print("Tagged "+str(j)+" of "+str(len(Lines))+" lines.")
