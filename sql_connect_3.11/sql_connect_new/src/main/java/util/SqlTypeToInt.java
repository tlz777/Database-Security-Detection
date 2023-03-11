package util;

import java.util.ArrayList;
import java.util.List;

public class SqlTypeToInt {
   public static String sqlType;
   public static int SqlTypeToIntFunc(){
       if (sqlType=="VARCHAR"||sqlType=="varchar") return 12;
       if (sqlType=="CHAR"||sqlType=="char") return 1;
       if (sqlType=="BLOB"||sqlType=="blob") return -4;
       if (sqlType=="TEST"||sqlType=="test") return -1;
       if (sqlType=="INTEGER"||sqlType=="integer"||sqlType=="INT"||sqlType=="int"||sqlType=="MEDIUMINT"||sqlType=="mediumint"||sqlType=="ID"||sqlType=="id") return 4;
       if (sqlType=="TINYINT"||sqlType=="tinyint") return -6;
       if (sqlType=="SMALLINT"||sqlType=="smallint") return 5;
       if (sqlType=="BIT"||sqlType=="bit"||sqlType=="BOOLEAN"||sqlType=="boolean") return -7;
       if (sqlType=="BIGINT"||sqlType=="bigint") return -5;
       if (sqlType=="FLOAT"||sqlType=="float") return 7;
       if (sqlType=="DOUBLE"||sqlType=="double") return 8;
       if (sqlType=="DECIMAL"||sqlType=="decimal") return 3;
       if (sqlType=="DATE"||sqlType=="date"||sqlType=="YEAR"||sqlType=="year") return 91;
       if (sqlType=="TIME"||sqlType=="time") return 92;
       if (sqlType=="DATETIME"||sqlType=="datetime"||sqlType=="TIMESTAMP"||sqlType=="timestamp") return 93;


       return 0;
   }

    public SqlTypeToInt() {
    }

    public SqlTypeToInt(String sqlType) {
       this.sqlType=sqlType;
    }

    public static String getSqlType() {
        return sqlType;
    }

    public static void setSqlType(String sqlType) {
        SqlTypeToInt.sqlType = sqlType;
    }

    public static void main(String[] args) {
        SqlTypeToInt varchar = new SqlTypeToInt("VARCHAR");
        System.out.println(varchar.SqlTypeToIntFunc());

    }
}
