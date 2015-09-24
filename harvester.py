from BeautifulSoup import BeautifulSoup
import logging
import requests
import multiprocessing

# Set the files to UTF-8
import sys
import os
reload(sys)
sys.setdefaultencoding("utf8")  # @UndefinedVariable

# Configure a logger for the entire script
logFormat = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logFormat)
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('harvester.log', mode='w')
file_handler.setFormatter(logging.Formatter(logFormat))
log.addHandler(file_handler)

ENDPOINT = "http://oai.bn.pt/servlet/OAIHandler"

class Harverster(object):
    def __init__(self, set_name):
        self.set_name = set_name
        
    def go(self):
        # Use a session to keep alive the connection
        session = requests.Session()
        
        # Set everything for the first page
        page_index = 0
        has_next = True
        payload = {'verb':'ListRecords',
                   'metadataPrefix':'marcxchange',
                   'set':self.set_name}
        
        while (has_next):
            # Get the page
            content = session.get(ENDPOINT, params=payload).text
            
            # Save it
            directory = 'data/{}'.format(self.set_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            output_file_name = '{}/{}.xml'.format(directory, page_index)
            with open(output_file_name, 'wb') as output_file:
                output_file.write(content)

            # Load the XML
            soup = BeautifulSoup(content)
            
            # Print the number of records
            records = soup.findAll('record')
            log.info('[{}] Got {} records for page {}'.format(self.set_name, len(records), page_index))

            # Look for a continuation token
            token_element = soup.find('resumptiontoken')
            has_next = (token_element != None)
            if has_next:
                page_index = page_index + 1
                payload = {'verb':'ListRecords',
                           'resumptionToken':token_element.string}
                
        session.close()

def harvester_thread(parameters):
        set_name = parameters['set_name']
        log.info('[{}] Starting harvester'.format(set_name))
        harvester = Harverster(set_name)
        harvester.go()
        log.info('[{}] Finished harvesting'.format(set_name))
        
if __name__ == '__main__':
        
    # Create the tasks
    tasks = []
    for set_name in ['catalogo', 'bndlivre', 'porbase']:
        tasks.append({'set_name': set_name})
    
    # Go !
    pool = multiprocessing.Pool(processes=4)
    pool.map(harvester_thread, tasks)
    pool.close()
    pool.join()
