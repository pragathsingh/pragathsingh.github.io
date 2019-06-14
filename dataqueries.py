from pymysql import *
from django.http import HttpResponse

def connect(server='127.0.0.1',username='root',password='',database="foodservice"):
    conn = Connection(server,username,password,database)
    cursor = conn.cursor()
    return conn,cursor

#inbuild database tables in sql which shouldnt matter to user or admin
ignore_tables = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']

#this function displays all tables in a database collection
def database_and_tables_names(database):

    conn,cursor = connect(database=database)
    if(conn and cursor):
        query = """SELECT table_schema, table_name FROM 
                       INFORMATION_SCHEMA.tables ORDER BY 
                       table_schema,table_name """
        cursor.execute(query)
        data = cursor.fetchall()
        dtn = {}
        for tuple in data:
            if (tuple[0] not in ignore_tables):
                if (tuple[0] not in dtn):
                    dtn[tuple[0]] = [tuple[1]]
                else:
                    dtn[tuple[0]].append(tuple[1])
        cursor.close()
        conn.close()
        return 'Database does exists',dtn
    else:
        return 'Database does not exists', None

def check_autoincreament(table,database,cursor):
    is_ai = False
    query = """SELECT *
               FROM INFORMATION_SCHEMA.COLUMNS
               WHERE TABLE_NAME = '"""+table+"""'
               AND table_schema = '"""+database+"""'
               AND EXTRA like '%auto_increment%'"""
    tmp = cursor.execute(query)
    data = cursor.fetchall()
    if(tmp > 0):
        is_ai = True
        ai_col = data[0][4]

    return is_ai,ai_col

def colums_data(table,database):
    conn,cursor = connect(database=database)
    query = """SELECT * FROM 
               INFORMATION_SCHEMA.COLUMNS 
               WHERE TABLE_NAME  = """ + "'"+table+"'" +\
            " AND table_schema ='"+database+"'"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    datalist = []
    for tuple in data:
        d = {}
        d['name'] = tuple[3]
        d['index'] = tuple[4]
        d['type'] = tuple[7]
        d['key'] = tuple[16]
        datalist.append(d)
    return datalist

def table_columns(table,database):

    conn,cursor = connect(database=database)
    query = """SELECT COLUMN_NAME FROM 
               INFORMATION_SCHEMA.COLUMNS 
               WHERE TABLE_NAME  = """ + "'"+table+"'" +\
            " AND table_schema ='"+database+"'"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def dtexist(table,database):

    message,dtn = database_and_tables_names(database)
    if(dtn):
        if (table in dtn[database]):
            message = "Table in Database Exists"
            return message, True
        else:
            message = "Table " + table + "does not exist in " + database + " database"
            return message, False
    else:
        return message, False


def selectfromcolumn(table, database, colstr):

    collist = colstr.split(':')
    column_name = collist[0]
    column_data = collist[1]
    column_data = "'"+column_data+"'"
    message,dtr = dtexist(table, database)
    selectallquery = "SELECT * FROM  " + table + " WHERE " + column_name + " = " + column_data

    if(dtr):
        conn,cursor = connect(database=database)
        try:
            cursor.execute(selectallquery)
            all = cursor.fetchall()
            conn.close()
            cursor.close()
            return 'Query Succeded....!!!Here is your data', all
        except:
            return 'There is was a problem exexuting the query', None
    else:
        return 'Table does not exists', None


def selectall(table,database):

    message,tableexists = dtexist(table, database)
    selectallquery = "SELECT * FROM  " + table
    if(tableexists):
        conn,cursor = connect(database=database)
        try:
            cursor.execute(selectallquery)
            all = cursor.fetchall()
            conn.close()
            cursor.close()
            return 'Query Succeded....!!!Here is your data',all
        except:
            return 'There is was a problem exexuting the query',None
    else:
        return 'Table does not exists',None

