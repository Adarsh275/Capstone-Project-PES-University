# Horizontal Pod Autoscaler (HPA) in Kubernetes

In the dynamic world of cloud-native applications, Horizontal Pod Autoscaler (HPA) is a crucial feature that automatically scales the number of pods based on resource utilization metrics. This dynamic scaling ensures optimal resource utilization, application performance, and simplified resource management.

## A Step-by-Step Guide to Setup and Configure HPA Autoscalar

#### **STEP 1:** Install Metrix Server

The first step is to install the Metrics Server, which is a component of Kubernetes that collects resource usage metrics from pods. This data is used by the Horizontal Pod Autoscaler (HPA) to determine whether to scale up or down the number of pods in a deployment.

> To check if the Metrics Server is already installed, you can run the following commands:
````
kubectl get nodes
kubectl top node   // Metrics API not available
kubectl top pods  //  Metrics API not available
````
If the Metrics API is not available, then you need to install the Metrics Server. To do this, go to the path where manifest files are present and apply the following manifest files:
``````
kubectl apply -f .    // all files are applyed
kubectl top nodes    // this get all the Metrics
``````
This will install the Metrics Server and all of its dependencies. Once the Metrics Server is installed, you should be able to see resource usage metrics using the `kubectl top` command.

#### **STEP 2:** Deploy sample app

The next step is to deploy a sample application that will generate CPU load. You can do this by applying the following manifest file:
``````
kubectl apply -f 01_Deployment.yml
``````
This will create a deployment with three replicas of the sample application. You can check the status of the deployment using the following command:
``````
kubectl get deploy
``````

#### **STEP 3:** Create Service

A service is a Kubernetes object that exposes a set of pods as a network service. You need to create a service for your sample application so that it can be accessed from outside the cluster. You can do this by applying the following manifest file:
``````
kubectl apply -f 02_Service.yml
``````
This will create a service for your sample application. You can check the status of the service using the following command:
``````
kubectl get svc
``````

#### **STEP 4:** Deploy HPA

The Horizontal Pod Autoscaler (HPA) is a Kubernetes object that automatically scales the number of pods in a deployment based on resource usage. You need to create an HPA for your sample application so that it will scale up when there is high CPU load. You can do this by applying the following manifest file:
``````
kubectl apply -f 03_HPA.yml
``````
This will create an HPA for your sample application. You can check the status of the HPA using the following command:
``````
kubectl get hpa
``````

#### **STEP 5:** Increase Load

To simulate high CPU load, you can run a load generator in a separate terminal window. The following command will run a load generator that will make continuous requests to your sample application:
``````
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://hpa-demo-deployment; done"
kubectl delete pod load-generator   // To terminate the load-generator Pod
``````
To stop load generation, we may either execute the above-mentioned command in a terminal or hit Ctrl+C inside the current shell session.

#### **STEP 6:** Moniter HPA Events

You can monitor the HPA events to see how the HPA is scaling the number of pods in your deployment. You can do this using the following command:
``````
kubectl get events
kubectl get HPA
``````
The HPA will automatically scale up the number of pods in your deployment when the CPU load is high. The HPA will also scale down the number of pods when the CPU load is low.

>Use the following command to see the current status of pod creation and deletion:
``````
kubectl get pods -w
``````
It will continuously print the list of pods, updating the output as the pods change state.

### References:

1. Nandan Adhikari (April 19, 2021) Horizontal Pod Autoscaler in Kubernetes https://around25.com/blog/horizontal-pod-autoscaler-in-kubernetes/

2. Ashok (April 11, 2023) Horizontal POD Autoscaler setup in Kubernetes https://www.youtube.com/watch?v=c-tsJrcB50I