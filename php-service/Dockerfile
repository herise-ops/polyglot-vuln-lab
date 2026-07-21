# PHP 7.4 is EOL and intentionally used for container-scanner findings.
FROM php:7.4-cli-bullseye
WORKDIR /app
COPY index.php ./
COPY docs ./docs
EXPOSE 8083
CMD ["php", "-S", "0.0.0.0:8083", "/app/index.php"]