def select(table,database,idstr):
    c = 0
    message,dtr = dtexist(table,database)
    if(dtr):
        conn,cursor = connect(database=database)
    else:
        return message,None
    idlist = idstr.split(':')
    colname = idlist[0]
    id = idlist[1]
    id = "'" + id + "'"

    checkquery = "SELECT * FROM  " + table + " WHERE " + colname + " = " + id
    c = cursor.execute(checkquery)

    if(c > 0):
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return 'Here is your data', data
    else:
        return 'no such id '+str(id)+'exists',None


def colum_data(table, database, column):
    message,dtr_valid = dtexist(table,database)
    if(dtr_valid):
        conn, cursor = connect(database=database)
        checkquery = "SELECT " + column + " FROM  " + table
        cursor.execute(checkquery)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if data:
            return data

    return None


#pass tablename,database name, columns to check if unique or not
#in string ex.'uername,email,password' , values in list
#both columns and values length should be same
def credentials_valid(table,database, colstr, values):
    message,dtr_valid = dtexist(table,database)
    colvalsame = []
    if(dtr_valid):
        conn, cursor = connect(database=database)
        checkquery = "SELECT " + colstr + " FROM  " + table
        cursor.execute(checkquery)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        col = colstr.split(',')
        for a in range(0,len(values)):
            colvalsame.append(False)
        if (data is not None):
            if(len(values) == len(col)):
                for a in range(0,len(col)):
                    for b in data:
                        if(b[a] == values[a]):
                            colvalsame[a] = True
                            break
        return colvalsame
    return message

def password_valid(table,database,passwordstr,idstr):
    message,dtr_valid = dtexist(table,database)
    if(dtr_valid):
        conn, cursor = connect(database=database)
        passlist = passwordstr.split(':')
        passcol = passlist[0]
        password = passlist[1]
        idlist = idstr.split(':')
        colname = idlist[0]
        id = idlist[1]
        checkquery = "SELECT " + passcol + " FROM  " + table + " WHERE " + colname + " = '" + id + "'"
        cursor.execute(checkquery)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data is not None:
            if data[0] == password:
                return True
            return False
        else:
            return False


def value_info(table,database,col,idstr):
    message,dtr_valid = dtexist(table,database)
    if(dtr_valid):
        conn, cursor = connect(database=database)
        idlist = idstr.split(':')
        colname = idlist[0]
        id = idlist[1]
        checkquery = "SELECT " + col + " FROM  " + table + " WHERE " + colname + " = '" + id + "'"
        cursor.execute(checkquery)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if (data is not None):
            return data
    return None

def select_from_columns(table,database,column_dict):
    message, dbintable = dtexist(table, database)

    if dbintable:
        conn, cursor = connect(database=database)
        columns_str = ""
        column_len = len(column_dict)
        count = 1
        for column in column_dict:
            if count < column_len:
                columns_str += (column + " = '" + str(column_dict[column]) + "' and ")
            if count == column_len:
                columns_str += (column + " = '" + str(column_dict[column]) + "'")
            count += 1

        #return columns_str
        query = "SELECT * FROM " + table + " WHERE " + columns_str
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data:
            return 'Here is your data', data
        else:
            return 'There was not such data you specified in table = ' + table, data
    return 'There is no table or database your entered', None


def delete(table,database,idstr):
    row_exists = False
    message, dbintable = dtexist(table, database)

    if (dbintable):
        conn, cursor = connect(database=database)
        message,data = select(table,database,idstr)
        if (data):
            row_exists = True
            idlist = idstr.split(":")
            idcol = idlist[0]
            id = "'"+idlist[1]+"'"
    if(row_exists):
        try:
            delquery = """DELETE FROM  """ + table + """ where """+idcol+ " = " + id
            cursor.execute(delquery)
            conn.commit()
            cursor.close()
            conn.close()
            return 'Deletion of row succeded'
        except:
            return 'There was a problem deleting the ' + idcol + id
    else:
        return message

def S_TO_QS(queryvalues):
    tmplist = queryvalues.split(",")
    tmpstr = ""
    for a in range(0,len(tmplist)):
        if(a is not len(tmplist)-1):
            tmpstr += ("'"+tmplist[a]+"',")
        else:
            tmpstr += ("'" + tmplist[a] + "')")
    return tmpstr

