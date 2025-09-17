

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
from abc import ABC, abstractmethod
from typing import List, Tuple
#add parent root to path

from utilities.create_logger import create_logger




class DataExtractor(ABC):

    """
    Abstract base class for data extractors.
    Subclasses must implement the extract method.
    Each extractor operates on a file specified by 'filepath'.
    Each extractor should know how to preprocess its specific file type, e.g., PDF, DOCX, TXT.
    """

    def __init__(self,filepath:str):
        self.filepath=filepath

   

    @abstractmethod
    def extract(self) -> List[Tuple[str, str]]:
        """
        Extract data from the file.
        Returns:
            List of (metadata, text) tuples.
        """
        pass



class PDFExtractor(DataExtractor):
    """
    Extract text and metadata from a PDF file.

    args:
        filepath: str : path to the pdf file
    
    returns:
        List[Tuple[str,str]]: list of tuples containing the text and metadata

    
    """

    
    
    def extract(self) -> List[Tuple[str, str]]:
        
        # Implement PDF extraction logic here
        return [("Sample PDF text", "metadata")]
    


if __name__ == "__main__":
    logger = create_logger(__name__,level=logging.INFO)
  
    logger.info("This is an info message from extractor module.")
    pdf_extractor = PDFExtractor('sample.pdf')
    data = pdf_extractor.extract()
    logger.info(f"Extracted data from PDF: {data}")