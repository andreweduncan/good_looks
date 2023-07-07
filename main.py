import lkml


'''
CODE SECTIONS:
1. FORMATTING OPTIONS
    - set list of valid field types
    - set ordering of looker field parameters

2. HEADERS
- functions and logic for extracting view header info

3. FIELD PARAMETER FUNCTIONS  
    - sort_field_parameters

4. FIELD ORGANIZATION FUNCTIONS

MAIN()


Goal for today:
Write a function that performs some custom formatting on 
certain view parameters, and get it to run in side the normal program operation
(most likely when field parameters are being ordered/parsed)

First two rules of function:
- [ ] add in double semicolons after sql fields </br>
- [ ] add in quotation marks around descriptions </br>

we are gonna write this one inside the sort_field_parameters function.


'''





#############################################
##          1. FORMATTING OPTIONS          ##
#############################################

# this contains a list of field types used to create the body of the view file,
# the field type headers, and to reconstruct the lkml for the individual fields
field_types_info = (
    # Nested tuple containing looker field type information for the program. 
    # Format:
    #  field_name  |  loaded_lkml_dict_key_name   |  lkml_field_header_name  
    ("dimension_group", "dimension_groups", "DIMENSION GROUPS"),
    ("dimension", "dimensions", "DIMENSIONS"),
    ("measure", "measures", "MEASURES"),
    ("N/A", "primary_key", "PRIMARY KEY"), #not actual field types
    ("N/A", "parameters_and_filters", "PARAMETERS / FILTERS"), #not actual field types
    ("N/A", "sets", "SETS") #not actual field types
)

# Controls the ordering of field parameters. Field parameters in the final view will 
# be sorted in this order. Parameters not listed will be added at the end.
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


# these fields unpack the correct tuple element from field_types_info to return a list of
# field_name  |  lkml_field_header_name  |  loaded_lkml_dict_key_name
# these are packed into tuples because sometimes the values need crossed referenced against 
# each other, for determining things like printing headers.
def field_types():
    field_type_list = []
    for field in field_types_info:
        field_type_list.append(field[0])
    return field_type_list

def loaded_lkml_dict_key_name():
    loaded_lkml_dict_key_name_list = []
    for field_header_name in field_types_info:
        loaded_lkml_dict_key_name_list.append(field_header_name[1])
    return loaded_lkml_dict_key_name_list

def lkml_field_header_names():
    lkml_field_header_name_list = []
    for field_header_name in field_types_info:
        lkml_field_header_name_list.append(field_header_name[2])
    return lkml_field_header_name_list

#############################################
##           FORMATTING OPTIONS            ##
#############################################


#############################################
##          2. HEADER FUNCTIONS            ##
#############################################

# https://candlescience.slab.com/posts/look-ml-standards-vwd6xr1z#:~:text=2-,Ordering,-of%20dimensions%3A
# removes and writes view headers to new file 
def extract_view_headers(loaded_lkml):
    ''' - remove the view file header elements from the loaded_lkml dictionary, 
        - format them, 
        - write the result to 'header_string' variable. 
        - By design, this captures ANY keys not in the field_types() function
          so if you have any weirdness in the operation it will appear in the header.'''
    lkml_field_dict_keys = loaded_lkml_dict_key_name()
    view_headers = {}
    for key, value in loaded_lkml.items(): #find keys not in field types dict
        if key not in lkml_field_dict_keys:
            view_headers[key] = value
    view_name = view_headers['name'] #extract and remove name
    del view_headers['name']
    view_headers['sql_table_name'] = view_headers['sql_table_name'] + ' ;;' #add semicolons  
    result = ""
    for key, value in view_headers.items(): #create correctly formatted view file header string
        result += f"  {key}: {value}\n"
        header_string = f'view: {view_name}' + ' {\n' + result + '\n'
    return header_string

#############################################
##            HEADER FUNCTIONS             ##
#############################################


#############################################
##      3. FIELD PARAMETER FUNCTIONS       ##
#############################################

def field_parameter_adjustments(dictionary):
    ''' When using the lkml module to parse the view file, the lkml field paramaters 
    have several unexpected quirks.
        - SQL fields are missing semicolons (;;) at the end
        - Descriptions are missing quotation marks.
    This performs these small adjustments to present the parameters as expected.
    As more of these adjustments are discovered, they can be added here'''
    for key, value in dictionary.items():
        if key == "description": # add double quotes around descriptions
            dictionary[key] = '"' + value + '"'
        elif key in ['sql','sql_latitude','sql_longitude','sql_on','sql_distinct_key']: # add double semicolons to sql fields
            dictionary[key] = value + " ;;"
    return dictionary

