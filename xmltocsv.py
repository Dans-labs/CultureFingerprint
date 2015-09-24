from BeautifulSoup import BeautifulSoup
import logging
import multiprocessing
import glob
import csv
import bz2

# Set the files to UTF-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")  # @UndefinedVariable

# Configure a logger for the entire script
logFormat = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logFormat)
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)
#file_handler = logging.FileHandler('xmltocsv.log', mode='w')
#file_handler.setFormatter(logging.Formatter(logFormat))
#log.addHandler(file_handler)

class XML2CSV(object):
    def __init__(self, set_name):
        self.set_name = set_name
        
    def go(self):
        # Get a list of files to process
        directory = 'data/{}'.format(self.set_name)
        input_files = glob.glob("{}/*.xml.bz2".format(directory))
        log.info('[{}] Found {} input files'.format(self.set_name, len(input_files)))
        
        # Prepare output
        output_file = bz2.BZ2File("{}.csv.bz2".format(directory), 'wb', compresslevel=7)
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"')
        
        for input_file in sorted(input_files):
            log.info('[{}] Processing {}'.format(self.set_name, input_file))
        
            content = bz2.BZ2File(input_file).read()
            soup = BeautifulSoup(content)
            records = soup.findAll('record')
            for record in records:
                # Get the identifier and skip if not found
                identifier = record.header.identifier
                if identifier == None:
                    continue
                
                # Get the date of publication and skip if not found
                date_pub = record.find('mx:datafield', tag="210")
                if date_pub != None:
                    date_pub = date_pub.find('mx:subfield', code='d')
                if date_pub == None:
                    continue
            
                # Get the UDC numbers
                UDCs = [entry.find('mx:subfield', code='a') for entry in record.findAll('mx:datafield', tag="675") if entry != None]
                    
                # Write one row per identifier/date/udc
                for UDC in UDCs:
                    if UDC != None:
                        row = [identifier.string, date_pub.string, UDC.string]
                        csv_writer.writerow(row)                     

        output_file.close()
        
def xmltocsv_thread(parameters):
        set_name = parameters['set_name']
        log.info('[{}] Starting xmltocsv'.format(set_name))
        converter = XML2CSV(set_name)
        converter.go()
        log.info('[{}] Finished xmltocsv'.format(set_name))
        
if __name__ == '__main__':
    # Create the tasks
    tasks = []
    for set_name in ['bndlivre']: #, 'porbase', 'catalogo' 
        tasks.append({'set_name': set_name})
    
    # Go !
    pool = multiprocessing.Pool(processes=3)
    pool.map(xmltocsv_thread, tasks)
    pool.close()
    pool.join()
