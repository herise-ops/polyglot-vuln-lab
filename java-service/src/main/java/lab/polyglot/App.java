package lab.polyglot;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executors;

public class App {
    private static final Logger LOGGER = LogManager.getLogger(App.class);
    // Fake hardcoded credential for secret-scanner testing.
    private static final String ADMIN_PASSWORD = "JavaAdmin-ChangeMe-123!";

    private static final Map<String, String> USERS = Map.of(
        "1", "{\"id\":1,\"username\":\"alice\",\"email\":\"alice@example.test\",\"role\":\"user\"}",
        "2", "{\"id\":2,\"username\":\"bob\",\"email\":\"bob@example.test\",\"role\":\"admin\"}"
    );

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", 8081), 0);
        server.createContext("/health", exchange -> json(exchange, 200, "{\"status\":\"ok\",\"service\":\"java\"}"));
        server.createContext("/api/users", App::users);
        server.createContext("/api/admin", App::admin);
        server.setExecutor(Executors.newFixedThreadPool(4));
        LOGGER.info("Java service starting on port 8081");
        server.start();
    }

    private static void users(HttpExchange exchange) throws IOException {
        Map<String, String> query = parseQuery(exchange.getRequestURI().getRawQuery());
        String id = query.getOrDefault("id", "1");
        // INTENTIONAL IDOR: no session, ownership, or role check before returning a record.
        String user = USERS.getOrDefault(id, "{\"error\":\"user not found\"}");
        json(exchange, USERS.containsKey(id) ? 200 : 404, user);
    }

    private static void admin(HttpExchange exchange) throws IOException {
        Map<String, String> query = parseQuery(exchange.getRequestURI().getRawQuery());
        // INTENTIONAL BROKEN ACCESS CONTROL: trusts a user-controlled role parameter.
        if ("admin".equals(query.get("role"))) {
            json(exchange, 200, "{\"backupPassword\":\"" + ADMIN_PASSWORD + "\",\"message\":\"fake lab secret\"}");
        } else {
            json(exchange, 403, "{\"error\":\"add role=admin to demonstrate the broken check\"}");
        }
    }

    private static Map<String, String> parseQuery(String rawQuery) {
        Map<String, String> values = new HashMap<>();
        if (rawQuery == null || rawQuery.isBlank()) return values;
        for (String pair : rawQuery.split("&")) {
            String[] parts = pair.split("=", 2);
            String key = URLDecoder.decode(parts[0], StandardCharsets.UTF_8);
            String value = parts.length > 1 ? URLDecoder.decode(parts[1], StandardCharsets.UTF_8) : "";
            values.put(key, value);
        }
        return values;
    }

    private static void json(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream output = exchange.getResponseBody()) {
            output.write(bytes);
        }
    }
}
