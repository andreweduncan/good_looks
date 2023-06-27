import lkml
'''
HOW IT WORKS:
# loaded_lkml - provides the view file info to parse
# main() - performs several operations on the loaded_lkml
Write out how main works:
    1. Write the header of the view to the final file (TBD)
    2. for loop: get field type from the loaded_lkml using field_types_info
            a. run sorting operations on each fields' parameters
            b. sort the fields alphabetically
            c. output to the final file
'''

'''
FUNCTION PURPOSES:
write what the functions do in a single like to recap what you have so far, and orient everything under a main() function.

extract_view_headers - extracts and formats view headers (w/ spacing) into a single string for main()

sort_field_parameters - sorts a view fields parameters. Returns field_name, sorted_field_parameters_dict
ordered_dimensions - this is going to be the loop part of 2a that causes sort_field_parameters to loop.
(** note: we can consolidate this into the sort_field_parameters function **)

BODY functions:
the body functions are going to be put into a loop that executes all functions for each field type found.
So: for each field type in field types dictionary
    - order the field parameters of each field of a given type (`sort_field_parameters`)
    - alphabetize the the fields by name 
    - add a centered header for that field type
    - write the header and ordered fields to the file
'''

'''
We need to convert the field types dictionary to a tuple because I fucked up.
I thought we only needed the name of the field type in loaded_lkml to access it,
and the name of the header according to the cs style guide, but it turns out we also 
need the real (non-plural) field type name to add in as the field type for the actual
field lkml (eg. dimension: my_dimension {...)

So:
1. create a tuple of tuples that contains field_name, loaded_lkml_field_key_name, lkml_field_header_name
2. figure out how to access each element of the tuple, and how to loop through pulling x
3. Replace all references to field_types_dictionary to the appropriate tuple element field_types_tuple[0]

'''

field_types_info = (
    # Nested tuple containing looker field type information for the program. 
    # Format:
    #  field_name  |  lkml_field_header_name  |  loaded_lkml_field_key_name
    ("dimension_group", "dimension_groups", "DIMENSION GROUPS"),
    ("dimension", "dimensions", "DIMENSIONS"),
    ("measure", "measures", "MEASURES"),
    ("N/A", "primary_key", "PRIMARY KEY"), #not actual field types
    ("N/A", "parameters_and_filters", "PARAMETERS / FILTERS"), #not actual field types
    ("N/A", "sets", "SETS") #not actual field types
)

# these fields unpack the correct tuple element from field_types_info to return a list of
# field_name  |  lkml_field_header_name  |  loaded_lkml_field_key_name
# these are packed into tuples because sometimes the values need crossed referenced against 
# each other, for determining things like printing headers.
def field_types():
    field_type_list = []
    for field in field_types_info:
        field_type_list.append(field[0])
    return field_type_list

def lkml_field_header_names():
    lkml_field_header_name_list = []
    for field_header_name in field_types_info:
        lkml_field_header_name_list.append(field_header_name[1])
    return lkml_field_header_name_list

def loaded_lkml_field_key_name():
    loaded_lkml_field_key_name_list = []
    for field_header_name in field_types_info:
        loaded_lkml_field_key_name_list.append(field_header_name[2])
    return loaded_lkml_field_key_name_list

# loaded_lkml - get lkml view file contents from lookml_string_file
with open('lookml_string_file.txt', 'r') as file:
    loaded_lkml = lkml.load(file.read())['views'][0]

# keys = field type names to search for in the loaded_lkml, values = how to print the section headers for that field
field_types_dictionary = {
    "dimension_groups": "DIMENSION GROUPS",
    "dimensions": "DIMENSIONS",
    "measures": "MEASURES",
    "primary_key": "PRIMARY KEY", #not actual field types
    "parameters_and_filters": "PARAMETERS / FILTERS", #not actual field types
    "sets": "SETS" #not actual field types
}

############ Section 1 ###############
# https://candlescience.slab.com/posts/look-ml-standards-vwd6xr1z#:~:text=2-,Ordering,-of%20dimensions%3A

