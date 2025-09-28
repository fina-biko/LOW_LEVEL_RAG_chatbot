import re
from typing import Tuple, Union

from src.low_level_rag.extractor import PDFExtractor
from utilities.exception import PdfExtractionError, PreprocessError
from utilities.create_logger import create_logger
from src.low_level_rag.preprocess import TextPreprocessor

logger=create_logger(name=__name__)

def chunk_text(tuple_list, chunk_size=10, overlap=3):
    """
    Chunk text from a list of tuples containing (page_number, text).

    Args:
        tuple_list (list): List of tuples where each tuple is (page_number, text).
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of overlapping words between chunks.

    Returns:
        list: A list of lists containing dictionaries with page numbers as keys and text chunks as values.
    """
    # Configuration (This is for WORDS, which requires splitting the content)
    CHUNK_SIZE = 3 # 3 words
    OVERLAP = 1
    STEP = CHUNK_SIZE - OVERLAP  # 3 - 1 = 2 

    outer_list = []

    for each_tuple in tuple_list:
        # 💥 FIX 1: Resetting start_index for each new page is crucial
        start_index = 0 
        inner_list = []
        
        page = each_tuple[0]
        content = each_tuple[1]
        
        # 💥 FIX 2: Clean and split the content into WORDS
        # Clean up non-breaking spaces (\xa0) and extra whitespace before splitting
        #cleaned_content = content.replace('\xa0', ' ').replace('.', ' ').replace(',', ' ')
        words = [word for word in content.split() if word] # Get a list of actual words
        logger.info(f"this is words after splitting based on white space: {words}")

        logger.info(f"\n--- Processing Page {page} ---")
        logger.info(f"Content (Cleaned Words): {words}")

        # 💥 FIX 3: Loop condition checks against the length of the WORDS list
        while start_index < len(words):
            # Slice the list of WORDS, not the character string
            chunk_list = words[start_index : start_index + CHUNK_SIZE]
            logger.info(f"this is chunk list for {page}: {chunk_list}")
            
            # Stop if the chunk is empty (shouldn't happen with correct logic, but a safeguard)
            if not chunk_list:
                break
                
            # Join the chunk list back into a string for the desired dictionary format
            chunk_string = " ".join(chunk_list)
            inner_list.append({page: chunk_string})
            logger.info(f"Added chunk for page {page}: '{chunk_string}'")
            
            # Advance the index by the calculated STEP (which is 2 words)
            start_index += STEP
        
        outer_list.append(inner_list)

    print("\n--- Final Result ---")
    print(outer_list)
    return outer_list


     
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
         cleaned_from_tuples = preprocessor.process_text(extracted_data)
         print("--- Test Case 2: List of Tuples ---")
         print(f"Original: '{extracted_data}'")
         print(f"Cleaned:  '{cleaned_from_tuples}'")
         print("-" * 
                  20)

        # --- Test Case 3: Error Handling (Invalid Type) ---
        #  print("--- Test Case 3: Error Handling ---")
         chunk_text(cleaned_from_tuples)

    except Exception as e:
     logger.error("An unexpected error occurred in the main execution block.")
        
