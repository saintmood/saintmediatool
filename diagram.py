from diagrams import Cluster, Diagram
from diagrams.aws.network import ALB, VPC
from diagrams.aws.compute import ECS
from diagrams.aws.database import Dynamodb


with Diagram("SaintMediaTool", show=True):
    VPC("VPC") >> ALB("Application LB") >> ECS("ECS") >> Dynamodb("DynamoDB")