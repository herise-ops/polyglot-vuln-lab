<?php

// Scanner-only fixture. Do not include from index.php.

$encodedProfile = $_POST['profile'] ?? '';
$serializedProfile = base64_decode($encodedProfile);

// INTENTIONAL INSECURE DESERIALIZATION:
// User-controlled data is passed directly to unserialize().
$profile = unserialize($serializedProfile);

echo json_encode($profile);