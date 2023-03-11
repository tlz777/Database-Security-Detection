package test;

import java.sql.*;

public class test_connect_sql {
    private final static String url = "jdbc:mysql://127.0.0.1:3306/project?useUnicode=true&characterEncoding=UTF-8&userSSL=true&serverTimezone=GMT%2B8";
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
            con.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
