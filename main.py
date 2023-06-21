from pprint import pprint
import os
import lkml
# from lkml_project_functions import *


'''
the field_types_dictionary provides two things:
1. the key represents a field type name that can be used to search the contents
of the loaded lkml dictionary.
eg. dimensions on a single view file can be found via loaded_lkml['views'][0]['dimensions']

2. the value represents the field header that will be printed above the organized field in 
the final product. You can test this by calling the "centered_header" function on it.

Example:
for value in field_types_dictionary.values():
    centered_header(value),print('\n')

The end goal of this is to be able to process a dictionary to find the matching keys,
perform a series of operations on those keys, and then print the header and contents
'''
field_types_dictionary = {
    "dimension_groups": "DIMENSION GROUPS",
    "dimensions": "DIMENSIONS",
    "measures": "MEASURES"
}

# Non field-type headers
pk_header = '''
  ##########################
  ##     PRIMARY KEY      ##
  ##########################'''

parameters_and_filters_header = '''
  ##########################
  ## PARAMETERS / FILTERS ##
  ##########################'''

sets_header = '''
  ##########################
  ##         SETS         ##
  ##########################'''

'''
Section Overview
Precursor variables and loading lkml
1. Sort the dimensions in a looker field according to the CS style guide.
2. general work for loading the lkml file
'''
file_path = 'lookml_string_file.txt'

def load_lkml_contents():
    ''' initiates the lkml loading process from the text file and creates the
    loaded_lkml variable'''
    with open(file_path, 'r') as file:
        contents = file.read()
        loaded_contents = lkml.load(contents)
    return loaded_contents


############ Section 1 ###############
# https://candlescience.slab.com/posts/look-ml-standards-vwd6xr1z#:~:text=2-,Ordering,-of%20dimensions%3A

def sort_looker_field_dimensions(dimension_dict):
    '''this function correctly orders the dimensions in a looker field according to the CS style guide.
    Be aware that the field name itself is also contained in this dictionary at the end, and will
    need to be extracted out. '''
    lkml_field_dimension_order = [
        'label', 
        'description', 
        'type', 
        'timeframes', 
        'sql', 
        'convert_tz', 
        'value_format_name', 
        'html', 
        'drill_fields', 
        'group_label', 
        'primary_key', 
        'hidden']
    dictionary_name = dimension_dict['name']
    del dimension_dict['name']
    sorted_keys = sorted(dimension_dict.keys(), key=lambda k: lkml_field_dimension_order.index(k) if k in lkml_field_dimension_order else len(lkml_field_dimension_order))
    sorted_dictionary = {key: dimension_dict[key] for key in sorted_keys}
    return dictionary_name, sorted_dictionary
########### END Section 1 ############


############ Section 2 ###############
def ordered_dimensions(field_dictionary):
    ''' this function runs the sorting function on the dimensions of each looker field 
    and returns a dictionary of dictionaries, where the key is the name of the field.
    This also orders them alphabetically by key.
    the input to this function is the loaded lkml, pointed at the field type section of your choice.
    For the example file, pointing it at 'dimensions' looks like: loaded_lkml['views'][0]['dimensions']'''
    for dimension in field_dictionary:
        key, value = sort_looker_field_dimensions(dimension)
        fields_dictionary[key] = value
    return fields_dictionary
########### END Section 2 ############


def print_field_elements(field_type,dictionary):
    '''This function takes a field type and dictionary input for that field,
    and prints out the field type, the field name, and the contents of the field WITH field header
    and organized contents. Additionally, each field is also in alphebetical order.
    '''
    field_type_list = ['pk','parameters_and_filters','dimension_groups','dimensions','measures','sets']
    if field_type in field_type_list:
        matched_variable = globals()[field_type+'_header']
        print(matched_variable)
        for key, value in dictionary.items():
            print(f'\n  {field_type}: {key} ' + '{')
            for parameter, contents  in value.items():
                print(f'    {parameter}: {contents}')
            print('    }')
    else:
        print(f'Field Type Invalid:\n you entered: {field_type}. valid field types are {field_type_list}')
        return



def centered_header(field, header_length = 26):
    '''This is a function that prints a centered header for a field type in the lkml.
    The actual program uses this by calling the function with the field type as the input
    based on whether a given field type is present in the lkml file.

    It iterates through the loaded_lkml dictionary and searches for keys matching the field type.
    If a key field_type is found, it uses the value associated with that key to print the header
    for that field. The header is centered in a 26 character block by default, but can be adjusted'''
    field_length = len(field)
    if field_length > header_length - 4:
        print(f'''field length for '{field}' too long for the standard {header_length} character block. 
        \nplease adjust header length via the optional header_length parameter
        \neg: centered_header(field,header_length=35)''')
        return  
    extra_space = header_length - field_length - 4 # -4 is for leading and trailing ##'s
    if extra_space % 2 == 0:  # Number is even
        front_pad = extra_space // 2
        back_pad = extra_space // 2
    else:  # Number is odd
        front_pad = extra_space // 2
        back_pad = extra_space // 2 + 1
    boundary = '#'*header_length
    print(boundary+'\n##'+ (' '*front_pad) + field + (' '*back_pad)+'##\n'+boundary)


# print(fields_dictionary)
# print_field_elements('dimensions',fields_dictionary)

def find_field_types(dictionary, field_types_dictionary):
    ''' this is a function that searches the dictionary created by loaded_lkml
    and finds the matching field types that match keys in the field_types_dictionary.
    '''
    found_values = []
    unexpected_values = []
    for key in dictionary.keys():
        if key in field_types_dictionary.keys():
            found_values.append(key)
        else:
            unexpected_values.append(key)
    print(f"Found field types: {found_values}.\n Also found unexpected field types: {unexpected_values}")


# create a dictionary to store the ordered field results
fields_dictionary = {}

# creates the loaded lkml for a single-view file
loaded_lkml = load_lkml_contents()['views'][0]




# print(field_types_dictionary.keys())
find_field_types(loaded_lkml, field_types_dictionary)

# for key in loaded_lkml['views'][0].keys():
#     print(key)

# 1. get the name of the view and the sql table name
# view_label = loaded_lkml['views'][0]['label']
# sql_table_name = loaded_lkml['views'][0]['sql_table_name']

# get dimensions, sort them, put the result in "fields dictionary"
# ordered_dimensions(loaded_lkml['views'][0]['dimensions'])


# for value in field_types_dictionary.values():
#     centered_header(value),print('\n')
















##### TESTING/ CODE GRAVEYARD #####
# Stuff that isnt useful in the final model but may be helpful for testing

'''
# Testing Materials: 

# this is a dictionary used for testing the ordering of field dimensions
dictionary = {
    'type': 'text',
    'sql': 'SELECT * FROM table',
    'html': '<p>Some HTML content</p>',
    'description': 'This is a description',
    'label': 'Label',
    'primary_key': True,
    'timeframes': ['day', 'week', 'month'],
    'convert_tz': True,
    'drill_fields': ['field1', 'field2'],
    'group_label': 'Group',
    'value_format_name': 'Format',
    'title': 'dont forget me',
    'name': 'my_dimension'
}

# this was a dictionary that fed a gpt prompt for the print_dictionary_elements function
 python_dictionary = {
    'first_record': {'color': 'orange', 'shape': 'circle', 'count': 2}, 
    'second_record': {'color': 'blue', 'shape': 'square', 'count': 1}, 
    'third_record': {'color': 'red', 'shape': 'triangle', 'count': 3}
}
'''
