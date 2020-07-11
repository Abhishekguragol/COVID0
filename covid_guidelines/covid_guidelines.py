from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, OrGroup
from whoosh import index
import os.path
import os
from tika import parser


def add_all_docs():
    if not os.path.exists("./covid_guidelines/indexdir"):
        os.mkdir("./covid_guidelines/indexdir")

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored = True), abstract = TEXT(stored = True))

    ix = index.create_in("./covid_guidelines/indexdir", schema)

    if not os.path.exists('./media/pdfs'):
        raise Exception('All the PDFs should be in folder named "pdfs"')

    docs = os.listdir('./media/pdfs')
    for doc in docs:
        writer = ix.writer()
        file = './media/pdfs/'+doc
        # Parse data from file
        file_data = parser.from_file(file)
        # Get files text content
        text = file_data['content']
        
        writer.add_document(title=doc[:doc.index('.')], content=text,
        path=file,
        abstract='''''')
        writer.commit()

def add_single_doc(doc_path,title):

    ix = index.open_dir("./covid_guidelines/indexdir")
    writer = ix.writer()
    file = doc_path
    # Parse data from file
    file_data = parser.from_file(file)
    # Get files text content
    text = file_data['content']
    
    writer.add_document(title=title, content=text,
    path=file,
    abstract='''''')
    writer.commit()

# Run find_docs(query) in routes.py 
def find_docs(key_string):
    ix = index.open_dir("./covid_guidelines/indexdir")
    return_dict = {}
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse(key_string)
        results = searcher.search(query, terms=True)

        # TODO: change paths for new dir structure
        for r in results:
            return_dict[r['title']] = "./media/"+r['path']
    return return_dict


#print(find_docs('Hospital'))