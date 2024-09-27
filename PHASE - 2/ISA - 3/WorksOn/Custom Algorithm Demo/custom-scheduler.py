from prometheus_api_client import PrometheusConnect
from kubernetes import client, config
import subprocess, uuid, time

 
print("custom scheduler running")
min_pods = 1
max_pods = 10

while(True):
    # Fetch the current CPU usage
    # Define the command to fetch CPU usage for all pods in the default namespace for application
    command = "kubectl top pods -l app=my-nginx --containers"
    
    # Run the command and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for any errors
    if process.returncode != 0:
        print("Error:", stderr.decode('utf-8'))
    else:
        # Process the output to access CPU values
        output_lines = stdout.decode('utf-8').split('\n')
        # The output contains columns for NAME, CPU(cores), and MEMORY(bytes)
        # Extract the CPU values from the output
        for line in output_lines[1:]:  # Skip the header line
            if line:
                #print(line)
                pod, pod_name, cpu_usage_m, memory_usage_b= line.split()
                
                #print(f"Pod: {pod_name}, CPU Usage: {cpu_usage}")
                cpu_usage_m = int(cpu_usage_m.rstrip("m"))
                break
                #current_usage_value = (cpu_usage_m / total_cpu_requests)*100
                #print(current_usage_value)
                
    print("fetched current cpu usage")
    print(cpu_usage_m)


    # Rest of your custom scheduler logic
    # Load the Kubernetes configuration from your kubeconfig file
    config.load_kube_config()

    # Create an instance of the Kubernetes API client
    api = client.CoreV1Api()

    # Query all the pods in the "default" namespace (change the namespace as needed)
    
    target_cpu_value = 40  

    scaling_factor = (cpu_usage_m - target_cpu_value) / 100.0
    if cpu_usage_m > target_cpu_value:
        # Increase pods proportionally to the difference between current and target CPU
            
        predicted_pods = round(min_pods + (max_pods - min_pods) * scaling_factor)
        predicted_pods = max(min_pods, min(predicted_pods,max_pods))

        namespace = "default"
        deployment_name = "my-nginx"
        label_selector = f"app={deployment_name}"
        pods = api.list_namespaced_pod(namespace, label_selector=label_selector)


        # Get the total number of pods in the list
        total_pods = len(pods.items)
        x = predicted_pods - total_pods
        if x > 0:
            for i in range(x):
                print("creating new pods")
                api = client.CoreV1Api()

                # Define the namespace where you want to create the pod
                namespace = "default"  # Change this to your desired namespace
                # Generate a UUID for unique pod names
                unique_id = str(uuid.uuid4().hex)[:6]


                # Create the pod object
                pod = client.V1Pod(
            metadata=client.V1ObjectMeta(
                name="my-pod-{}".format(unique_id),
                labels={"app": "my-nginx"}  # Add the label here
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-nginx",
                        image="veenagarag/my-nginx-sample",
                    )
                ]
            ),
        )
            
                try:
                    # Create the pod in the specified namespace
                    api.create_namespaced_pod(namespace, pod)

                    print(f"Pod {pod.metadata.name} created successfully.")
                except Exception as e:
                    print(f"Error creating pod: {e}")

        else:
            
            y = total_pods - predicted_pods
            namespace = "default"
            deployment_name = "my-nginx"
            label_selector = f"app={deployment_name}"
            else_podn = api.list_namespaced_pod(namespace, label_selector=label_selector)


            # Get the total number of pods in the list
            total_podsn = len(else_podn.items)
            print("total pods in else condition",total_podsn)

            if total_podsn > min_pods:
                
                command = "kubectl top pods -l app=my-nginx --containers"
                pods_Arrn = []
                # Run the command and capture the output
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                # Check for any errors
                if process.returncode != 0:
                    print("Error:", stderr.decode('utf-8'))
                else:
                    # Process the output to access CPU values
                    output_lines = stdout.decode('utf-8').split('\n')
                    # The output contains columns for NAME, CPU(cores), and MEMORY(bytes)
                    # Extract the CPU values from the output
                    for line in output_lines[1:]:  # Skip the header line
                        if line:
                            #print(line)
                            pod, pod_name, cpu_usage_m, memory_usage_b= line.split()
                            cpu_usage_m = int(cpu_usage_m.rstrip("m"))
                            pods_Arrn.append(pod)
                    print(pods_Arrn)  


                if predicted_pods < total_podsn and total_podsn > min_pods:
                    print("figuring out what pods to delete")
                    # Find the indices of elements that start with "my-pod-"
                    indices_to_deleten = [i for i, element in enumerate(pods_Arrn) if element.startswith("my-pod-")]
                    n = total_podsn - predicted_pods
                    print("n is",n)
                    # Extract the elements to be deleted
                    elements_to_deleten = [pods_Arrn[i] for i in indices_to_deleten[:n]]

                    
                    print(elements_to_deleten)
                    # Print the elements that are removed from the array
                    #print(elements_to_delete)
                    for i in elements_to_deleten:
                        
                        try:
                            # Delete the pod
                            api.delete_namespaced_pod(i, namespace)

                            print(f"Pod {i} deleted successfully.")
                        except Exception as e:
                            print(f"Error deleting pod: {e}")

                        

    else:
            # Decrease pods proportionally to the difference between target and current CPU
        namespace = "default"
        deployment_name = "my-nginx"
        label_selector = f"app={deployment_name}"
        else_pod = api.list_namespaced_pod(namespace, label_selector=label_selector)


        # Get the total number of pods in the list
        total_pods = len(else_pod.items)
        print("total pods in else condition",total_pods)

        if total_pods > min_pods:
            
            command = "kubectl top pods -l app=my-nginx --containers"
            pods_Arr = []
            # Run the command and capture the output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Check for any errors
            if process.returncode != 0:
                print("Error:", stderr.decode('utf-8'))
            else:
                # Process the output to access CPU values
                output_lines = stdout.decode('utf-8').split('\n')
                # The output contains columns for NAME, CPU(cores), and MEMORY(bytes)
                # Extract the CPU values from the output
                for line in output_lines[1:]:  # Skip the header line
                    if line:
                        #print(line)
                        pod, pod_name, cpu_usage_m, memory_usage_b= line.split()
                        cpu_usage_m = int(cpu_usage_m.rstrip("m"))
                        pods_Arr.append(pod)
                print(pods_Arr)  
                        
            scaling_factor = (cpu_usage_m - target_cpu_value) / 100.0
            predicted_pods = round(max_pods - (max_pods - min_pods) * scaling_factor)
            predicted_pods = min(min_pods, min(predicted_pods,max_pods))
            print("Deleting pods with low CPU usage")
            # Create a Kubernetes API instance
            api = client.CoreV1Api()

            # Define the namespace where the pod is located
            namespace = "default"  # Change this to your desired namespace
            # Load the Kubernetes configuration from your kubeconfig file
            config.load_kube_config()

            # Create an instance of the Kubernetes API client
            api = client.CoreV1Api()

            

            # Get the total number of pods in the list
            
            if predicted_pods < total_pods and total_pods > min_pods:
                print("figuring out what pods to delete")
                # Find the indices of elements that start with "my-pod-"
                indices_to_delete = [i for i, element in enumerate(pods_Arr) if element.startswith("my-pod-")]
                n = total_pods - predicted_pods
                print("n is",n)
                # Extract the elements to be deleted
                elements_to_delete = [pods_Arr[i] for i in indices_to_delete[:n]]

                
                print(elements_to_delete)
                # Print the elements that are removed from the array
                #print(elements_to_delete)
                for i in elements_to_delete:
                    
                    try:
                        # Delete the pod
                        api.delete_namespaced_pod(i, namespace)

                        print(f"Pod {i} deleted successfully.")
                    except Exception as e:
                        print(f"Error deleting pod: {e}")



    time.sleep(10)



    




    
    

        