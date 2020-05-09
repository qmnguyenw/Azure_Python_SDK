from azure.mgmt.sql import SqlManagementClient
from azure.common.client_factory import get_client_from_cli_profile
import pyodbc

LOCATION = 'eastus'
GROUP_NAME = 'todoWebResourceGroup'
SERVER_NAME = 'todoWebServer'
DATABASE_NAME = 'todoDB'
USER_NAME = 'mysecretname'
PASSWORD = '123456a@'

# authenticate
sql_client = get_client_from_cli_profile(SqlManagementClient)


def run_example():
    # Get SQL Database
    print('Get SQL Database')
    database = sql_client.databases.get(
        GROUP_NAME,
        SERVER_NAME,
        DATABASE_NAME
    )
    print(database)
    print("\n\n")


def create_and_insert():
    server = 'tcp:'+SERVER_NAME+'.database.windows.net'
    database = DATABASE_NAME
    username = USER_NAME
    password = PASSWORD
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(
        'Driver='+driver+';'+
        'Server='+server+',1433;'+
        'Database='+database+';'+
        'Uid='+username+';'+
        'Pwd='+password+';'+
        'Encrypt=yes;'+
        'TrustServerCertificate=no;'+
        'Connection Timeout=30;'
        # 'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password
    )
    cursor = cnxn.cursor()
    tsql = "CREATE TABLE CLOUD (name varchar(255), code int);"
    tsqlInsert = "INSERT INTO CLOUD (name, code) VALUES ('Azure', 1); "
    selectValues = "SELECT * FROM CLOUD"
    with cursor.execute(tsql):
        print('Successfully created table!')
    with cursor.execute(tsqlInsert):
        print('Successfully inserted data into table')
    cursor.execute(selectValues)
    row = cursor.fetchone()
    while row:
        print(str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()
    cnxn.commit()

if __name__ == "__main__":
    run_example()
    create_and_insert()
