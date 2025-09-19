 


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
    def extract(self) -> List[Tuple[str, str]]:
        #take a file path and extracts text
        pass


class PDFExtractor(DocumentExtractor):
    extension = ".pdf"
    """   what do we need for a pdf? 
    we need to conirm if the pdf path is a valid, but this is the work of the
    factory, to check if the visitor it gets is valid before directing it to the worker
    else the worker in the factory may be letting in an alshababa, so it is 
    done in the factory class"""

    
    def extract(self, ) -> List[Tuple[str, str]]:
        # Dummy implementation for PDF extraction
        return [("this is a Sample PDF text", "metadata")]
    
if __name__ == "__main__":
    filepath=r"C:\Users\User\Downloads\Cloud Concepts [Slides].pdf"
    pdf_extractor = PDFExtractor(filepath)
    extracted_data = pdf_extractor.extract()
    print(extracted_data)