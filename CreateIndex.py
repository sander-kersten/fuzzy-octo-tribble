from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("WikiIndex", schema)
writer = ix.writer()
Content = open('/home/sander/Studie/Stage/fuzzy-octo-tribble/Wikicorpus/FULL_WIKI_Sentences').read().split('\n')

for i in range(len(Content)):
    writer.add_document(title=u"Wiki"+str(i+1), path=u"/wiki"+str(i+1), content=Content[i])

writer.commit()
