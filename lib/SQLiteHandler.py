import sqlite3
import os
import re


class SQLiteHandler:

    def __init__(self, SQLiteFileName):
        self.dbFile = os.path.normpath(SQLiteFileName)
        self.conn = sqlite3.connect(self.dbFile)
        self.createDB()

    def commitSQL(self, sql):
        result = self.conn.execute(sql)
        self.conn.commit()  # maybe not neccessary?
        self.lastSQLquery = sql
        self.lastResult = result

    def createDB(self):
        queryBlock = []
        sql = "drop table if exists session;"
        queryBlock.append(sql)
        sql = "create table if not exists session('username' string UNIQUE,'filecount' string,'startdate' string,'enddate'  " \
              "string,'current_filename' string,maxsize string,para1 string,para2 string,para3 string,para4 string," \
              "para5 string,para6 string,para7 string, para8 string,para9 string,version string,PRIMARY KEY(username));"
        queryBlock.append(sql)
        sql = "drop table if exists files;"
        queryBlock.append(sql)
        sql = "create table if not exists files('ID' BIGINT UNIQUE,'basename' string, 'filename' string ," \
              "'xsize' int,'ysize' int,'image_mode' string,'file_scale' float, 'zoom_scale' float," \
              "'global_FX' string, 'skip_file' string,'Valid_Exif' int, 'ISOSpeedRatings' " \
              "float, 'ExifVersion' string,'Valid_GPS' int,'coord_ref' string, 'lat' float,'lon' float," \
              "'altitude' float,'gpsTime' string,'DateTime' string,'DateTimeOriginal' string, 'DateTimeDigitized' " \
              "string, 'FocalLength' float, 'Model' string, 'Make' string,'comment' string DEFAULT '',PRIMARY KEY(ID));"
        queryBlock.append(sql)
        sql = "drop table if exists detailed;"
        queryBlock.append(sql)
        sql = "create table if not exists detailed('ID' BIGINT UNIQUE,'username' string,'filename' string,'xpos' string," \
              "'ypos'  string,'category' string,'category_index' string,'modifier' int,'count' string,'colour' " \
              "string,'species_index' string,'group_ID' string,'tagsize' string,'lat' string,'lon' string,'altitude' " \
              "string,'gps_date' string,'cam_date' string,'save_date' string,'comment' string DEFAULT '',PRIMARY KEY(ID));"
        queryBlock.append(sql)
        for query in queryBlock:
            self.commitSQL(query)

    def insertRow(self, tableName, dictionary):
        placeholders = ', '.join(['%s'] * len(dictionary))
        for i, j in dictionary.items():
            try:
                dictionary[i] = dictionary[i].decode('string-escape')
            except:
                pass
            if j is None:
                dictionary[i] = 'None'
        values = tuple(dictionary[key] for key in dictionary.keys())
        columns = ', '.join(dictionary.keys())
        sql = "INSERT into %s (%s) VALUES %s;" % (tableName, columns, values)
        print(sql)
        self.commitSQL(sql)

    def sqlite_create_summary_table(self, conn, so):
        self.commitSQL("DROP TABLE IF EXISTS 'summary';")
        self.commitSQL("CREATE TABLE 'summary' AS SELECT * FROM files;")
        for c in so.out_clean:
            self.commitSQL("ALTER TABLE 'summary' ADD COLUMN '" + c + "' INT;")
        files = []
        sql = "SELECT filename FROM files;"
        for row in conn.execute(sql):
            files.append(row[0])
        for f in files:  # maybe group by files and then iterate?
            for c in so.out:
                sql = "SELECT sum(count),category FROM detailed WHERE filename = '" + f + "' AND category = '" + c + "';"
                val = conn.execute(sql).fetchone()[0]
                if val is None:
                    val = 0
                c2 = re.sub('[:*.!,;\s]', '_', c)  # remove evil characters
                sql = "UPDATE summary SET '" + c2 + "' = " + str(val) + " WHERE filename = '" + f + "';"
                conn.execute(sql)
                try:
                    self.pb.STEP()  # maybe remove if we include progress bar on dump
                except:
                    pass
        conn.commit()

    def deleteIDFromTable(self, ID, tableName):
        sql = "DELETE from %s where ID = %s;" % (tableName, ID)
        self.commitSQL(sql)

    def deleteFromFiles(self, fileName):
        sql = "DELETE from files where filename = %s;" % (fileName)
        self.commitSQL(sql)

    def getTable(self, tableName):
        out = []
        sql = "select * from %s;" % tableName
        for row in self.conn.execute(sql):
            out.append(row)
        return out

    def get_sqlite_from_row(self, data):
        for row in data:
            tag = dict(ID=str(row[0]), username=str(row[1]), filename=str(row[2]), xpos=str(row[3]), ypos=str(row[4]),
                       category=str(row[5]), category_index=str(row[6]), modifier=str(row[7]), count=str(row[8]),
                       colour=str(row[9]), species_index=str(row[10]), group_ID=str(row[11]), lat=str(row[12]),
                       lon=str(row[13]), altitude=str(row[14]), gps_date=str(row[15]), cam_date=str(row[16]),
                       save_date=str(row[17]))
            self.insertRow(tableName='details', dictionary=tag)

    def getDataFromImage(self, filename):
        sql = 'select ID,basename,filename,xsize,ysize,file_scale,zoom_scale,skip_file,global_FX,lat,lon,altitude,' \
              'gpsTime,DateTimeOriginal,DateTimeDigitized,Model,Make,Valid_GPS,Valid_Exif,' \
              'ISOSpeedRatings from files where filename ="%s"' % (filename)
        self.commitSQL(sql)
        ID, basename, filename, xsize, ysize, file_scale, zoom_scale, skip_file, global_FX, lat, lon, altitude, gpsTime, \
        datetimeoriginal, datetimedigitized, model, maker, valid_gps, valid_exif, isospeed = self.lastResult.fetchone()
        dictionary = dict(ID=ID, basename=basename, filename=filename, xsize=xsize, ysize=ysize,
                          file_scale=file_scale, zoom_scale=zoom_scale, skip_file=skip_file, global_FX=global_FX,
                          lat=lat,lon=lon, altitude=altitude, gpsTime=gpsTime, DateTimeOriginal=datetimeoriginal,
                          DateTimeDigitized=datetimedigitized, Model=model, Make=maker, Valid_GPS=valid_gps,
                          Valid_Exif=valid_exif, ISOSpeedRatings=isospeed)
        return dictionary


def main():
    handle = SQLiteHandler(os.path.join(os.getcwd(), 'test.db'))
    handle.createDB()


if __name__ == "__main__":
    main()
