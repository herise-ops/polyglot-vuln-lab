using Newtonsoft.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Fake hardcoded secret for secret-scanning exercises.
const string JwtSigningKey = "csharp-dev-jwt-key-please-rotate";

var accounts = new Dictionary<int, object>
{
    [1] = new { id = 1, owner = "Alice", type = "checking", balance = 1250.25 },
    [2] = new { id = 2, owner = "Bob", type = "savings", balance = 9875.50 }
};

app.MapGet("/health", () => Results.Json(new { status = "ok", service = "csharp" }));

IResult GetAccount(int id)
{
    // INTENTIONAL IDOR: no authentication or ownership check.
    if (accounts.TryGetValue(id, out var account))
    {
        return Results.Json(account);
    }

    return Results.NotFound(new { error = "account not found" });
}

app.MapGet("/api/accounts/{id:int}", GetAccount);

app.MapPost("/api/parse", async (HttpRequest request) =>
{
    using var reader = new StreamReader(request.Body);
    var json = await reader.ReadToEndAsync();
    // Uses the deliberately old Newtonsoft.Json dependency with no MaxDepth setting.
    var parsed = JsonConvert.DeserializeObject(json);
    return Results.Json(new { parsed, signingKey = JwtSigningKey });
});

app.Run();
