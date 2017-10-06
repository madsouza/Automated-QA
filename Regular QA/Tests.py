from openpyxl import *
import glob
path = 'Machines'


def ML04(machine):
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
        print('duplicate')
        return 'duplicate files'

    values_to_submit = [qa_sheet['S20'].value, qa_sheet['S22'].value, qa_sheet['S24'].value,
                        qa_sheet['S26'].value, qa_sheet['S29'].value]
    if None in values_to_submit:
        return 'empty value'
    values_to_submit = map(int, values_to_submit)
    print (values_to_submit)
    return values_to_submit


def ML05(machine):
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
        print('duplicate')
        return 'duplicate files'

    values_to_submit = [qa_sheet['J44'].value, qa_sheet['J46'].value, qa_sheet['J48'].value]
    if None in values_to_submit:
        return 'empty value'
    values_to_submit = map(int, values_to_submit)
    print (values_to_submit)


def ML09(machine):
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
        print('duplicate')
        return 'duplicate files'

    values_to_submit = [qa_sheet['J60'].value, qa_sheet['J62'].value, qa_sheet['J64'].value]
    if None in values_to_submit:
        return 'empty value'
    values_to_submit = map(int, values_to_submit)
    print (values_to_submit)





ML09('RT1')
