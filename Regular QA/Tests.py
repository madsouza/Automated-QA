from openpyxl import *
import glob
path = 'Machines'
# testinfo
#   test: [sheet, [excel cells]]
test_info = {'ML04': ['ML04 ML05 ML09', ['S20', 'S22', 'S24', 'S26', 'S28']],

             'ML05': ['ML04 ML05 ML09', ['J44', 'J46', 'J48']],

             'ML06': ['ML06 ML08 ML10', ['N22', 'N24', 'T22', 'T24']],

             'ML07_LAT': ['ML07 - LNG, LAT, VRT', ['Q20', 'Q22', 'Q24', 'Q26']],

             'ML07_LNG': ['ML07 - LNG, LAT, VRT', ['Q39', 'Q41', 'Q43', 'Q45']],

             'ML07_VRT': ['ML07 - LNG, LAT, VRT', ['Q58', 'Q60', 'Q62', 'Q64']],

             'ML08': ['ML06 ML08 ML10', ['N44', 'N46', 'T44', 'T46']],

             'ML09': ['ML04 ML05 ML09', ['J60', 'J62', 'J64']],

             'ML10': ['ML06 ML08 ML10', ['F63', 'F65', 'F67', 'K63', 'K65', 'K67', 'P63', 'P65', 'P67']],

             'ML11_e': ['ML11', ['AF43', 'AJ45', 'AF47', 'AJ49', 'AF51', 'AJ53', 'AF55', 'AJ57', 'AF59', 'AJ61']],
             'ML11_p': ['ML11', ['AF71', 'AJ73', 'AF75', 'AJ77', 'AF79', 'AJ81', 'AF83', 'AJ85', 'AF87', 'AJ89']],

             'ML12_e': ['ML12', ['U34', 'AE34', 'AO34', 'U37', 'AE37', 'AO37', 'U40', 'AE40', 'AO40',
                                 'U43', 'AE43', 'AO43', 'U46', 'AE46', 'AO46']],
             'ML12_p': ['ML12', ['U55', 'AE55', 'AO55', 'U58', 'AE58', 'AO58', 'U61', 'AE61', 'AO61',
                                 'U64', 'AE64', 'AO64', 'U67', 'AE67', 'AO67']],

             'DTRR': ['DTRR, DIME', ['T27']],
             'DIME': ['DTRR, DIME', ['T56']]}


def get_test(machine, test_number):
    test_path = '%s/%s/*' % (path, machine)
    # glob loads all files in a folder
    files = glob.glob(test_path)
    # filter to files containing ml_04
    files = filter(lambda a: test_number in a, files)
    # check that file exists
    if not files:

        return 'no file'

    # check if 2 files present
    elif len(files) > 1:
        # if so remove file with yyyy-mm-dd
        files = filter(lambda b: 'mm-dd' in b, files)
    try:
        qa_file = load_workbook(files[0], data_only=True)
        qa_sheet = qa_file[test_info[test_number][0]]
    except:

        return 'duplicate files'
    values_to_submit = [qa_sheet[c].value for c in test_info[test_number][1]]

    if None in values_to_submit:
        return 'empty value'
    try:
        values_to_submit = map(int, values_to_submit)
    except:
        values_to_submit = map(str, values_to_submit)

    return values_to_submit

if __name__ == "__main__":
    print get_test('RT2', 'DIME')
