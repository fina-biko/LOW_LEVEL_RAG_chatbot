 


from abc import ABC, abstractmethod
from typing import List, Tuple
from utilities.create_logger import create_logger
import logging


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
            raise ValueError(f"Subclass {name} must define an 'extension' class variable.")
        else:
           ext:str=cls.extension

        #call the registry and register the ext and the class type
        from .DataextractorFactory import ExtractorFactory
        ExtractorFactory.register_extractor(ext, cls)
        create_logger(__name__,level=logging.INFO).info(f"Registered  new extractor {name} for extension {ext}")
       

    @abstractmethod
    def extract(self) -> List[Tuple[int, str]]:
        #take a file path and extracts text
        pass


class PDFExtractor(DocumentExtractor):
    extension = ".pdf"
    """   what do we need for a pdf? 
    we need to confirm if the pdf path is valid, but this is the work of the
    factory, to check if the visitor it gets is valid before directing it to the worker.
    Else the worker in the factory may be letting in an invalid file, so it is 
    done in the factory class.

    So we should extract the data here and return each page as a tuple of (metadata and text.)
    the reader object returns the extracted text,in string format, so we can just return it as a tuple"""

    
    def extract(self, ) -> List[Tuple[int, str]]:
        # Dummy implementation for PDF extraction
        
        # Use a PDF library like PyPDF2 or pdfminer to extract text from PDF files
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
            #raise extration error
            raise e

if __name__ == "__main__":
    filepath_1=r"C:\Users\User\Desktop\michelle.pdf"
    filepath = r"C:\\Users\\User\\Downloads\\Cloud Concepts [Slides].pdf"
    pdf_extractor = PDFExtractor(filepath_1)
    extracted_data = pdf_extractor.extract()
   
    print(extracted_data)