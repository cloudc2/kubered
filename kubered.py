#!/usr/bin/env python


import subprocess
import sys
import os
import json
import shutil
#import yaml
import time


# python2/3 compatability
try:
    input = raw_input
except NameError:
    pass

kubered_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.isfile(kubered_path + '/config.json'):
    print('Initializing config.json from config.json.example')
    shutil.copy(kubered_path + '/config.json.example',kubered_path + '/config.json')

with open(kubered_path + '/config.json') as config:
    config_parser = json.load(config)

with open(kubered_path + '/config.json.example') as defaults:
    default_config = json.load(defaults)

cloudProvider = config_parser['cloudProvider']
awscliPath = config_parser['awscliPath']
kopsPath = config_parser['kopsPath']
kubectlPath = config_parser['kubectlPath']
sshPublicKey = config_parser['sshPublicKey']
ingressEngine = config_parser['ingressEngine']
S3BucketName = config_parser['S3BucketName']
AWSZone = config_parser['AWSZone']
AWSMasterSize = config_parser['AWSMasterSize']
AWSNodeSize = config_parser['AWSNodeSize']
AWSNetworking = config_parser['AWSNetworking']
AWSTopology = config_parser['AWSTopology']
HACluster = config_parser['HACluster']
gossipBasedCluster = config_parser['gossipBasedCluster']
masterCount = config_parser['masterCount']
dockerHubUserName = config_parser['dockerHubUserName']
dockerHubPassword = config_parser['dockerHubPassword']
dockerEmail = config_parser['dockerEmail']
clusterName = ""

# Help
def usage():
    print("usage: python kubered.py <hash_file> <hash_type>/n")

def check_agreement():
    if not os.path.isfile(kubered_path + '/.agree'):
        with open(kubered_path + "/agreement.txt") as agreement:
            print(agreement.read())
        answer = input("Do you agree? ")
        if answer == "Yes" or answer == "yes" or answer == "y" or answer == "Y":
            open('.agree', 'a').close()
        else:
            quit_kr()
    else:
        return


def ascii_art():
    print(r"""

$$\   $$\          $$\                                           $$\
$$ | $$  |         $$ |                                          $$ |
$$ |$$  /$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ |
$$$$$  / $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$ |
$$  $$<  $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$$$$$$$ |$$ /  $$ |
$$ |\$$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$   ____|$$ |  $$ |
$$ | \$$\\$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      \$$$$$$$\ \$$$$$$$ |
\__|  \__|\______/ \_______/  \_______|\__|       \_______| \_______|
                          Version 0.5
  """)


# Pick Which cloud to use
def pick_cloud():
    print("pick the cloud\n")


# Pick the ingress controller
def pick_ingress():
    print("Pick ingress controller\n")


# Pick the C2 server type
def pick_c2():
    print("Pick C2 server type\n")


def name_cluster():
    global clusterName
    while 1:
        clusterName = input("\nEnter Cluster Name:")
        return clusterName

#def external_dns():
    with open('DeployFiles/externalDNS.tpl', 'r') as input_file:
        results = yaml_as_python(input_file)
        print(results)
        for value in results:
            print(value)


def change_config():
    print("Coming Soon, for now quit the script, edit config.json, and run the script again\n")


def get_elb():
    elb = subprocess.check_output("kubectl get svc istio-ingressgateway -n istio-system -o json", shell=True)
    json_parser = json.load(elb)
    elbName = json_parser['uid']
    print(elbName)

def bootstrap_cluster():
    process1 = subprocess.Popen("kubectl apply -f istio/istio-1.3.2/install/kubernetes/helm/helm-service-account.yaml",
                                shell=True)
    try:
        process1.wait()
    except KeyboardInterrupt:
        process1.kill()
    time.sleep(15)
    process2 = subprocess.Popen("helm init --service-account tiller", shell=True)
    try:
        process2.wait()
    except KeyboardInterrupt:
        process2.kill()
    time.sleep(15)
    process3 = subprocess.Popen(
        "helm install istio/istio-1.3.2/install/kubernetes/helm/istio-init --name istio-init --namespace istio-system",
        shell=True)
    try:
        process3.wait()
    except KeyboardInterrupt:
        process3.kill()
    time.sleep(15)
    process4 = subprocess.Popen(
        "helm install istio/istio-1.3.2/install/kubernetes/helm/istio --name istio --namespace istio-system --values istio/istio-1.3.2/install/kubernetes/helm/istio/values-istio-demo.yaml",
        shell=True)
    try:
        process4.wait()
    except KeyboardInterrupt:
        process4.kill()
    time.sleep(15)
    process5 = subprocess.Popen("kubectl label namespace default istio-injection=enabled", shell=True)
    try:
        process5.wait()
    except KeyboardInterrupt:
        process5.kill()
    time.sleep(15)

