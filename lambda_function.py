import cursor
import boto3
import pymysql
import subprocess
import os

DB_NAME = 'db_Student'
BACKUP_BD_NAME = 'db_Student_backup'
TABLE = 'tbl_Student'
DOWNLOAD_FILE = 'download_backup.sql'

def lambda_handler(event, context):
    print("MySQL Backup Function Started ===>")
    #mysqldb.corlgu8ddbzz.us-west-2.rds.amazonaws.com

    host = 'mysqldb1.corlgu8ddbzz.us-west-2.rds.amazonaws.com'
    user = 'rameshlodh'
    password = 'rahul123'
    S3_Bucket_Name = 'rameshlodhbucket'

    print("Trying to Connect With MySQL DataBase ===>")

    connection = pymysql.connect(host=host, user=user, password=password)

    print("MySQL Database Connected ====>")

    cursor = connection.cursor()

    sql = f"create database IF NOT EXISTS {DB_NAME}"
    cursor.execute(sql) 

    cursor.execute("show databases")
    cursor.fetchall()
    connection.select_db(DB_NAME)

    cursor.execute("CREATE TABLE if not exists tbl_Student (id int, name VARCHAR(255), address VARCHAR(255))")
    cursor.execute("show tables")

    sql = "insert into tbl_Student values (1, 'ramesh', 'kalyan')"
    cursor.execute(sql)

    cursor.execute("select * from tbl_Student")
    connection.commit()

    print(cursor.fetchall())

    command = f"mysqldump --host %s --user %s -p%s %s | aws s3 cp - s3://%s/%s" %(
        host, user, password, DB_NAME, S3_Bucket_Name, DB_NAME + '.sql')
    subprocess.run(command, shell=True)
    print("MySQL Database Backup Done ====>")

    if not os.path.exists(f'/tmp/{DOWNLOAD_FILE}'):
        #os.makedirs('/tmp')
        open (f'/tmp/{DOWNLOAD_FILE}','w').close()

    S3_Client = boto3.client('s3')

    S3_Client.download_file(S3_Bucket_Name, DB_NAME + '.sql', f'/tmp/{DOWNLOAD_FILE}')

    cursor.execute("create database IF NOT EXISTS db_Student_backup")
    
    command = f"mysql -h {host}, -u {user}, -p{password} db_Student_backup < /tmp/{DOWNLOAD_FILE}"
    output = subprocess.run(command, shell=True)

    if output.returncode == 0:
        print("MySQL Database restore successfully ====>")
    else:
        (f"MySQL Database restore failed with error code {output.returncode}")
    return "MySQL Database Backup Done ===>"
lambda_handler(None,None)







































