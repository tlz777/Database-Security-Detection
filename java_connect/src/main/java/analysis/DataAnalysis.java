package analysis;

import connect.JDBCconnect;
import entity.Country;
import util.SqlTypeToInt;

import java.io.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;


public class DataAnalysis {
    public static JDBCconnect con=new JDBCconnect();
    public static List<String> records_string=new ArrayList<>();
    public static List<String> filterColumnnames=new ArrayList<>();

    public static String tableNameTest="";//等在main中用System.in来自定义设置
    public static String databaseNameTest=con.getDatabasename();//这里直接用连接mysql时的数据库
    public static String outputPathTest="";//等在main中用System.in来自定义设置

    //如果main中不需要调用排序函数，则不用管下面两个变量
    public static List<String> sortListsTest= Arrays.asList("duration","temperature");
    public static boolean ifascTest=false;


    //满足广适！
    public static void analysisAll(JDBCconnect con,String tableName,String databaseName) throws SQLException {
        records_string.clear();
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("select * from "+tableName);
        //获取数据库表中所有字段名称
        List<String> allColumnName = getAllColumnName(databaseName, tableName);
        while (rs.next()) {
            String s="";
            for (int i=0;i<allColumnName.size()-1;i++) {
                s+=RSgetXXX(rs,allColumnName.get(i),tableName)+',';
            }
            s+=RSgetXXX(rs,allColumnName.get(allColumnName.size()-1),tableName);
            records_string.add(s);
        }
        con.closeConnection();
    }

    //需改进，ifasc应该是个数组，对每个字段进行排序
    public static void analysisSort(JDBCconnect con,String tableName,String databaseName,List<String> sortLists,boolean ifasc) throws SQLException {
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        String sortString=listToString(sortLists,',');
        String sql="";
        if(ifasc){
            sql="select * from "+tableName+" order by "+sortString+" asc;";
        }
        else{
            sql="select * from "+tableName+" order by "+sortString+" desc;";
        }
        ResultSet rs = stmt.executeQuery(sql);
        //获取数据库表中所有字段名称
        List<String> allColumnName = getAllColumnName(databaseName, tableName);
        while (rs.next()) {
            String s="";
            for (int i=0;i<allColumnName.size()-1;i++) {
                s+=RSgetXXX(rs,allColumnName.get(i),tableName)+',';
            }
            s+=RSgetXXX(rs,allColumnName.get(allColumnName.size()-1),tableName);
            records_string.add(s);
        }
        con.closeConnection();
    }

    //需改进广适！分组不太好弄聚合操作是什么，看后续项目有无必要调用进行修改
    public static void analysisGroup(JDBCconnect con) throws SQLException {
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT region,count(*) FROM tb_country group by region;");

        while (rs.next()) {
            String s=rs.getString("region")+','+rs.getInt("count(*)");
            records_string.add(s);
        }
        con.closeConnection();
    }

