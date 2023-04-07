from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client


def main():
    # Create VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    vpc_response = vpc.create_vpc()
    print('VPC created :' + str(vpc_response))

    # Adding tag to VPC
    vpc_name = 'Boto3_VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_tag(vpc_id, vpc_name)
    print("Added name to VPC")

    # Create Internet gateway
    igw_response = vpc.create_ig()
    print("IG created")

    # getting internet gateway id
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # creating subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    # Adding name tag to public subnet
    vpc.add_tag(public_subnet_id, 'Boto-3-Public-subnet')

    # creating public route table
    public_rtb_response = vpc.create_route_table(vpc_id)
    rtb_id = public_rtb_response['RouteTable']['RouteTableId']
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associating subnet to route Table
    vpc.associate_subnet_to_rtb(rtb_id, public_subnet_id)

    # Allow auto assign public ip address for subnet
    vpc.allow_auto_assign_ip_address_for_subnet(public_subnet_id)

    # Creating private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    print("Created private subnet")

    # Adding name tag to private subnet
    vpc.add_tag(private_subnet_id, 'Boto-3-Private-subnet')
    print("Tag added to subnet")

    # EC2 Instances
    ec2 = EC2(ec2_client)


    # Creating KeyPair
    key_pair_name = 'Boto3-key-pair'
    key_pair_response = ec2.create_key_pair(key_pair_name)
    print("KeyPair created " + str(key_pair_response))

    # Creating security group
    public_security_grp_name = 'Boto3-sec-grp'
    description = 'Public security group for public subnet internet access'
    public_security_grp_response = ec2.create_security_grp( public_security_grp_name, description, vpc_id)
    security_grp_id = public_security_grp_response['Group_Id']

    # Adding public access to the security group
    ec2.add_inbound_rule(security_grp_id)

    # Start up script for EC2
    user_data = """ #!/bin/bash
                yum update -y
                yum install httpd24 -y
                service httpd24 start
                chkconfig httpd on
                echo "<html><body><h1>Welcome to our code using <b>Boto3</b></h1></body></html> > /var/www/html/index.html"""

    # Launching EC2 instance using AMI and public subnet
    ec2.launch_ec2_instance('ami-0376ec8eacdf70aae', key_pair_name, 1, 1, 't2.micro', security_grp_id, public_subnet_id, user_data)

    # Adding annother security group for private EC2 Instance
    private_security_grp_name='Boto3-private-SG'
    private_security_description='Private security group for private subnet'
    private_security_grp_response = ec2.create_security_grp( private_security_grp_name, private_security_description)

    private_security_grp_id = private_security_grp_response['GroupId']
    ec2.add_inbound_rule(private_security_grp_id)

    # Launching EC2 instance using AMI and private subnet
    ec2.launch_ec2_instance('ami-0376ec8eacdf70aae', key_pair_name, 1, 1, 't2.micro', private_security_grp_id, private_subnet_id, """""")


if __name__ == '__main__':
    main()

