
import os,fdb,platform

db_server        = os.getenv("DB_HOST", '192.168.10.5')
db_path          = os.getenv("DB_PATH", 'sklad_prod')
db_user          = os.getenv("DB_USER", 'MONITOR')
db_password      = os.getenv("DB_PASSWORD", 'inwino')

def fetchall_as_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_sql(endpoint):
    sql = 'select qry from querys where ENDPOINT = \'%s\';' % endpoint
    con=create_connect()
    cur=con.cursor()
    rawdata = cur.execute(sql)
    data = rawdata.fetchone()
    return data[0]

def create_connect():
    if platform.system() == 'Windows':
        con = fdb.connect(
            host=db_server,
            port=3053,
            database=db_path,
            user=db_user,
            password=db_password,
            charset="utf-8",
            fb_library_name="C:/sklad/x64/fbclient.dll"
        )
    else:
        return fdb.connect(
            host=db_server,
            port=3053,
            database=db_path,
            user=db_user,
            password=db_password,
            charset="utf-8"
        )
    return con

def get_data(sql):
    con = create_connect()
    cur = con.cursor()
    rawdata = cur.execute(sql)
    data = fetchall_as_dict(rawdata)
    cur.close()
    con.close()
    return data