def deploy_cobalt():
    process6 = subprocess.Popen(
        "kubectl create secret docker-registry {secret_name} --docker-username={user_name} "
        "--docker-password={docker_pass} --docker-email={docker_email}".format(
            secret_name="regcred",
            user_name=dockerHubUserName,
            docker_pass=dockerHubPassword,
            docker_email=dockerEmail), shell=True)
    try:
        process6.wait()
    except KeyboardInterrupt:
        process6.kill()
    time.sleep(15)
    process7 = subprocess.Popen("helm install charts/teamserver-chart --name=teamserver1", shell=True)
    try:
        process7.wait()
    except KeyboardInterrupt:
        process7.kill()
    time.sleep(15)
    process8 = subprocess.Popen("kubectl apply -f istio/istio-yaml/teamserver/ts-tls-gateway.yaml", shell=True)
    try:
        process8.wait()
    except KeyboardInterrupt:
        process8.kill()
    time.sleep(15)
    process9 = subprocess.Popen("kubectl apply -f istio/istio-yaml/teamserver/admin-virtual-service.yaml", shell=True)
    try:
        process9.wait()
    except KeyboardInterrupt:
        process9.kill()
    print("finished!!\n")


def deploy_merlin():
    process7 = subprocess.Popen("helm install charts/merlin-chart --name=merlin1", shell=True)
    try:
        process7.wait()
    except KeyboardInterrupt:
        process7.kill()
    time.sleep(15)
    process8 = subprocess.Popen("kubectl apply -f istio/istio-yaml/merlin/merlin-gateway.yaml", shell=True)
    try:
        process8.wait()
    except KeyboardInterrupt:
        process8.kill()
    time.sleep(15)
    process9 = subprocess.Popen("kubectl apply -f istio/istio-yaml/merlin/merlin-virtual-service.yaml", shell=True)
    try:
        process9.wait()
    except KeyboardInterrupt:
        process9.kill()
    print("finished!!\n")

def deploy_silent():
    process7 = subprocess.Popen("helm install charts/silenttrinity-chart --name=silenttrinity1", shell=True)
    try:
        process7.wait()
    except KeyboardInterrupt:
        process7.kill()
    time.sleep(15)
    process8 = subprocess.Popen("kubectl apply -f istio/istio-yaml/silenttrinity/silenttrinity-gateway.yaml", shell=True)
    try:
        process8.wait()
    except KeyboardInterrupt:
        process8.kill()
    time.sleep(15)
    process9 = subprocess.Popen("kubectl apply -f istio/istio-yaml/silenttrinity/silenttrinity-virtual-service.yaml", shell=True)
    try:
        process9.wait()
    except KeyboardInterrupt:
        process9.kill()
    print("finished!!\n")

def deploy_covenant():
    process7 = subprocess.Popen("helm install charts/covenant-chart --name=covenant1", shell=True)
    try:
        process7.wait()
    except KeyboardInterrupt:
        process7.kill()
    time.sleep(15)
    process8 = subprocess.Popen("kubectl apply -f istio/istio-yaml/covenant/covenant-gateway.yaml", shell=True)
    try:
        process8.wait()
    except KeyboardInterrupt:
        process8.kill()
    time.sleep(15)
    process9 = subprocess.Popen("kubectl apply -f istio/istio-yaml/covenant/covenant-virtual-service.yaml", shell=True)
    try:
        process9.wait()
    except KeyboardInterrupt:
        process9.kill()
    print("finished!!\n")

def deploy_gophish():
    print("deploying Gophish\n")
    process1 = subprocess.Popen("kubectl apply -f dockerfiles/gophish/deploy.yaml", shell=True)
    try:
        process1.wait()
    except KeyboardInterrupt:
        process1.kill()

