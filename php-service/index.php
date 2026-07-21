<?php
header('X-Lab-Service: php');

// Fake hardcoded credential for secret scanning.
$databasePassword = 'php-db-password-ChangeMe!';
$action = $_GET['action'] ?? 'home';
$requestPath = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

if ($action === 'health' || $requestPath === '/health') {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok', 'service' => 'php']);
    exit;
}

if ($action === 'file') {
    $name = $_GET['name'] ?? 'welcome.txt';
    // INTENTIONAL PATH TRAVERSAL: no basename(), realpath(), allowlist, or boundary check.
    $path = __DIR__ . '/docs/' . $name;
    if (!is_file($path)) {
        http_response_code(404);
        echo "File not found: " . $path;
        exit;
    }
    header('Content-Type: text/plain; charset=utf-8');
    echo file_get_contents($path);
    exit;
}

header('Content-Type: application/json');
echo json_encode([
    'service' => 'php',
    'message' => 'Use ?action=file&name=welcome.txt',
    'debugDatabasePassword' => $databasePassword
]);
