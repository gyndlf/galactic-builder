import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'galactic-builder-database'
GDOCS_OAUTH_JSON = 'galactic-builder-8e70e9c56779.json'


def open(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)

        #wks = gc.open(spreadsheet).sheet1
        wks = gc.open(spreadsheet)
        return wks

    except Exception as ex:
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


def get_stats(worksheet, person, item):
    """Get the item from the row person in the worksheet"""
    if worksheet is None:
        return 'Error no given worksheet.'

    found_person = worksheet.find(person)
    found_item = worksheet.find(item)

    print('Found person', found_person.row, found_person.col)
    print('Found item', found_item.row, found_item.col)

    cell = worksheet.cell(found_person.row, found_item.col).value
    return cell

print('Opening...')
sheet = open(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
print('Running...')


wks_list = sheet.worksheets()
worksheet = sheet.worksheet('people')

print(get_stats(worksheet, 'james', 'money'))


# Rows : Columns
#worksheet.update_cell(y, x, num)

'''
worksheet.update_cell(2, 7, 'Bingo!')

# Select a range
cell_list = worksheet.range('B1:B7')

for cell in cell_list:
    cell.value = 'O_o'

# Update in batch
worksheet.update_cells(cell_list)
'''

