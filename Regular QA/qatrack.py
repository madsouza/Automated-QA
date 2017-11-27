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
    wb = openpyxl.load_workbook('test_urls.xlsx')
    ws = wb.active
    row = filter(lambda x: ws['A%s' % x].value == test, [i for i in range(2, ws.max_row + 1)])[0]
    col = chr(filter(lambda x: ws['%s1' % chr(x)].value == machine, [i for i in range(66, 73)])[0])
    return "qa/utc/perform/%s/" % ws['%s%s' % (col, row)].value


def submit(test_url, values):
    length = len(values)
    constant_data = {'csrfmiddlewaretoken': token,
                     "work_started": date + ' 12:00',
                     "work_completed": date + ' 12:30',
                     "status": "1",
                     "form-TOTAL_FORMS": str(length),
                     "form-INITIAL_FORMS": str(length),
                     "form-MAX_NUM_FORMS": "1000"}

    test_data = {"form-%s-value" % n: values[n] for n in range(0, length)}
    submission_data = constant_data.copy()
    submission_data.update(test_data)
    resp = s.post(root + test_url, data=submission_data)





ip_address, user, password = read_file()
root, token, s = login()
date = datetime.datetime.now().strftime("%d-%m-%Y")

