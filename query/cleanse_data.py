# input of array to cleanse white space and remove duplicates in array

def cleanse_data_list(raw_data_list):
    clean_data_list = []
    found_data = set()
    for raw_data in raw_data_list:
        if raw_data and (not raw_data.isspace()):
            clean_data = raw_data.strip()
            if clean_data not in found_data:
                found_data.add(clean_data)
                clean_data_list.append(clean_data)
    return clean_data_list
