# Module 1 Homework: Docker & SQL

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

1. Install Terraform on Laptop. 

2. Copy the files from the course repo to Laptop.

3. Modify the files (see main.tf under terraform_basic folder) and create a GCP Bucket and Big Query Dataset.

GCP Bucket
   <img src="images/gcp_bucket.png" alt="GCP Bucket" width="50" height="30">
   
   
Big Query Dataset
   <img src="images/big_query_dataset.png" alt="Big Query Dataset" width="50" height="30">

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


=======
### Concepts (DE ZoomCamp from DataTalksClub)
* [Terraform_overview](../1_terraform_overview.md)

=======

