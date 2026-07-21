import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;

import com.sun.net.httpserver.HttpExchange;

public final class UnsafeXmlParser {

    public static String parse(HttpExchange exchange) throws Exception {
        byte[] requestBody = exchange
            .getRequestBody()
            .readAllBytes();

        DocumentBuilderFactory factory =
            DocumentBuilderFactory.newInstance();

        // INTENTIONAL XXE:
        // DTDs and external entities are not disabled.
        Document document = factory
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(requestBody));

        return document.getDocumentElement().getNodeName();
    }
}