    //满足广适！
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
                s+=RSgetXXX(rs,fields[i],tableName)+',';
            }
            s+=RSgetXXX(rs,fields[fields.length-1],tableName);
            records_string.add(s);
        }

        con.closeConnection();
    }

    public static void analysisTypeFilter(JDBCconnect con,String[] filtertypes,String tableName,String databaseName) throws SQLException {
        for (String filtertype : filtertypes) {
            //获得该类型的int值
            SqlTypeToInt stti = new SqlTypeToInt(filtertype);
            int inttype=stti.SqlTypeToIntFunc();
            //获取数据库表中所有字段名称
            List<String> allColumnName = getAllColumnName(databaseName, tableName);
            //判断每个字段名称的类型是否与filtertype一致；若一致，将该字段名称加入filterColumnnames
            boolean ifexsitsfiltertype=false;
            for (String ColumnName : allColumnName) {
                if(getOneFieldTypeInt(ColumnName,tableName)==inttype){
                    ifexsitsfiltertype=true;
                    filterColumnnames.add(ColumnName);
                }
            }
            //表中没有这个类型，没法过滤出来
            if(ifexsitsfiltertype==false)
            {
                System.out.println("warnning：表中没有"+filtertype+"类型的字段，无法过滤出该类型信息");
                List<String> columnTypes = getAllFieldTypeName(tableName);
                System.out.println("tip：表中所含字段类型为："+columnTypes);
            }
        }
        System.out.println("info：过滤出的字段名称为："+filterColumnnames);

        //开始执行过滤字段的查询
        if (filterColumnnames.size()==0){
            System.out.println("表中字段类型均不满足过滤条件，无法执行数据过滤提取，请重新选择过滤字段类型！");
            List<String> columnTypes = getAllFieldTypeName(tableName);
            System.out.println("tip：表中所含字段类型为："+columnTypes);
            return ;
        }
        String searchfields="";
        for (String field : filterColumnnames) {
            searchfields+=field+",";
        }
        searchfields=searchfields.substring(0,searchfields.length()-1); //去掉最后一个逗号

        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT "+searchfields+" FROM "+ tableName);
        while (rs.next()) {
            String s="";
            for (int i=0;i<filterColumnnames.size()-1;i++) {
                s+=RSgetXXX(rs,filterColumnnames.get(i),tableName)+',';
            }
            s+=RSgetXXX(rs,filterColumnnames.get(filterColumnnames.size()-1),tableName);
            records_string.add(s);
        }

        con.closeConnection();

    }

    //需改进广适！  不用这个了，用下面那个广适outPutString
    public static void outPut(List<Country> records,String path){
        File file = new File(path);
        try {
            if(!file.exists()) {
                file.createNewFile();
            } else {
                file.delete();
                file.createNewFile();
            }
            FileWriter fw = new FileWriter(file, true);
            BufferedWriter bw = new BufferedWriter(fw);
            //书写表头
            String head = "code"+ ',' +"name"+ ',' +"region"+ "\r\n";
            bw.write(head);
            //书写内容
            for(Country country:records) {
                bw.write(country.toString()+"\r\n");
            }
            bw.flush();
            bw.close();
            fw.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("successfully write to file!");
    }

    //满足广适！
    public static void outPutString(List<String> records_string,String path,String head){
        File file = new File(path);
        try {
            if(!file.exists()) {
                file.createNewFile();
            } else {
                file.delete();
                file.createNewFile();
            }
            FileWriter fw = new FileWriter(file, true);
            BufferedWriter bw = new BufferedWriter(fw);
            //书写表头
            bw.write(head+"\r\n");
            //书写内容
            for(String s:records_string) {
                bw.write(s+"\r\n");
            }
            bw.flush();
            bw.close();
            fw.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("[success] 数据分析结果成功写入"+outputPathTest);
    }

    //得到所有列的类型（返回类型名称字符串数组）
    public static List<String> getAllFieldTypeName(String tableName) throws SQLException {
        List<String> columnTypes = new ArrayList<>();
        //与数据库的连接
        Connection connection = con.getConnection();
        PreparedStatement pStemt = null;
        String tableSql ="SELECT * FROM " + tableName;
        pStemt = connection.prepareStatement(tableSql);
        //结果集元数据
        ResultSetMetaData rsmd = pStemt.getMetaData();
        //表列数
        int size = rsmd.getColumnCount();
        for (int i = 0; i < size; i++) {
            columnTypes.add(rsmd.getColumnTypeName(i + 1));
        }
        return columnTypes;
    }

    //得到所有列的类型（返回JDBC的int类型数组）
    public static List<Integer> getAllFieldTypeInt(String tableName)throws SQLException{
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();

        ResultSet rs = stmt.executeQuery("SELECT * FROM " + tableName);
        ResultSetMetaData meta = rs.getMetaData();
        int columnCount = meta.getColumnCount();
        List<Integer> result=new ArrayList<>();
        for (int i = 0; i < columnCount; i++)
        {
            Integer field;
            int cursor = i + 1;
            field = meta.getColumnType(cursor);
            result.add(field);
        }
        return result;
    }

    //得到自定义某些列的类型（返回JDBC的int类型数组）
    public static List<Integer> getSomeFieldTypeInt(String[] fields,String tableName)throws SQLException{
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        String searchfields="";
        for (String field : fields) {
            searchfields+=field+",";
        }
        searchfields=searchfields.substring(0,searchfields.length()-1); //去掉最后一个逗号
        // System.out.println(searchfields);
        ResultSet rs = stmt.executeQuery("SELECT "+searchfields+" FROM "+ tableName);
        ResultSetMetaData meta = rs.getMetaData();
        int columnCount = meta.getColumnCount();
        List<Integer> result=new ArrayList<>();
        for (int i = 0; i < columnCount; i++)
        {
            Integer field;
            int cursor = i + 1;
            field = meta.getColumnType(cursor);
            result.add(field);
        }
        return result;
    }

    //得到自定义某一个列的类型（返回JDBC的int类型）
    public static Integer getOneFieldTypeInt(String fieldName,String tableName)throws SQLException{
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT "+fieldName+" FROM "+ tableName);
        ResultSetMetaData meta = rs.getMetaData();
        Integer result;
        result= meta.getColumnType(1);  //注意不是0！
        return result;
    }

    //执行不同类型的rs查询
    public static String RSgetXXX(ResultSet rs,String fieldName,String tableName) throws SQLException {
        Integer type = getOneFieldTypeInt(fieldName, tableName);
        if(type==12||type==1||type==-1)return rs.getString(fieldName);
        if(type==-6|type==5||type==4)return String.valueOf(rs.getInt(fieldName));
        if(type==-5)return String.valueOf(rs.getLong(fieldName));
        if(type==-7)return String.valueOf(rs.getBoolean(fieldName));
        if(type==7)return String.valueOf(rs.getFloat(fieldName));
        if(type==8)return String.valueOf(rs.getDouble(fieldName));
        if(type==3)return String.valueOf(rs.getBigDecimal(fieldName));
        if(type==-4)return String.valueOf(rs.getBlob(fieldName));
        if(type==91)return String.valueOf(rs.getDate(fieldName));
        if(type==92)return String.valueOf(rs.getTime(fieldName));
        if(type==93)return String.valueOf(rs.getTimestamp(fieldName));
        return "not found!";
    }

    //获取数据库表中的全部字段名称
    public static List<String> getAllColumnName(String databaseName,String tableName) throws SQLException {
        List<String> ColumnNames=new ArrayList<>();
        Connection connection = con.getConnection();
        DatabaseMetaData meta = connection.getMetaData();
        ResultSet resultSet = meta.getColumns(databaseName, null, tableName, "%");
        while (resultSet.next()) {
            String ColumnName=resultSet.getString(4);
            ColumnNames.add(ColumnName);
        }
        return ColumnNames;
    }

    public static List<String> getAllTableName() throws SQLException {
        List<String> TableNames=new ArrayList<>();
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("show tables;");
        while (rs.next()) {
            String TableName=rs.getString(1);
            TableNames.add(TableName);
        }
        con.closeConnection();
        return TableNames;
    }

    //输出数据库的所有表信息到指定路径
    public static void outputDBinfo() throws SQLException {
        List<String> tbnames=getAllTableName();
        for (String tbname : tbnames) {
            analysisAll(con,tbname,databaseNameTest);
            System.out.println(tbname+"    "+outputPathTest+"/"+tbname+".csv");
            outPutString(records_string,outputPathTest+"/"+tbname+".csv", listToString(getAllColumnName(databaseNameTest, tbname),','));

        }
    }

    //把字符串lists转换为按某字符分割的字符串
    public static String listToString (List<String> contents, char split){
        String s="";
        for (int i=0;i<contents.size()-1;i++) {
            s+=contents.get(i)+split;
        }
        s+=contents.get(contents.size()-1);
        return s;
    }

    //输出密码强度检测，有点bug
    public static int PwdStrengthScore(JDBCconnect con) throws SQLException {
        String pwd=con.getPwd();
        System.out.println("[success] 获取连接密码为："+pwd);
        Connection connection = con.getConnection();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("select validate_password_strength('"+pwd+"')");
        while (rs.next()) {
            String s=rs.getString("validate_password_strength('"+pwd+"')");
            System.out.println("[tip] 密码强度为："+s);
        }

        con.closeConnection();
        return 0;
    }
    public static void main(String[] args) throws SQLException, IOException, InterruptedException {


    /*   analysisGroup(con);
        outPutString(records_string,"G:\\yingwenlujing\\output\\shujvkujiance\\DataOutPut3.txt",
                "region"+ ',' +"count(*)");
     */

    /*    String[] fields={"patino","illno","vaccination","temperature"};
          analysisCertainField(con,fields,"record");

        //设置输出文件的表头
        String head="";
        for (int i=0;i<fields.length-1;i++) {
            head+=fields[i]+',';
        }
        head+=fields[fields.length-1];
       outPutString(records_string,"G:\\yingwenlujing\\output\\shujvkujiance\\DataOutPut4.txt", head);
    */

        //List<Integer>result=getAllFieldTypeInt("record");System.out.println(result);
        // List<Integer>result=getSomeFieldTypeInt(fields,"record");System.out.println(result);
        //Integer field = getOneFieldTypeInt("patino", "record");System.out.println(field);

        //List<String> allColumnName = getAllColumnName("project", "record"); System.out.println(allColumnName);

        /*String[] filterTypes={"double","boolean"};
        analysisTypeFilter(con,filterTypes,"record","project");

        if(filterColumnnames.size()!=0){

            //设置输出文件的表头
            String head="";
            for (int i=0;i<filterColumnnames.size()-1;i++) {
                head+=filterColumnnames.get(i)+',';
            }
            head+=filterColumnnames.get(filterColumnnames.size()-1);
            outPutString(records_string,"G:\\yingwenlujing\\output\\shujvkujiance\\DataOutPut5.txt", head);
        }*/

        //测试anlysisAll普适性
        //analysisAll(con,tableNameTest,databaseNameTest);
        //outPutString(records_string,outputPathTest, listToString(getAllColumnName(databaseNameTest, tableNameTest),','));

        //测试analysisSort普适性
        //analysisSort(con,tableNameTest,databaseNameTest, sortListsTest,ifascTest);
        //outPutString(records_string,outputPathTest, listToString(getAllColumnName(databaseNameTest, tableNameTest),','));

        //输入需要分析的表名
        System.out.println("[tip] 请输入待分析数据表名：");
        Scanner myScanner = new Scanner(System.in);
        tableNameTest=myScanner.next();

        //输入结果存放路径
       // System.out.println("[tip] 请输入结果存放路径：");
       // myScanner = new Scanner(System.in);
        outputPathTest="DetectTempFile";
        //创建文件夹
        File directory = new File(outputPathTest);
        //mkdir
        boolean hasSucceeded = directory.mkdir();
        System.out.println("创建文件夹结果（不含父文件夹）：" + hasSucceeded);

        //测试密码强度
        //PwdStrengthScore(con);//测试con对应的密码

        //测试输出一张表的全信息
        //analysisAll(con,tableNameTest,databaseNameTest);
        //outPutString(records_string,outputPathTest, listToString(getAllColumnName(databaseNameTest, tableNameTest),','));

        //测试输出数据库所有表名
        //outPutString(records_string,outputPathTest, listToString(getAllTableName(),','));

        //测试输出数据库所有表的全信息
        outputDBinfo();
        //调用python文件并获得命令行输出
        //获取父文件夹
        String parentPath = new File("").getAbsolutePath();
        String commonPath= new File(parentPath).getParent();
        String pyPath=commonPath+"/py_api/main.py";
        Runtime run = Runtime.getRuntime();
        Process process = run.exec("python "+pyPath);
        System.out.println("python "+pyPath);
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line = null;
        while ((line = in.readLine()) != null) {
            System.out.println(line);
        }
        in.close();
        int re = process.waitFor();
        System.out.println(re);
    }
}


