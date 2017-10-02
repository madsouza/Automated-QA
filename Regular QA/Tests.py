from openpyxl import *
import glob
path = 'Machines'


def ML_04(machine):
    test_path = '%s/%s/*' % (path, machine)
    # glob loads all files in a folder
    files = glob.glob(test_path)
    # filter to files containing ml_04
    files = filter(lambda x: 'ML04' in x, files)
    # check that file exists
    if not files:
        return 'no file'

    # check if 2 files present
    elif len(files) > 1:
        # if so remove file with yyyy-mm-dd
        files = filter(lambda x: 'mm-dd' in x, files)
    try:
        qa_file = load_workbook(files[0], data_only=True)
        qa_sheet = qa_file["ML04 ML05 ML09"]
    except:
        return 'duplicate files'

    values_to_submit = [qa_sheet['S20'].value, qa_sheet['S22'].value, qa_sheet['S24'].value,
                        qa_sheet['S26'].value, qa_sheet['S28'].value]
    #print (qa_sheet.merged_cell_ranges)
    print(qa_sheet['J44'].value)
    for i in range(18,30):
        print(qa_sheet['S%s'%i].value)
        print(qa_sheet['T%s' % i].value)
        print(qa_sheet['U%s' % i].value)
        print(qa_sheet['V%s' % i].value)
        print(qa_sheet['W%s' % i].value)
        print(qa_sheet['X%s' % i].value)
        print(qa_sheet['Y%s' % i].value)
        print(qa_sheet['Z%s' % i].value)


ML_04('RT1')