# removes and writes view headers to new file 
def extract_view_headers(loaded_lkml):
    ''' - remove the view file header elements from the loaded_lkml dictionary, 
        - format them, 
        - write the result to 'header_string' variable. 
        - By design, this captures ANY keys not in the field_types() function
          so if you have any weirdness in the operation it will appear in the header.'''
    view_headers = {}
    lkml_field_header_names_list = lkml_field_header_names()
    for key, value in loaded_lkml.items(): #find keys not in field types dict
        if key not in lkml_field_header_names_list:
            view_headers[key] = value
    view_name = view_headers['name'] #extract and remove name
    del view_headers['name']
    view_headers['sql_table_name'] = view_headers['sql_table_name'] + ' ;;' #add semicolons
    result = ""
    for key, value in view_headers.items(): #create correctly formatted view file header string
        result += f"  {key}: {value}\n"
        header_string = f'view: {view_name}' + ' {\n' + result
    return header_string

def sort_field_parameters(field):
    '''this function correctly orders the dimensions in a looker field according to the CS style guide.
    Be aware that the field name itself is also contained in this dictionary at the end, and will
    need to be extracted out. '''
    lkml_field_parameters_order = [
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
    field_name = field['name']
    del field['name']
    sorted_keys = sorted(field.keys(), key=lambda k: lkml_field_parameters_order.index(k) if k in lkml_field_parameters_order else len(lkml_field_parameters_order))
    sorted_field_parameters_dict = {key: field[key] for key in sorted_keys}
    return field_name, sorted_field_parameters_dict
########### END Section 1 ############


############ Section 2 ###############
def ordered_dimensions(field_dictionary):
    ''' this function runs the sorting function on the dimensions of each looker field 
    and returns a dictionary of dictionaries, where the key is the name of the field.
    This also orders them alphabetically by key.
    the input to this function is the loaded lkml, pointed at the field type section of your choice.
    For the example file, pointing it at 'dimensions' looks like: loaded_lkml['views'][0]['dimensions']'''
    for dimension in field_dictionary:
        key, value = sort_field_parameters(dimension)
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
        matched_variable = field_type
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
    boundary = '#' * header_length
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



def main(loaded_lkml, field_types_dictionary):
    # extract and format view file headers
    header = extract_view_headers(loaded_lkml, field_types_dictionary)
    body = "" #TBD
    footer = '\n}'
    formatted_view = header + body + footer
    with open('ordered_lkml_file.txt', 'w') as file:
        file.write(formatted_view)
    print(formatted_view)




# find_field_types(loaded_lkml, field_types_dictionary)

# main(loaded_lkml, field_types_dictionary)

#experimental
# def assemble_view_body(loaded_lkml, field_types_dictionary):
#     #output of this function should be a string that represents the view file body
#     '''this function takes the loaded lkml and the field types dictionary and
#     assembles the body of the view file. It does this by iterating through the field types
#     dictionary and searching for the matching field type in the loaded lkml. If it finds a match,
#     it calls the print_field_elements function to print the field type, field name, and field contents.
#     '''
#     for key in loaded_lkml.keys():
#         if key in field_types_dictionary.keys():
#             print(loaded_lkml[key])
# assemble_view_body(loaded_lkml, field_types_dictionary)








'''
right now I want to create a version of print field elements that doesnt validate the field type.
We can then put that inside of a for loop that does the validation 


'''

# def print_field_elements(field_type,dictionary):
#     '''This function takes a field type and dictionary input for that field,
#     and prints out the field type, the field name, and the contents of the field WITH field header
#     and organized contents. Additionally, each field is also in alphebetical order.
#     '''
#     for key, value in dictionary[field_type]:
#         print(f'{key}: {value}')
#     # matched_variable = field_type
#     # print(matched_variable)
#     # for key, value in dictionary.items():
#     #     print(f'\n  {field_type}: {key} ' + '{')
#     #     for parameter, contents  in value.items():
#     #         print(f'    {parameter}: {contents}')
#     #     print('    }')

# goal:
# get a list of fields of a given field type


# print_field_elements('dimensions',loaded_lkml)
# print(loaded_lkml['dimensions'])

# for field in loaded_lkml['dimensions']:
#     sort_field_parameters(field)
#     field_name, sorted_field_parameters_dict

def formatted_field_type(field_type):
    fields_dictionary = {}
    for dimension in field_type:
        key, value = sort_field_parameters(dimension)
        fields_dictionary[key] = value
    print(fields_dictionary)
    return fields_dictionary

# print("clear _______________________________________________\n" * 3)

# formatted_field_type(loaded_lkml['dimensions'])

'''
okay think through how to build the body function
1. get a function that can correctly order the parameters of a single field.
2. run that function for every field of a field type
3. run the function to alphabetize those fields
4. run the function to print the field type, field name, and field contents


'''

#loaded_lkml['dimensions'] is a list of dictionaries.
the_list = [
    {'description': 'Box code of the carton. Box codes that start with sku are items that ship as-is without being put into a carton.', 
    'type': 'string', 'sql': '${TABLE}.box_code', 'name': 'box_code'}, 
    {'description': 'Shipping carrier responsible for delivering the packed carton to the customer', 
    'type': 'string', 'sql': '${TABLE}.carrier', 'name': 'carrier'}, 
    {'type': 'string', 'description': """If the box code starts with ‘sku’, then it is a ‘self-contained item'.\n                  
    If the box code uses the word 'envelope', then it is a ‘packed envelope’.\n                  
    If the box code uses the word 'box', then it is a ‘packed box’.\n                  
    If it doesnt match any of these things, then it is ‘uncategorized’.""", 
    'sql': '${TABLE}.package_type', 'name': 'package_type'}, 
    {'type': 'number', 'description': 'Carton id code. This number is unique to each individual box that we pack and ship out.', 'sql': '${TABLE}.carton_id', 'name': 'carton_id'}, {'description': 'Day of week (Eastern Time) that a carton was packed', 'type': 'string', 'sql': '${TABLE}.day_of_week', 'name': 'day_of_week'}, {'description': 'hour of day (Eastern Time) that a carton was packed', 'type': 'number', 'sql': '${TABLE}.hour_of_day', 'name': 'hour_of_day'}, {'description': 'ID of order that this package belongs to', 'type': 'number', 'sql': '${TABLE}.order_id', 'name': 'order_id'}, {'description': 'Name of warehouse where carton was packed', 'type': 'string', 'sql': '${TABLE}.warehouse', 'name': 'warehouse'}, {'description': 'weight in pounds of the completed packed carton', 'type': 'number', 'sql': '${TABLE}.lb_weight', 'name': 'lb_weight'}]


def sort_field_type(field_type):
    fields_dictionary = {}
    body_string = '\n' + '#'*44 + '\n####### CENTERED HEADER DUMMY STRING #######\n' + '#'*44 + '\n'
    for field in loaded_lkml[field_type]:
        key, value = sort_field_parameters(field) # sort field parameters of a field
        fields_dictionary[key] = value # add that field to the fields dictionary
    sorted(fields_dictionary.items()) # alphabetize dictionary fields by name
    for key, value in fields_dictionary.items(): # add field type and name
        body_string = body_string + (f'\n  {field_type}: {key} ' + '{')
        for parameter, contents  in value.items():
            body_string += (f'\n    {parameter}: {contents}')
        body_string += ('\n  }\n')
    print(body_string)
    return body_string






def print_field_elements(field_type,dictionary):
    '''This function takes a field type and dictionary input for that field,
    and prints out the field type, the field name, and the contents of the field WITH field header
    and organized contents. Additionally, each field is also in alphebetical order.
    '''
    field_type_list = ['pk','parameters_and_filters','dimension_groups','dimensions','measures','sets']
    if field_type in field_type_list:
        matched_variable = field_type
        print(matched_variable)
        for key, value in dictionary.items():
            print(f'\n  {field_type}: {key} ' + '{')
            for parameter, contents  in value.items():
                print(f'    {parameter}: {contents}')
            print('    }')
    else:
        print(f'Field Type Invalid:\n you entered: {field_type}. valid field types are {field_type_list}')
        return




# print(loaded_lkml)

# sort_field_type('dimensions')




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
