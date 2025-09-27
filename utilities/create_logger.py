import logging
import os


from utilities.yaml_utils import read_yaml_log_path

def create_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create and configure a logger.

    Args:
      
        level (int): The logging level (default is logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """

    filepath=read_yaml_log_path()

  # set the logger to have the name of the module
    logger = logging.getLogger(name)

    #give the logger the level of log
    logger.setLevel(level)

    # Create console handler and set level to the console handler
    #ch = logging.StreamHandler()
    #ch.setLevel(level)

      #create file handler and set level to file handler
    

    if 'log_file' in filepath:
        
        if  os.path.exists(filepath['log_file']):
            fh = logging.FileHandler(filepath['log_file'])
            fh.setLevel(level)
        else:
            fh = logging.FileHandler('logs/app.log')
            fh.setLevel(level)


    else:
        fh = logging.FileHandler('logs/app.log')
        fh.setLevel(level)
   

  
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to console handler
    fh.setFormatter(formatter)
    #ch.setFormatter(formatter)

    # Add console handler to logger
    if not logger.hasHandlers():
        logger.addHandler(fh)
        #logger.addHandler(ch)

        

    return logger

if __name__ == "__main__":
    logger = create_logger(name=__name__,level=logging.INFO)
    logger.info("Logger has been created successfully.")