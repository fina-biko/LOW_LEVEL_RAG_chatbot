
import os
folders=[
    'docs',
    'utilities',
    'config',
    'logs',
    'src',
    'src/low_level_rag',

   

]
files=[

     'notebook.ipynb',
    'pyproject.toml',
    'gitignore',
    'README.md',
    'docs/design.md',
     'src/__init__.py',
    #'src/low_level_rag/__init__.py',
    'src/low_level_rag/extractor.py',
    'src/low_level_rag/DataextractorFactory.py',
    'src/preprocess.py',
    'src/chunking.py',
    'src/embedding.py',
    'src/vector_store.py',
    
    'config/config.yaml',
    'utilities/create_logger.py',
     'utilities/__init__.py',
    'utilities/exception.py',
        
    'utilities/yaml_utils.py',
    'logs/app.log'

    
   
    

]

def create_folders():
    """
    for folder string  in folders:
    make it an actual folder by using os.makedir

    for file string in files:
    check if the file actually exists
    if not ope the file for editing
    
    """
    for dir in folders:
        os.makedirs(dir,exist_ok=True)


def create_files():
    for file in files:
        if not os.path.exists(file):
            with open(file,'w') as f:
                pass
        else:
           print("file already exists")


if __name__=="__main__":
    create_folders()
    create_files()