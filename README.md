# de-zcamp

DE ZoomCamp from DataTalksClub
=======
### Concepts
* [Terraform_overview](../1_terraform_overview.md)

### Execution

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
C:\Users\user>cd C:\Users\user\terraform-projects
C:\Users\user\terraform-projects>terraform init

# Check changes to new infra plan
C:\Users\user\terraform-projects>terraform plan
```

```shell
# Create new infra
C:\Users\user\terraform-projects>terraform apply
```

```shell
# Delete infra after your work, to avoid costs on any running services
C:\Users\user\terraform-projects>terraform destroy
```

