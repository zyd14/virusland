import java.io.*;
import java.util.Scanner;

public class JPauda {

    public static boolean fileExist (String path) {
        File fdin = new File(path);
        try {
            boolean exist = fdin.exists();
            return exist;
        } catch (Exception e) {
            return false;
        }
    }

    public static String getExpect(String line) {
        int start = line.indexOf ("Expect = ") + 9;
        int end = line.length();
        return line.substring(start, end);
    }

    public static String getHit (String line) {
        return line.substring(1, line.length());
    }

    public static String getQuery (String line) {
        line = line.replaceAll("\\s+", " ");
        return line.substring(6, line.length());
    }

    public static boolean isExpect (String line) {
        return line.contains("Expect");
    }
    public static boolean isHit (String line) {
        if (line.length() > 0) {
            return line.charAt(0) == '>';
        } else {
            return false;
        }
    }
    public static boolean isQuery (String line) {
        return line.indexOf("Query=") == 0;
    }

    public static void main (String [] args) {
        if (args.length != 2) {
            System.out.println("Usage: $ java JPauda [input file] [output file]");
        } else {
            boolean finExist = fileExist(args[0]);
            if (!finExist) {
                System.out.println("File \"" + args[0] + "\" does not exist.");
                return;
            }
            File fdin = new File (args[0]);
            File fdout = new File (args[1]);
            String line = new String ("");
            String currQuery = new String ("");
            String currHit = new String ("");
            String currExp = new String("");
            String output = new String ("");
            try {
                Scanner scnr = new Scanner (fdin);
                PrintWriter pw = new PrintWriter (fdout);
                System.out.println("Processing " + args[0]);
                int lc = 0;
                while (scnr.hasNextLine()) {
                    line = scnr.nextLine();
                    lc++;
                    if (lc % 100000 == 0) {
                        System.out.println("\t" + lc + " line processed.");
                    }
                    if (isQuery(line)) {
                        currQuery = getQuery(line);
                    }
                    if (isHit(line)) {
                        currHit = getHit(line);
                    }
                    if (isExpect(line)) {
                        currExp = getExpect(line);
                        output = currQuery + "\t" + currHit + "\t" + currExp + "\n";
                        pw.printf(output);
                    }
                }
                scnr.close();
                pw.close();
            } catch (FileNotFoundException e) {
                System.out.println("File \"" + args[1] + "\" cannot be created.");
            }
        }
    }
}
