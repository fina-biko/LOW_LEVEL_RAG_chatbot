 


from abc import ABC, abstractmethod
from typing import List, Tuple


class DocumentExtractor(ABC):
    def __init__(self,filepath:str) -> None:
        super().__init__()
        self.filepath=filepath


    #any time a subclass inherits from  you , push it to be reigistred at the factory registry
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        DocumentExtractorFactory.register_extractor(cls.__name__, cls)
    @abstractmethod
    def extract(self, file_path: str) -> List[Tuple[str, str]]:
        pass


class PDFExtractor(DocumentExtractor):

    
    def extract(self, file_path: str) -> List[Tuple[str, str]]:
        # Dummy implementation for PDF extraction
        return [("Sample PDF text", "metadata")]