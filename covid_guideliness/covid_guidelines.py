from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, OrGroup
from whoosh import index
import os.path
import os
from tika import parser


def add_all_docs():
    if not os.path.exists("./indexdir"):
        os.mkdir("./indexdir")

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored = True), abstract = TEXT(stored = True))

    ix = index.create_in("./indexdir", schema)

    if not os.path.exists('pdfs'):
        raise Exception('All the PDFs should be in folder named "pdfs"')

    docs = os.listdir('pdfs')
    for doc in docs:
        writer = ix.writer()
        file = 'pdfs/'+doc
        # Parse data from file
        file_data = parser.from_file(file)
        # Get files text content
        text = file_data['content']
        
        writer.add_document(title=doc[:doc.index('.')], content=text,
        path=file,
        abstract='''''')
        writer.commit()

def add_single_doc(doc_path,title):

    ix = index.open_dir("./indexdir")
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

def find_docs(key_string):
    ix = index.open_dir("./indexdir")
    return_dict = {}
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse(key_string)
        results = searcher.search(query, terms=True)

        for r in results:
            return_dict[r['title']] = r['path']
    return return_dict