def create_cluster():
    global clusterName
    print("Creating Kubernetes Cluster\n")
    if gossipBasedCluster == "yes" or gossipBasedCluster == "Yes":
        fullClusterName = clusterName + ".k8s.local"
    else:
        fullClusterName = clusterName
    kopsProcess = subprocess.Popen(
        "{kops_path}  create cluster --zones {AWS_zones} --topology {AWS_Topology} --networking {AWS_Networking} "
        "--master-size {AWS_Master_Size} --master-count {AWS_Master_Count} --node-size {AWS_Node_Size} --name "
        "{cluster_Name} --state={AWS_Bucket_Name} --yes".format(
            kops_path=kopsPath,
            AWS_zones=AWSZone,
            AWS_Topology=AWSTopology,
            AWS_Networking=AWSNetworking,
            AWS_Master_Size=AWSMasterSize,
            AWS_Master_Count=masterCount,
            AWS_Node_Size=AWSNodeSize,
            cluster_Name=fullClusterName,
            AWS_Bucket_Name=S3BucketName), shell=True)
    try:
        kopsProcess.wait()
    except KeyboardInterrupt:
        print('Killing PID {0}...'.format(str(kopsProcess.pid)))
        kopsProcess.kill()


def cluster_status():
    global clusterName
    print("Checking Cluster status of " + clusterName + "\n")
    if gossipBasedCluster == "yes" or gossipBasedCluster == "Yes":
        fullClusterName = clusterName + ".k8s.local"
    else:
        fullClusterName = clusterName
    kopsProcess = subprocess.Popen(
        "{kops_path}  validate cluster --name "
        "{cluster_Name} --state={AWS_Bucket_Name}".format(
            kops_path=kopsPath,
            cluster_Name=fullClusterName,
            AWS_Bucket_Name=S3BucketName), shell=True)
    try:
        kopsProcess.wait()
    except KeyboardInterrupt:
        print('Killing PID {0}...'.format(str(kopsProcess.pid)))
        kopsProcess.kill()

def list_pods():
    process1 = subprocess.Popen("kubectl get pods --show-labels", shell=True)
    try:
        process1.wait()
    except KeyboardInterrupt:
        process1.kill()

def delete_cluster():
    global clusterName
    confirm = input("Are you sure you want to delete the cluster " + clusterName + "? ")
    if confirm == "yes" or confirm == "Yes" or confirm == "y" or confirm == "Y":
        print("Deleting Kubernetes Cluster " + clusterName + "\n")
        if gossipBasedCluster == "yes" or gossipBasedCluster == "Yes":
            fullClusterName = clusterName + ".k8s.local"
        else:
            fullClusterName = clusterName
        kopsProcess = subprocess.Popen(
        "{kops_path}  delete cluster --name "
        "{cluster_Name} --state={AWS_Bucket_Name} --yes".format(
            kops_path=kopsPath,
            cluster_Name=fullClusterName,
            AWS_Bucket_Name=S3BucketName), shell=True)
        try:
            kopsProcess.wait()
        except KeyboardInterrupt:
            print('Killing PID {0}...'.format(str(kopsProcess.pid)))
            kopsProcess.kill()
    else:
        return


#do any cleanup needed
def cleanup():
    print("cleanup\n")


# Show README
def show_readme():
    with open(kubered_path + "/readme.txt") as kuberedReadme:
        print(kuberedReadme.read())


# Exit Program
def quit_kr():
    cleanup()
    sys.exit(0)


# The Main Guts
def main():
    check_agreement()
    ascii_art()

    # Display Options
    try:
        while 1:
            print("\n\t(1) Change config values")
            print("\n\t(10) Name Cluster")
            print("\t(11) Deploy Cluster")
            print("\t(12) Check Cluster Status")
            print("\t(13) List Pods in Cluster")
            print("\t(14) Delete Cluster")
            print("\n\t(20) Bootstrap Cluster")
            print("\n\t(30) Deploy Cobalt Strike")
            print("\t(31) Deploy Merlin")
            print("\t(32) Deploy Silent Trinity")
            print("\t(33) Deploy Covenant")
            print("\n\t(40) Deploy Gophish")
            print("\n\t(98) Display README")
            print("\t(99) Quit")
            options = {"1": change_config,
                       "10": name_cluster,
                       "11": create_cluster,
                       "12": cluster_status,
                       "13": list_pods,
                       "14": delete_cluster,
                       "20": bootstrap_cluster,
                       "30": deploy_cobalt,
                       "31": deploy_merlin,
                       "32": deploy_silent,
                       "33": deploy_covenant,
                       "40": deploy_gophish,
                       "98": show_readme,
                       "99": quit_kr
                       }
            try:
                task = input("\nSelect a task: ")
                options[task]()
            except KeyError:
                pass
    except KeyboardInterrupt:
        quit_kr()

# Boilerplate
if __name__ == '__main__':
    main()
