from os import listdir
from os.path import isfile, join
from config import SQL_QUERIES_FOLDER
import re
from .log import LOGGER


def get_sql_files(folder):
    '''Fetch all SQL query files in folder.'''
    files = [folder + '/' + f for f in listdir(folder) if isfile(join(folder, f)) if '.sql' in f]
    return files

def read_sql_from_files(folder):
    try:
        '''Read SQL query from .sql file.'''
        files = get_sql_files(folder)
        sql_queries = {}
        for file in files:
            sql_file = open(file, 'r')
            query = sql_file.read()
            name = re.split('/|\.', sql_file.name)[1] 
       
            sql_queries[name] = query
            sql_file.close()
        return sql_queries
    except Exception as e:
         LOGGER.error(e)
         raise e
    


queries = read_sql_from_files(SQL_QUERIES_FOLDER)