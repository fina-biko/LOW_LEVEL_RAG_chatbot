INPUT: a networking pdf,etc, USER-question
OUTPUT:answer from a chatbot

pseudocode:

# 1.load the pdf
    extract text using pypdf module page per page
    this text should be returned as  list of list, each page in alist

    edge cases: we might have multiple extractors , pdf, word so we should have an ** extractor abstract class  to be subclassed by extractors **

    exractors: PDF extractor, word extractor

    logging module: logs al activites of the file. settings of the log file in config

    exception handling: input not a path to file, 
                        error loading the pdf

# 2.Preprocess the text
    clean the text to remoe white spaces

# 3.create chunks for the texts
   create chunk with overlap, 
    
# 4. pass the chunks to an embedding model


# 5.store the embeddings in a faiss vector db

# 6. create the retriever


#

#

  
