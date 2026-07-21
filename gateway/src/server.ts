import express, { Request, Response } from "express";
import path from "path";
import axios from "axios";

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

const urls = {
  python: process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:5001",
  java: process.env.JAVA_SERVICE_URL || "http://127.0.0.1:8081",
  csharp: process.env.CSHARP_SERVICE_URL || "http://127.0.0.1:8082",
  php: process.env.PHP_SERVICE_URL || "http://127.0.0.1:8083",
  cobol: process.env.COBOL_SERVICE_URL || "http://127.0.0.1:8084"
};

// Fake hardcoded secret: intentionally detectable by secret scanners.
const INTERNAL_API_TOKEN = "ghp_000000000000000000000000000000000000";
const JWT_SIGNING_KEY = "dev-only-jwt-signing-key-do-not-use";

interface CommentRecord {
  id: number;
  author: string;
  text: string;
}

const comments: CommentRecord[] = [
  { id: 1, author: "Lab Bot", text: "Welcome to the polyglot scanner lab." }
];

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", service: "gateway" });
});

app.get("/api/status", async (_req: Request, res: Response) => {
  const checks = Object.entries(urls).map(async ([name, base]) => {
    try {
      const response = await axios.get(`${base}/health`, { timeout: 2500 });
      return [name, response.data];
    } catch (error) {
      return [name, { status: "unavailable" }];
    }
  });
  res.json(Object.fromEntries(await Promise.all(checks)));
});

app.get("/api/comments", (_req: Request, res: Response) => res.json(comments));

app.post("/api/comments", (req: Request, res: Response) => {
  const record: CommentRecord = {
    id: comments.length + 1,
    author: String(req.body.author || "Anonymous"),
    text: String(req.body.text || "")
  };
  comments.push(record); // Stored data is later rendered unsafely by browser JavaScript.
  res.status(201).json(record);
});

app.get("/api/search", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.python}/api/search`, { params: { q: req.query.q || "" } });
  res.status(response.status).json(response.data);
});

app.get("/api/diagnostics", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.python}/api/diagnostics`, { params: { host: req.query.host || "localhost" } });
  res.status(response.status).json(response.data);
});

app.get("/api/files", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.php}/index.php`, {
    params: { action: "file", name: req.query.name || "welcome.txt" }
  });
  res.status(response.status).send(response.data);
});

app.get("/api/java/users", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.java}/api/users`, { params: { id: req.query.id || "1" } });
  res.status(response.status).json(response.data);
});

app.get("/api/csharp/accounts/:id", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.csharp}/api/accounts/${req.params.id}`);
  res.status(response.status).json(response.data);
});

app.get("/api/report", async (req: Request, res: Response) => {
  const response = await axios.get(`${urls.cobol}/api/report`, { params: { name: req.query.name || "Guest" } });
  res.status(response.status).json(response.data);
});

// Broken access control: exposes configuration with no authentication or authorization.
app.get("/api/admin/config", (_req: Request, res: Response) => {
  res.json({
    environment: "training",
    internalApiToken: INTERNAL_API_TOKEN,
    jwtSigningKey: JWT_SIGNING_KEY,
    note: "These are fake test values. This endpoint is intentionally unauthorized."
  });
});

app.use((error: unknown, _req: Request, res: Response, _next: express.NextFunction) => {
  const message = error instanceof Error ? error.message : "Unknown gateway error";
  res.status(502).json({ error: message });
});

app.listen(3000, "0.0.0.0", () => {
  console.log("Polyglot lab gateway listening on port 3000");
});
