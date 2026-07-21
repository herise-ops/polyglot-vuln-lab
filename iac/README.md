# Deliberately insecure IaC

These files exist for IaC scanner comparison. They are **not deployment templates** and must not be applied.

Expected finding themes include:

- Public network access and `0.0.0.0/0` ingress
- Public blob/container access
- HTTP allowed without HTTPS-only enforcement
- Missing encryption / key-management settings
- Hardcoded plaintext credentials
- Kubernetes privileged mode, root user, host networking, broad RBAC, and unpinned images
