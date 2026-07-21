import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;

public final class UnsafeFileReader {

    public static String readDocument(
            HttpExchange exchange,
            Map<String, String> query
    ) throws IOException {

        String filename = query.getOrDefault("file", "report.txt");

        // INTENTIONAL PATH TRAVERSAL:
        // User-controlled input determines which local file is read.
        Path requestedFile = Path.of("/srv/reports/" + filename);

        return Files.readString(requestedFile);
    }
}