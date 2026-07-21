import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;

public final class UnsafeUserSearch {

    public static String search(
            HttpExchange exchange,
            Map<String, String> query,
            Connection connection
    ) throws Exception {

        String username = query.getOrDefault("username", "");

        // INTENTIONAL SQL INJECTION:
        // User-controlled input is concatenated into SQL.
        String sql =
            "SELECT email FROM users WHERE username = '" +
            username +
            "'";

        Statement statement = connection.createStatement();
        ResultSet result = statement.executeQuery(sql);

        return result.next()
            ? result.getString("email")
            : "Not found";
    }
}