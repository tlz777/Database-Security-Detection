package connect;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Scanner;

public class JDBCconnect {
    static {
        System.out.println("[tip] 请依次输入：主机地址 端口号 数据库名称 用户名 密码，示例：hadoop101 3306 project root root");
    }
    private static final Scanner myScanner = new Scanner(System.in);
    //连接数据库，根据自己情况修改
    private static final String driverManager="com.mysql.cj.jdbc.Driver";
    //System.out.println("请输入主机名：");
    private static final String ip=myScanner.next();//hadoop101
    private static final String port=myScanner.next();//3306
    private static final String databasename=myScanner.next();//project数据库
    private static final String url="jdbc:mysql://"+ip+":"+port+"/"+databasename+"?characterEncoding=utf-8" +
            "useUniCode=true&&characterEncoding=UTF-8&&serverTimezone=GMT%2B8";
    private static final String username=myScanner.next();//root
    private static final String password=myScanner.next();//root
    private static Connection conn=null;
    public static Connection getConnection(){

        try {
            Class.forName(driverManager);
            conn = DriverManager.getConnection(url, username, password);
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }
    public static String getPwd(){
        return password;
    }
    public static void closeConnection() throws SQLException {
        conn.close();
    }
}
