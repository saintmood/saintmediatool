# saintmediatool

## Deployment
In this section you could find short manual regarding basic configuration of AWS Fargate. 
Please navigate to `./deployment/cloudformation` before moving further.

### AWS Core infrastructure setup
This setup will create a new stack with next resources: 
* VPC
* 2 subnets in 2 different AZs
* Internet Gateway
* according routing tables

*Command*:  

```bash
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-core-infrastructure --template-body file://./core-infrastructure-setup.yml
```

### AWS ECS Fargate cluster setup

```bash
aws cloudformation create-stack --stack-name ecs-fargate --capabilities CAPABILITY_IAM --template-body file://./ecs-fargate-via-cloudformation.yml
```
## Create repository

```bash
aws ecr create-repository \
--repository-name ecr-saintmediatool \
--region eu-central-1 \
--image-scanning-configuration scanOnPush=true
```