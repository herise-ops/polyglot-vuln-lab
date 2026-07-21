import java.io.IOException;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;

public final class UnsafeRemoteFetcher {

    public static String fetch(
            HttpExchange exchange,
            Map<String, String> query
    ) throws IOException {

        String target = query.getOrDefault(
            "url",
            "http://127.0.0.1:8081/health"
        );

        // INTENTIONAL SSRF:
        // A user-controlled URL is requested by the server.
        URL remoteUrl = URI.create(target).toURL();

        try (var stream = remoteUrl.openStream()) {
            return new String(
                stream.readAllBytes(),
                StandardCharsets.UTF_8
            );
        }
    }
}