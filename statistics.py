import csv
import bz2
import logging
import re
import json
import os
from jinja2 import Template

# http://www.delimited.io/blog/2013/12/8/chord-diagrams-in-d3
# http://c3js.org/
# http://nvd3.org/examples/scatter.html
# http://www.highcharts.com/demo/scatter


# Configure a logger for the entire script
logFormat = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logFormat)
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)

BIN_SIZE = 25

# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  

def process_dataset(dataset_name):
    data = {}
    data['nb_records'] = 0
    data['nb_recs_exact_date'] = 0
    data['nb_recs_several_udc'] = 0
    data['per_date'] = {}
    data['per_date_bin'] = {}
    data['per_udc'] = {}
    data['udc_length'] = {}
    data['matrices'] = {}
    for sep in ['+', '/', ':']:
        data['matrices'][sep] = [[0 for x in range(10)] for x in range(10)] 
    
    # Open the file
    input_file = bz2.BZ2File("data/{}.csv.bz2".format(dataset_name))
    reader = csv.reader(input_file, delimiter=',', quotechar='"')

    # Process the records
    processed_ids = set()
    for record in reader:
        # Get the identifier
        identifier = record[0]
        data['nb_records'] = data['nb_records'] + 1
        
        # Look if the date is exact, check that we don't record duplicates
        if identifier not in processed_ids:
            processed_ids.add(identifier)
            date = record[1]
            if re.match("^[0-9]{4}$", date):
                # Store the exact data
                data['nb_recs_exact_date'] = data['nb_recs_exact_date'] + 1
                data['per_date'].setdefault(date, 0)
                data['per_date'][date] = data['per_date'][date] + 1
                # Store a bin value
                date_bin = (int(date) / BIN_SIZE) * BIN_SIZE
                data['per_date_bin'].setdefault(date_bin, 0)
                data['per_date_bin'][date_bin] = data['per_date_bin'][date_bin] + 1
        else:
            # Count the number of UDC classes used
            data['nb_recs_several_udc'] = data['nb_recs_several_udc'] + 1
            
        # Filter out non valid UDC class
        udc_class = record[2]
        udc_main = udc_class[0]
        if not re.match("^[0-9]$", udc_main):
            continue
        
        # Count the main group of the UDC class
        data['per_udc'].setdefault(udc_main, 0)
        data['per_udc'][udc_main] = data['per_udc'][udc_main] + 1

        # Record the length of the class
        class_len = str(len(udc_class))
        data['udc_length'].setdefault(class_len, 0)
        data['udc_length'][class_len] = data['udc_length'][class_len] + 1
        
        # Extract the matrices
        for sep in ['+', '/', ':']:
            cls = udc_class.split(sep)
            classes = filter(lambda c: c != '', cls) # Filter out '::' and the like
            for index in range(len(classes)-1):
                from_group = classes[index][0]
                to_group = classes[index+1][0]
                if re.match("^[0-9]$", from_group) and re.match("^[0-9]$", to_group):
                    v = data['matrices'][sep][int(from_group)][int(to_group)]
                    data['matrices'][sep][int(from_group)][int(to_group)] = v + 1
                    
    # Close the file
    input_file.close()

    # Refactor the per_date and per_udc for the charting library
    for key in ['per_date', 'per_date_bin', 'per_udc']:
        labels = sorted(data[key].keys())
        values = [data[key][l] for l in labels]
        data['{}_pairs'.format(key)] = {'size': len(labels), 'labels':labels, 'vals':values} 
        
    # Return the data
    return data

if __name__ == '__main__':
    dataset_names = ['bndlivre', 'catalogo', 'porbase']  # 

    # Run the data collection part
    data = {}
    for dataset_name in dataset_names:
        log.info("Start processing {}".format(dataset_name))
        data[dataset_name] = process_dataset(dataset_name)
    
    # Prepare the overviews
    overviews = {}
    for key in ['per_date_bin', 'per_udc']:
        overview = {}
        labels = set()
        for dataset_name in dataset_names:
            for label in data[dataset_name]['{}_pairs'.format(key)]['labels']:
                labels.add(label)
        overview['labels'] = sorted([l for l in labels])
        overview['datasets'] = []
        color_index = 0
        for dataset_name in dataset_names:
            r, g, b = tableau20[color_index]
            color_index = color_index + 1
            dataset = {'label': dataset_name,
                       'fillColor' : "rgba({},{},{},0.5)".format(r, g, b),
                       'strokeColor' : "rgba({},{},{},0.8)".format(r, g, b),
                       'highlightFill' : "rgba({},{},{},0.75)".format(r, g, b),
                       'highlightStroke' : "rgba({},{},{},1)".format(r, g, b),
                       'data' : []}
            for l in overview['labels']:
                v = 0
                if l in data[dataset_name][key]:
                    v = data[dataset_name][key][l]
                dataset['data'].append(v)
            overview['datasets'].append(dataset)
        overviews[key] = overview
        
    # Write down the CSV files for the D3 scatter plots
    for dataset_name in dataset_names:
        output_name = 'udc_length_{}.csv'.format(dataset_name)
        with open('data/' + output_name, 'w') as output_file:
            writer = csv.writer(output_file, delimiter=',', quotechar='"')
            writer.writerow(['length','count'])
            keys = sorted(data[dataset_name]['udc_length'].keys())
            for k in keys:
                v = data[dataset_name]['udc_length'][k]
                if v != 0:
                    writer.writerow([k,v])
                        
    # Write down the CSV files for the D3 Chord diagrams
    name_map = {'+':'plus', ':':'colon', '/':'slash'}
    for dataset_name in dataset_names:
        for (k,v) in data[dataset_name]['matrices'].iteritems():
            output_name = 'network_{}_{}.csv'.format(dataset_name, name_map[k])
            with open('data/' + output_name, 'w') as output_file:
                writer = csv.writer(output_file, delimiter=',', quotechar='"')
                writer.writerow(['from','to','count'])
                for row in range(0, len(v)):
                    for col in range(0, len(v[row])):
                        if v[row][col] != 0:
                            writer.writerow([row,col,v[row][col]])
                            
    # Render the page        
    log.info("Building the statistics page")
    template = Template(open('templates/stats.html', 'r').read())        
    template_data = {'datasets':data,
                     'overview_years':overviews['per_date_bin'],
                     'overview_udc':overviews['per_udc'], }
    with open('/tmp/stats.html', 'w') as outfile:
        outfile.write(template.render(template_data))
        