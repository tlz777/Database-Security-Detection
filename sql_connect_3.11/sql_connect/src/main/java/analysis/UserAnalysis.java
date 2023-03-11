package analysis;
import connect.JDBCconnect;


import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

import static analysis.DataAnalysis.*;

public class UserAnalysis {
    public static JDBCconnect con=new JDBCconnect();
    public static List<String> records_string=new ArrayList<>();

    public static String tableNameTest="user";//等在main中用System.in来自定义设置
    //public static String databaseNameTest="mysql";//直接在连接数据库时设定为mysql即可
    public static String outputPathTest="";//等在main中用System.in来自定义设置


    public static void analysisCertainField(JDBCconnect con,String[] fields,String tableName) throws SQLException {
        String searchfields="";
        for (String field : fields) {
            searchfields+=field+",";
        }
        searchfields=searchfields.substring(0,searchfields.length()-1); //去掉最后一个逗号

        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT "+searchfields+" FROM "+ tableName);
        while (rs.next()) {
            String s="";
            for (int i=0;i<fields.length-1;i++) {
                s+=RSgetXXX(rs,fields[i],tableName)+'\t';
            }
            s+=RSgetXXX(rs,fields[fields.length-1],tableName);
            records_string.add(s);
        }

        con.closeConnection();
    }

    public static void main(String[] args) throws SQLException {
        //输入结果存放路径
        System.out.println("[tip] 请输入结果存放路径：");
        Scanner myScanner = new Scanner(System.in);
        outputPathTest=myScanner.next();

        //测试输出一张表的全信息
        //analysisAll(con,tableNameTest,databaseNameTest);
        //outPutString(records_string,outputPathTest, listToString(getAllColumnName(databaseNameTest, tableNameTest),'\t'));

        //测试获取user表的指定列信息
        String[] fields={"Host","User","authentication_string","password_last_changed"};
        analysisCertainField(con,fields,tableNameTest);
        outPutString(records_string,outputPathTest, listToString(Arrays.asList(fields),'\t'));


    }
}
