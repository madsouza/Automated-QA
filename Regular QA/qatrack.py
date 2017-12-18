import requests
import datetime
import openpyxl


def read_file():
    with open('user_info', 'r') as f:
        info = f.read().splitlines()
    ip = info[0]
    username = info[1][6:]
    passwrd = info[2][10:]
    return ip, username, passwrd


def login():
    root = ip_address
    login_url = root + "accounts/login/"
    s = requests.Session()

    # we need to GET the login page so we can retrieve the csrf token
    s.get(login_url)
    token = s.cookies['csrftoken']

    login_data = {
        'username': user,
        'password': password,
        'csrfmiddlewaretoken': token
    }
    # perform the login
    login_resp = s.post(login_url, data=login_data)
    token = s.cookies['csrftoken']
    print token
    return root, token, s


def test_number(machine, test):
    wb = openpyxl.load_workbook('tests.xlsx')
    ws = wb['test_urls']
    row = filter(lambda x: ws['A%s' % x].value == test, [i for i in range(2, ws.max_row + 1)])[0]
    col = chr(filter(lambda x: ws['%s1' % chr(x)].value == machine, [i for i in range(66, 73)])[0])
    return "qa/utc/perform/%s/" % ws['%s%s' % (col, row)].value


def submit(test_url, values):
    length = len(values)
    test_data = {}
    constant_data = {'csrfmiddlewaretoken': token,
                     "work_started": date + ' %s' % time,
                     "work_completed": date + ' %s' % time,
                     "status": "1",
                     "form-TOTAL_FORMS": str(length),
                     "form-INITIAL_FORMS": str(length),
                     "form-MAX_NUM_FORMS": "1000"}
    for n in range(0, length):
        if values[n] == 'Yes':
            test_data["form-%s-value" % n] = '1'
        elif values[n] == 'No':
            test_data["form-%s-value" % n] = '0'
        else:
            test_data["form-%s-value" % n] = values[n]
    # test_data = {"form-%s-value" % n: values[n] for n in range(0, length)}
    submission_data = constant_data.copy()
    submission_data.update(test_data)
    resp = s.post(root + test_url, data=submission_data)



ip_address, user, password = read_file()
root, token, s = login()
date = datetime.datetime.now().strftime("%d-%m-%Y")
time = datetime.datetime.now().strftime("%H:%M")

if __name__ == '__main__':
    print time
