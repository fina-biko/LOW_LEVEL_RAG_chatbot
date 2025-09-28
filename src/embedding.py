import re
from typing import Tuple, Union

from src.low_level_rag.extractor import PDFExtractor
from utilities.exception import PdfExtractionError, PreprocessError
from utilities.create_logger import create_logger
from src.low_level_rag.preprocess import TextPreprocessor
from src.chunking import chunk_text

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
logger=create_logger(name=__name__)
def embed_text(outer_list,model_name=SentenceTransformer("all-MiniLM-L6-v2"))->list:
    """
    Embed text chunks from a list of lists containing dictionaries with page numbers as keys and text chunks as values.

    Args:
        outer_list (list): A list of lists where each inner list contains dictionaries with page numbers as keys and text chunks as values.

    Returns:
        list: A list of lists containing dictionaries with page numbers, embedded chunks, and original chunks.
    """
    # This will hold the final result
    final_outer_list = []
    try:

        for inner_list in outer_list:
            list_of_tokens = []
            for first_dict in inner_list:  # the number of dict in each inner list is the number of chunks
                # unpack the dictionary
                logger.info(f"unpacking this dict: {first_dict}")
                page = list(first_dict.keys())[0]
                text = list(first_dict.values())[0]  # the first chunk
                logger.info(f"unpacked page {first_dict}: {page}, text chunk: {text}")
                logger.info(f"calling the model {model_name} to embed the chunk")
                embedded_chunk =  model_name.encode(text)
                logger.info(f"successfully embedded chunk: ")
                # say it returns sth
                # append this embedded chunk and the page number and the original chunk as dict to this list
                list_of_tokens.append({page: page, "original_chunk": text,"embedded_chunk": embedded_chunk })
                logger.info(f"appended  embedded chunk to list_of_tokens: {list_of_tokens}")
            final_outer_list.append(list_of_tokens)

        #log the shape of the outer list
        logger.info(f"final outer list with embedded chunks: {final_outer_list}")

        return final_outer_list

    except Exception as e:
       
        logger.error(f"Error occurred during embedding: {e}")
        return []
    

    
if __name__ == "__main__":
    logger.info("Starting the preprocessing pipeline...")
    # Example usage with the refactored class
    try:
        # Assuming PDFExtractor is available from your original code.
        # It is imported but not defined in the provided snippet.
        # This part of the code is for demonstration of the new class.
         filepath_1=r"C:\Users\User\Desktop\michelle.pdf"
         filepath = r"C:\\Users\\User\\Downloads\\Cloud Concepts [Slides].pdf"
         filepath2=r"C:\Users\User\Downloads\Cloud Concepts [Slid].pdf"
         pdf_extractor = PDFExtractor(filepath_1)
         extracted_data = pdf_extractor.extract()
   
  
        # Initialize the preprocessor
         preprocessor = TextPreprocessor()

        # # --- Test Case 1: Raw String Input ---
        #  raw_string = "This is a test.\n\nIt has some\n extra spaces and punctuation ."
        #  cleaned_string = preprocessor.process_text(raw_string)
        #  print("--- Test Case 1: Raw String ---")
        #  print(f"Original: '{raw_string}'")
        #  print(f"Cleaned:  '{cleaned_string}'")
        #  print("-" * 20)

        # --- Test Case 2: List of Tuples Input ---
         tuple_list = [(1, "First page text.\n This has a hyphen-\nated word."), (2, "Second page text with a space   problem.")]
         cleaned_from_tuples = preprocessor.process_text(tuple_list)
         print("--- Test Case 2: List of Tuples ---")
         print(f"Original: '{tuple_list}'")
         print(f"Cleaned:  '{cleaned_from_tuples}'")
         print("-" * 
                  20)

        # --- Test Case 3: Error Handling (Invalid Type) ---
        #  print("--- Test Case 3: Error Handling ---")
         text=chunk_text(cleaned_from_tuples)
         print(len(text))
         print("getting into embedding function")
         embedded_text=embed_text(text)
         print(len(embedded_text))

    except Exception as e:
     logger.error("An unexpected error occurred in the main execution block.",exc_info=True)
        


            
    