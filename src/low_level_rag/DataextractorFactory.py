
import os
from utilities.create_logger import create_logger
import logging

logger= create_logger(__name__,level=logging.INFO)

class ExtractorFactory:
    #have an empty dictionary to store the extractors
    _registry : dict[str, type] = {}

    #have a class that regosters the extractors
    # it should accept  thename of the class and add it to the registry, and the filepath 
    #giiven to the class so it knows the filetype
    @classmethod
    def register_extractor(cls, ext: str, class_type: type) -> dict[str, type]:
        #here the cls refers to the ExtractorFactory class itself
        #take the extension
        #take the class itself, using class__name__
        #register it as key value pair
        cls._registry[ext]=class_type
        logger.info(f"registered extractor for {ext} : {class_type}")
        return cls._registry
    
    # a method to show all the registred extractors
    @classmethod
    def show_registered_extractors(cls):
        logger.info(f"Registered extractors: {cls._registry}")
        return cls._registry

    @classmethod
    def create_extractor(cls, filepath: str):
        #should just take the filepath
        #extract file ext from the filepath
        ext=os.path.splitext(filepath)[1]
        logger.info(f"Creating extractor for file: {filepath} with extension: {ext}")
        #check if the file ext is in the registry
        if ext in cls._registry:
            class_type=cls._registry[ext]
            logger.info(f"Found extractor class {class_type} for extension {ext}")
            #return an instance of the class
            return class_type('filepath')
        else:
            error_msg=f"No extractor registered for extension: {ext}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        #if it is, return the class type and call th instance of the class
        #if not, raise an exception
        #
            





            
if __name__ == "__main__":
    # Register a dummy extractor using a built-in class (e.g., list)
    #print(ExtractorFactory.register_extractor(".pdf", list))
    #print(ExtractorFactory.register_extractor(".txt", dict))

    #show the registered extractors
    print(ExtractorFactory.show_registered_extractors())
    print("---------------------------------------------------")
    
    print(ExtractorFactory.create_extractor("sample.pdf"))
    print("---------------------------------------------------")

   #show the registered extractors
    print(ExtractorFactory.show_registered_extractors())


   