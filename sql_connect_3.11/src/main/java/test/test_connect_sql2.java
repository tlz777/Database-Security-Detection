package test;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

import static connect.JDBCconnect.getConnection;

public class test_connect_sql2 {
    private final static String url = "jdbc:mysql://hadoop101:3306/project?useUnicode=true&characterEncoding=UTF-8&userSSL=false&serverTimezone=GMT%2B8";
    private final static String username = "root";
    private final static String password = "root";

    public static void main(String args[]) throws SQLException {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            //DriverManager.registerDriver(new sun.jdbc.odbc.JdbcOdbcDriver());
            Connection con = DriverManager.getConnection(url, username, password);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery("select * from record");
            while (rs.next()) {
                System.out.print("patino:" + rs.getInt("patino"));
                System.out.print("  illno:" + rs.getInt("illno"));
                System.out.print("  vaccination:" + rs.getString("vaccination"));
                System.out.print("  duration:" + rs.getInt("duration"));
                System.out.println("  temperature:" + rs.getFloat("temperature"));
                System.out.println("---------------------------------------------------------------------");
            }

            List<String> columnTypes = new ArrayList<>();
            //与数据库的连接
            Connection conn = getConnection();
            PreparedStatement pStemt = null;
            String tableSql ="select * from record";

                pStemt = conn.prepareStatement(tableSql);
                //结果集元数据
                ResultSetMetaData rsmd = pStemt.getMetaData();
                //表列数
                int size = rsmd.getColumnCount();
                for (int i = 0; i < size; i++) {
                    columnTypes.add(rsmd.getColumnTypeName(i + 1));
                }

            System.out.println(columnTypes);
            con.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