def colums_valid(table,database,columns):
    col_valid = True
    if(dtexist(table,database)):
        conn, cursor = connect(database=database)
        columstuple = table_columns(table,database)
        collist = []
        for tuple in columstuple:
            collist.append(tuple[0])
        for a in columns:
            if(a not in collist):
                col_valid = False
        cursor.close()
        conn.close()
        return col_valid

def insert_into_table(table,database,valuestr,splitkey):

    message,dtr = dtexist(table,database)

    if(dtr):
        conn, cursor = connect(database=database)
        values = valuestr.split(splitkey)
        columns = table_columns(table,database)
        valueslen = len(values)
        columnslen = len(columns)
        #return HttpResponse(columns)
        if(columnslen == valueslen):
            insertquery = "insert into `" + table + "` values(" + S_TO_QS(valuestr)
            cursor.execute(insertquery)
            conn.commit()
            cursor.close()
            conn.close()
            return insertquery+"this query succeded"
        else:
            #check for ai columns
            if(valueslen + 1 == columnslen):

                ai_exist, ai_col_index= check_autoincreament(table,database=database,cursor=cursor)
                ai_col_index -= 1
                insvalue = ""
                values.insert(ai_col_index,NULL)
                #return HttpResponse('ai_key exist')
                for a in range(0,columnslen):
                    if (a == columnslen - 1):
                        if(values[a] == NULL):
                            insvalue += values[a]
                        else:
                            insvalue += ("'" + values[a] + "')")
                    else:
                        if (values[a] == NULL):
                            insvalue += values[a]+","
                        else:
                            insvalue += ("'" + values[a] + "',")

            insertquery = "insert into `" + table + "` values(" + insvalue
            cursor.execute(insertquery)
            conn.commit()
            cursor.close()
            conn.close()
            return 'Query Succeded '+insertquery
    else:
        return message

def is_primary(table,database,pkcol):

    is_pk = False
    columnsdata = colums_data(table, database)
    for column in columnsdata:
        if (pkcol == column['name']):
            if (column['key'] == 'PRI'):
                is_pk = True
                return is_pk
    return is_pk

def S_TO_D_AND_L(str,splitkey):
    list = str.split(splitkey)
    columns_in_str = []
    colvalues = {}
    for a in list:
        tmp = a.split('=')
        colvalues[tmp[0]] = tmp[1]
        columns_in_str.append(tmp[0])
    return colvalues,columns_in_str

def L_TO_UQS(dic):
    qs = ""
    colval = {}
    for a in dic:
        colval[a] = ("'" + dic[a] + "'")
    for a in colval:
        qs += (a + " = " + colval[a] + ",")
    qs = qs[:len(qs)-1]
    return qs

def update_table(table,database,pkstr,valuestr,splitkey):
    pk_valid = False
    col_valid = False
    query_success = False
    message, databsetablexists = dtexist(table, database)
    pklist = pkstr.split(":")
    pkcol = pklist[0]
    pk = pklist[1]
    if databsetablexists:         #if table exists
        conn, cursor = connect(database=database)       #make connection
        message, data = select(table, database, pkstr)    #if the row is in table or not
        if data is not None:
            pk_valid = is_primary(table, database, pkcol)
            colvalues,columns = S_TO_D_AND_L(valuestr,splitkey)
            col_valid = colums_valid(table,database,columns)
            if pk_valid and col_valid:
                uqs = L_TO_UQS(colvalues)
                updatequery = "update " + table + " set " + uqs + " where " + pkcol + " = " + pk
                #return HttpResponse(updatequery)
                try:
                    cursor.execute(updatequery)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    query_success = True
                    return ' Query Succeded' + updatequery, 1
                except:
                    return 'Some problem came while executing query :'+updatequery, None
        else:
            return 'there is no id '+pk + 'in table '+table, None

    if not query_success:
        return 'There was a problem executing the query', None




