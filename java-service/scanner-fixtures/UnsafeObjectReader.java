import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.ObjectInputStream;

public final class UnsafeObjectReader {

    public static Object readObject(HttpExchange exchange)
            throws IOException, ClassNotFoundException {

        // INTENTIONAL INSECURE DESERIALIZATION:
        // Untrusted request data is passed to ObjectInputStream.
        ObjectInputStream input = new ObjectInputStream(
            exchange.getRequestBody()
        );

        return input.readObject();
    }
}