import re
from typing import Tuple, Union

from src.low_level_rag.extractor import PDFExtractor
from utilities.exception import PdfExtractionError, PreprocessError
from utilities.create_logger import create_logger

# Use a module-level logger for all class methods
logger = create_logger(name=__name__)

class TextPreprocessor:
    """
    A class for performing a text cleaning pipeline.

    Encapsulates text preprocessing steps, handling different input types,
    and managing potential exceptions. The pipeline applies a series of
    regular expression-based cleaning routines to text.
    """
    def _get_input_shape(self,data):
      """
      Detects if the input data is a 1D list of tuples or a 2D list of lists.

      Args:
         data (list): The input data structure.

      Returns:
         str: '1D' or '2D' or 'Invalid Input'
      """
      if not isinstance(data, list) or not data:
         return 'Invalid Input'  # Not a list or is empty
      # Get the first element of the list passed 
      first_element = data[0]

      # Check if the first element is a tuple, indicating a 1D list of (page, text)
      if isinstance(first_element, tuple) and len(first_element) == 2 and isinstance(first_element[0], int):
         logger.info(f"shape detected as {len(data)}D list of tuples")
         print("Detected 1D list of tuples")
         return '1D'  # e.g., [(1, 'text1'), (2, 'text2')]

      # Check if the first element is a list, indicating a 2D list of lists
      elif isinstance(first_element, list):
         logger.info(f"shape detected as {len(data)} list of lists")
         # Optional: Further check if the nested list also follows the expected structure
         if first_element and isinstance(first_element[0], tuple):
               return '2D'  # e.g., [[(1, 'text1')], [(1, 'text3')]]
         return '2D' # Assume 2D if the first element is a list

      else:
         return 'Invalid Input'
    
    def _clean_text(self, text: str) -> str:
        """
        Applies a series of cleaning and normalization steps to a single string.
        
        Args:
            text (str): The raw text string to clean.

        Returns:

            str: The cleaned, normalized text.

        """
        # 1. Replace double newlines with a single space
        cleaned = text.replace("\n\n", " ")
        # 2. Replace single newlines with a single space
        cleaned = cleaned.replace("\n", " ")
        # 3. Remove hyphen + whitespace word breaks (e.g., "pri-\nmary" -> "primary")
        cleaned = re.sub(r"-\s+", "", cleaned)
        # 4. Collapse multiple spaces into a single space
        cleaned = re.sub(r"\s+", " ", cleaned)
        # 5. Normalize spaces before punctuation
        cleaned = re.sub(r"\s+([.,!?;:])", r"\1", cleaned)
        # 6. Strip leading and trailing spaces
        cleaned = cleaned.strip()
        return cleaned


    def process_text(self,  text: list[Tuple[int, str]]) -> list:
        """

                    Input: The list of tuples from Step 1.

            Method: reprocessor

            Iterate through (page_num, raw_text) tuples.

            Call the cleaning function only on raw_text.

            Crucially, return the cleaned result paired with the page number.

            Output: A list of tuples with cleaned text: [(page_num, cleaned_text), (page_2_num, cleaned_text), ...]
                Processes a list of (page_num, text) tuples or a 2D list of such tuples,    
                """
        #log the shape of the text
        shape = self._get_input_shape(text)
        if shape:
            try:
                logger.info(f"Input text  detected is: {shape}")
                if shape not in ['1D', '2D']:
                  raise PreprocessError(message="Input text must be a list of (page, text) tuples or a 2D list of lists.")
                if shape == '1D':
                    cleaned_tuples = []

                    for data in text:
                            page = data[0]
                            content = data[1]
                            logger.debug(f"Page: {page}, Content snippet: {content[:30]}...")
                            cleaned_content = self._clean_text(content)
                            logger.debug(f"Cleaned Content snippet: {cleaned_content[:30]}...")
                            cleaned_tuples.append((page, cleaned_content))
                    return cleaned_tuples
        
                elif shape == '2D':
                    cleaned_tuples = []
                for sublist in text:
                    for data in sublist:
                        page = data[0]
                        content = data[1]
                        logger.debug(f"Page: {page}, Content snippet: {content[:30]}...")
                        cleaned_content = self.clean_text(content)
                        logger.debug(f"Cleaned Content snippet: {cleaned_content[:30]}...")
                        cleaned_tuples.append([(page, cleaned_content)])
                return cleaned_tuples
            except Exception as e:
                logger.error(f"Error determining input shape: {e}")
                raise PreprocessError(message="Could not determine input shape.", exception=e)
        else:
            raise PreprocessError(message="Input text structure is not recognized.")

    
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

    except Exception as e:
     logger.error("An unexpected error occurred in the main execution block.")
        
