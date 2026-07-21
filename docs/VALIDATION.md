# Validation notes

The repository was checked before packaging with the following local validations:

- TypeScript gateway: dependencies installed, TypeScript compiled, server started, and `/`, `/health`, and `/api/admin/config` responded.
- Browser JavaScript: syntax checked with Node.js.
- Python service: Flask test client verified health, normal search, the intentional SQL-injection behavior, and safe command simulation.
- Java service: source compiled and the health, IDOR, and broken-role-check endpoints were exercised using temporary logging API stubs. The packaged Maven build uses the declared Log4j dependency.
- PHP service: syntax checked, built-in server started, and health/file routes were exercised.
- C# service: C# source parsed without syntax errors; the project XML is well formed.
- IaC: Docker Compose and Kubernetes YAML parsed successfully; Terraform HCL parsed successfully.
- JSON/XML manifests and shell-script syntax were checked.

A Docker daemon and .NET/GnuCOBOL toolchains were not available in the packaging environment, so the complete multi-container Compose stack was not executed end-to-end here. The repository includes Dockerfiles and a smoke-test script for that final environment-level check.
