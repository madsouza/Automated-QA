import psycopg2
from passlib.hash import pbkdf2_sha256

conn = psycopg2.connect(dbname='qatrackdb2', user='qatrack', host='', password='qatrackpass', port="5432")


def check_user(user, password):
    cur = conn.cursor()
    cur.execute("select * from information_schema.tables ")
    cur.execute("select * \
    from INFORMATION_SCHEMA.COLUMNS \
    where TABLE_NAME='auth_user' ")


    cur.execute("select password from auth_user where username='%s'"% user)

    try:
        db_hash = cur.fetchall()[0][0]
    except IndexError:
        return False
    db_hash = db_hash.split("$")


    hashed_password = pbkdf2_sha256.using(rounds=db_hash[1], salt=db_hash[2]).hash(password)
    hashed_password = (hashed_password + '=').split("$")

    if hashed_password[-1] == db_hash[-1]:
        return True
    else:
        return False


if __name__ == '__main__':
    print check_user('', '')