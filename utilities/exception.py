# a base exception
# an exception handler
from utilities.create_logger import create_logger
import logging

class BaseCustomException(Exception):
    """
    arggs: message to print to the console
         the excption that occured, can be none

         actions: it logs the error 
         it print the error 
    
    
    """
    
    #all base exception will subclass this and must have thesse attributes
    def __init__(self, message:str,exception:Exception | None=None) :
        self.message=message
        self.exception=exception

        #just pass the message to the parent init because this is what will be printed
        super().__init__(message)

        #log the error whenever a subclass is instntiated
        #get the instancem, get the type of the instance that this the class object then  get the name of the class, the name
        # of the class is what will be logged, also get the module that this class redsides in
        #get the class of this instance
       
        
        
        class_name=self.__class__.__name__
        module_name=self.__class__.__module__

        #create  the logger object
        logger=create_logger(name=module_name,level=logging.ERROR)

        # now that the exception has been created, log the error. logger error has that abilty to log  bora tu u say it
        logger.error(msg=f"{self.message}  raised by {class_name} class  ",exc_info=self.exception or True)

        
        



class HandleException:
    def __init__(self,message:str,error:Exception):
        self.message=message
        self.error=error
        #to be used after error hs  been raised

        #log the error
        logger=create_logger(name=__name__,level=logging.ERROR)
        logger.error(msg=self.message,exc_info=True)
        #print a friendly message to the console
        print  (self.message)

class PdfExtractionError(BaseCustomException):
    pass
class DataFactoryError(BaseCustomException):
    pass



if __name__=="__main__":
    try:
        try:
            1/0
        except Exception as e:
            #aftercatchng this error what do we do: we raise it
            raise PdfExtractionError(f" Extracting pdf  has failed with >>>>>>{e}")  from e
    except PdfExtractionError as e:
        HandleException(" Error has occured",error=e)#this will be printed first
        #then the error we had excepted , plus the arguments we had passed will be printed next




        

    