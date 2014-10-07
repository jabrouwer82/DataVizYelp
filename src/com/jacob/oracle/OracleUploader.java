package com.jacob.oracle;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class OracleUploader {
  static final String DB_URL = "jdbc:oracle:thin:@128.83.138.158:1521:orcl";
  static final String[] DML_FILES = {
                                     "attribute.dml",
                                     "attribute_business.dml",
                                     "business.dml",
                                     "business_category.dml",
                                     "business_neighborhood.dml",
                                     "category.dml",
                                     "checkin.dml",
                                     "checkin_info.dml",
                                     "compliment.dml",
                                     "elite_year.dml",
                                     "elite_year_user.dml",
                                     "hour.dml",
                                     "neighborhood.dml",
                                     "review.dml",
                                     "user.dml",
                                     "user_friend.dml",
                                     "vote.dml"
  };

  static final String JDBC_DRIVER = "oracle.jdbc.OracleDriver";
  static final String PASS = "orcl_jab5948";

  static final String USER = "C##cs347_jab5948";

  public static void main(String[] args) {
    String inputDir = args[0];
    if (args.length < 1) {

    }
    Connection conn = null;
    Statement stmt = null;
    try {
      // STEP 2: Register JDBC driver
      Class.forName("com.mysql.jdbc.Driver");

      // STEP 3: Open a connection
      System.out.println("Connecting to database...");
      conn = DriverManager.getConnection(DB_URL, USER, PASS);

      // STEP 4: Execute a query
      System.out.println("Creating statement...");
      stmt = conn.createStatement();
      String sql;
      sql = "SELECT id, first, last, age FROM Employees";
      ResultSet rs = stmt.executeQuery(sql);

      // STEP 5: Extract data from result set
      while (rs.next()) {
        // Retrieve by column name
        int id = rs.getInt("id");
        int age = rs.getInt("age");
        String first = rs.getString("first");
        String last = rs.getString("last");

        // Display values
        System.out.print("ID: " + id);
        System.out.print(", Age: " + age);
        System.out.print(", First: " + first);
        System.out.println(", Last: " + last);
      }
      // STEP 6: Clean-up environment
      rs.close();
      stmt.close();
      conn.close();
    } catch (SQLException se) {
      // Handle errors for JDBC
      se.printStackTrace();
    } catch (Exception e) {
      // Handle errors for Class.forName
      e.printStackTrace();
    } finally {
      // finally block used to close resources
      try {
        if (stmt != null) {
          stmt.close();
        }
      } catch (SQLException se2) {
      }// nothing we can do
      try {
        if (conn != null) {
          conn.close();
        }
      } catch (SQLException se) {
        se.printStackTrace();
      }
    }
    System.out.println("Goodbye!");
  }
}
