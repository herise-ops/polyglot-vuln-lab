output "database_password" {
  value     = aws_db_instance.insecure.password
  sensitive = false
}
