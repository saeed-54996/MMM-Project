import csv

def read_csv_to_dict_list(file_path):
    dict_list = []

    with open(file_path, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            # Replace empty strings with None
            dict_list.append({k: (v if v != '' else None) for k, v in row.items()})
            
    return dict_list
