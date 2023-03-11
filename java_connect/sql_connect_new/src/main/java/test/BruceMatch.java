package test;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class BruceMatch {
    public static List<String> weakpwds=new ArrayList<>();
    public static List<String> passwords=new ArrayList<>();
    public static List<Integer> match=new ArrayList<>();
    public static void readFile() throws FileNotFoundException {
        String pathname = "D:\\Users\\DELL\\Desktop\\我的大学\\04.大二下\\数据库检测项目\\week4(8.4~8.10)\\weakpwd.txt";
        File filename = new File(pathname);
        InputStreamReader reader = new InputStreamReader(
                new FileInputStream(filename)); // 建立一个输入流对象reader
        BufferedReader br = new BufferedReader(reader); // 建立一个对象，它把文件内容转成计算机能读懂的语言

        String pathname2 = "D:\\Users\\DELL\\Desktop\\我的大学\\04.大二下\\数据库检测项目\\week4(8.4~8.10)\\passwords.txt";
        File filename2 = new File(pathname2);
        InputStreamReader reader2 = new InputStreamReader(
                new FileInputStream(filename2)); // 建立一个输入流对象reader
        BufferedReader br2 = new BufferedReader(reader2); // 建立一个对象，它把文件内容转成计算机能读懂的语言
        try {
            String line;
            while ((line = br.readLine()) != null) {
                // 一次读入一行数据
               // System.out.println(line);
                weakpwds.add(line);
            }
            String line2;
            while ((line2 = br2.readLine()) != null) {
                // 一次读入一行数据
                // System.out.println(line);
                passwords.add(line2);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    //暴力匹配算法实现
    public static void violenceMatch(){
        for (String weakpwd : weakpwds) {
            int index=passwords.indexOf(weakpwd);
            match.add(index);
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        readFile();
        violenceMatch();
        //System.out.println(weakpwds.size()+" "+passwords.size()+" "+match.size());
        //System.out.println(weakpwds.get(3)+" "+passwords.get(4)+" "+match.get(2));
        File file = new File("D:\\Users\\DELL\\Desktop\\我的大学\\04.大二下\\数据库检测项目\\week4(8.4~8.10)\\matchResult.txt");
        try {
            if(!file.exists()) {
                file.createNewFile();
            } else {
                file.delete();
                file.createNewFile();
            }
            FileWriter fw = new FileWriter(file, true);
            BufferedWriter bw = new BufferedWriter(fw);
            int index=0;
            for (String weakpwd : weakpwds) {
                bw.write(weakpwd+"\t"+match.get(index++)+"\r\n");
            }

            bw.flush();
            bw.close();
            fw.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("successfully write to file!");
    }

}
