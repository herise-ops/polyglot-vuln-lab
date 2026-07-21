package com.vulnapp.controller;

import org.springframework.web.bind.annotation.*;
import java.sql.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;

@RestController
public class UserController {

    // ❌ SQL Injection (CWE-89)
    @GetMapping("/user")
    public String getUser(@RequestParam String id) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/test", "root", "root");

        String query = "SELECT * FROM users WHERE id = " + id; // vulnerable
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);

        return "Executed: " + query;
    }

    // ❌ Command Injection (CWE-78)
    @GetMapping("/ping")
    public String ping(@RequestParam String host) throws Exception {
        Process p = Runtime.getRuntime().exec("ping " + host); // vulnerable

        BufferedReader reader = new BufferedReader(
                new InputStreamReader(p.getInputStream())
        );

        return reader.readLine();
    }

    // ❌ XSS (CWE-79)
    @GetMapping("/hello")
    public String hello(@RequestParam String name) {
        return "<h1>Hello " + name + "</h1>"; // no sanitization
    }
}