def sort_field_parameters(field):
    '''this function correctly orders the dimensions in a looker field according to the CS style guide.
    Be aware that the field name itself is also contained in this dictionary at the end, and will
    need to be extracted out. '''
    field_name = field['name']
    del field['name']
    sorted_keys = sorted(field.keys(), key=lambda k: lkml_field_parameters_order.index(k) if k in lkml_field_parameters_order else len(lkml_field_parameters_order))
    sorted_field_parameters_dict = {key: field[key] for key in sorted_keys}
    adjusted_field_parameters = field_parameter_adjustments(sorted_field_parameters_dict) #add small adjustments to fields
    return field_name, adjusted_field_parameters

#############################################
##        FIELD PARAMETER FUNCTIONS        ##
#############################################


#############################################
##     4. FIELD ORGANIZATION FUNCTIONS     ##
#############################################

def sort_field_type(loaded_lkml_dict_key_name,lkml_field_header_name):
    fields_dictionary = {}
    body_string = centered_header(lkml_field_header_name)
    for field in loaded_lkml[loaded_lkml_dict_key_name]:
        key, value = sort_field_parameters(field) # sort field parameters of a field
        fields_dictionary[key] = value # add that field to the fields dictionary
    sorted(fields_dictionary.items()) # alphabetize dictionary fields by name
    for key, value in fields_dictionary.items(): # add field type and name
        body_string = body_string + (f'\n  {loaded_lkml_dict_key_name}: {key} ' + '{')
        for parameter, contents  in value.items():
            body_string += (f'\n    {parameter}: {contents}')
        body_string += ('\n  }\n')
    return body_string


def centered_header(field, header_length = 26):
    '''This is a function that prints a centered header for a field type in the lkml.
    The actual program uses this by calling the function with the field type as the input
    based on whether a given field type is present in the lkml file.

    It iterates through the loaded_lkml dictionary and searches for keys matching the field type.
    If a key field_type is found, it uses the value associated with that key to print the header
    for that field. The header is centered in a 26 character block by default, but adjusts to
    accomodate longer titles when needed '''
    field_length = len(field)
    if field_length > header_length - 4:
        header_length = field_length + 6
        print(f'Long header present. Adjusting header block length from 26 to {header_length}')
    extra_space = header_length - field_length - 4 # -4 is for leading and trailing ##'s
    if extra_space % 2 == 0:  # Number is even
        front_pad = extra_space // 2
        back_pad = extra_space // 2
    else:  # Number is odd
        front_pad = extra_space // 2
        back_pad = extra_space // 2 + 1
    boundary = '#' * header_length
    header = ('  '+boundary+'\n  ##'+ (' '*front_pad) + field + (' '*back_pad)+'##\n  '+boundary+'\n')
    return header


def create_view_body(loaded_lkml):
    body = ''
    for i in field_types_info:
        if i[1] in loaded_lkml.keys():
            lkml_field_header_name = i[2]
            loaded_lkml_dict_key_name = i[1]
            sorted_field_type = sort_field_type(loaded_lkml_dict_key_name,lkml_field_header_name)
            body += sorted_field_type + '\n'
    return body

#############################################
##       FIELD ORGANIZATION FUNCTIONS      ##
#############################################


def read_lookml_file():
    try:
        with open(f'original_view_files/{view_file_name}.view', "r") as file:
            loaded_lkml = lkml.load(file.read())['views'][0]
            return loaded_lkml
    except FileNotFoundError:
        error_message = "The program expects a view file located inside 'lookml_string_file.txt'. "
        error_message += "Please add 'lookml_string_file.txt' to this folder and rerun the program."
        return error_message



def main(loaded_lkml):
    # extract and format view file headers
    header = extract_view_headers(loaded_lkml)
    body = create_view_body(loaded_lkml) #TBD
    footer = '}'
    formatted_view = header + body + footer
    with open(f'reformatted_view_files/{view_file_name}.view', 'w') as file:
        file.write(formatted_view)
    print(formatted_view)

# loaded_lkml - get lkml view file contents from lookml_string_file
# with open('lookml_string_file.view', 'r') as file:
#     loaded_lkml = lkml.load(file.read())['views'][0]
# print(loaded_lkml['dimensions'][0])

view_file_name = input('please enter the name of the view file in the original_view_files folder:')

loaded_lkml = read_lookml_file()
main(loaded_lkml)

