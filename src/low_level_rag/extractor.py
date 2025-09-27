 


from abc import ABC, abstractmethod
from typing import List, Tuple
from utilities.create_logger import create_logger
import logging

from utilities.exception import PdfExtractionError


logger = logging.getLogger(__name__)


class DocumentExtractor(ABC):
    extension: str  # Expected to be defined in subclasses

    def __init__(self,filepath:str) -> None:
        super().__init__()
        self.filepath=filepath
       


    #any time a subclass inherits from  you , push it to be reigistred at the factory registry
    def __init_subclass__(cls, **kwargs: dict):
        super().__init_subclass__(**kwargs)
        #get the name of the subclass when it inheirits from DocumentExtractor
        name=cls.__name__
        #get the extension it has defined
        if not hasattr(cls,'extension'):
            raise PdfExtractionError(f"Subclass {name} must define an 'extension' class variable.")
        else:
           ext:str=cls.extension

        #call the registry and register the ext provided and the class type
        from .DataextractorFactory import ExtractorFactory
        ExtractorFactory.register_extractor(ext, cls)
        create_logger(__name__,level=logging.INFO).info(f"Registered  new extractor {name} for extension {ext}")
       

    @abstractmethod
    def extract(self) -> List[Tuple[int, str]]:
        #take a file path and extracts text
        pass


class PDFExtractor(DocumentExtractor):
    extension = ".pdf"


    
    def extract(self, ) -> List[Tuple[int, str]]:
        """
        Extract text from a PDF file, returning page numbers and their corresponding text.

        This method uses the `pypdf.PdfReader` to read the file located at 
        `self.filepath`. For each page in the PDF, the extracted text is stored 
        along with its page number as a tuple `(page_number, text)`. 

        Returns:
            List[Tuple[int, str]]: 
                A list of tuples where each tuple contains:
                - int: The page number (starting from 0).
                - str: The extracted text content of that page.

        Raises:
            Exception: If any error occurs during PDF reading or text extraction.

        Example:
            >>> extractor = PDFExtractor("sample.pdf")
            >>> pages = extractor.extract()
            >>> print(pages[0])
            (0, "This is the text from the first page...")
        """
        try:
            from pypdf import PdfReader
            reader_object=PdfReader(self.filepath)
            #list contains tuples of (page_number, text)
            extracted_text:list[Tuple[int, str]]=[]
            for pair in enumerate(reader_object.pages):

                extracted_text.append((pair[0], pair[1].extract_text()))
            logger.info(f"Successfully extracted text from PDF: {self.filepath}")



            return extracted_text       
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {self.filepath}, Error: {e}")
            raise PdfExtractionError(self.filepath, e)


if __name__ == "__main__":
    filepath_1=r"C:\Users\User\Desktop\michelle.pdf"
    filepath = r"C:\\Users\\User\\Downloads\\Cloud Concepts [Slides].pdf"
    filepath2=r"C:\Users\User\Downloads\Cloud Concepts [Slid].pdf"
    pdf_extractor = PDFExtractor(filepath2)
    extracted_data = pdf_extractor.extract()
   
    print(extracted_data)