# Core python library


## Description

The libraries contained in the core package are responsible for creating a cluster of VMs and installing all the required packages and configs to have a complete lambda instance. A description of the libraries follows:

### provisioner

The library is responsible for creating/deleting a VM cluster, using the Kamaki python API. It reads the authentication info from the .kamakirc, and accepts the cluster specs as arguments.

### ansible_manager

The library is responsible for managing the ansible, that will run on the cluster. Its tasks are:
* It reads a python dictionary object, containing the necessary info about the cluster and its nodes
* It creates an ansible inventory object, using the dictionary
* It creates the necessary group and host vars, required for ansible to run on all the nodes and configure them properly
* It sets some ansible constants, required eg for SSH tunnelling through the master node
* It runs ansible playbooks using the previously mentioned inventory and constants

### lambda_instance_manager

The library is responsible for creating/deleting the entire lambda instance.
Run script as `lambda_instance_manager.py --action=create` for creating a lambda cluster.
Run script as `lambda_instance_manager.py --action=delete --cluster_id=<id>` for deleting a lambda cluster.
According to the action selected, certain arguments must be modified.

If action is CREATE
* It sets the provisioner arguments (cluster specs), then calls the provisioner to create the cluster.
* After that, it gets the output dictionary of the provisioner and adds some more values to it, which are obtained using the provisioner, after the cluster creation.
* It calls the ansible_manager, to create the inventory, using the dictionary as input.
* Finally, it uses the created manager object (containing the inventory and constants), to run the required playbooks in the correct order, to create the lambda instance.

If action is DELETE
* It reads the cluster id from the arguments.
* Creates a query to read the cluster information from the database with this id.
* It call the delete_lambda_cluster method of the provisioner with the information it retrieved from the database.

## Prerequisites

* kamaki 0.13.4 or later
* ansible 1.9.2 or later
* crypto 1.4.1 or later


## Installation

- Create a .kamakirc configuration in your home folder and add all the required configurations.
 Here is an example configuration
```
[global]
default_cloud = lambda
; ca_certs = /path/to/certs

[cloud "lambda"]
url = https://accounts.okeanos.grnet.gr/identity/v2.0
token = your-okeanos-token
```
Note that you may retrieve your ~okeanos API token, after logging into the service, by visiting [this page][api_link].

1. Install required packages. Within the `core` directory execute

       $ sudo pip install -r requirements.txt

1. Install fokia library locally using 

       $ sudo python setup.py install


## Usage


To create a lambda instance, one must execute:
```
python lambda_instance_manager.py --project-name {{~okeanos project name}}
```

from within the `core/fokia` directory. To change the default settings (one master and one slave VM) use the following command line flags:

```
  --master-name MASTER_NAME    Name of Flink master VM [default: lambda-master]
  --slaves SLAVES              Number of Flink slaves [default: 1]
  --vcpus-master VCPUS_MASTER  Number of CPUs on Flink master [default: 4]
  --vcpus-slave VCPUS_SLAVE    Number of CPUs on Flink slave(s) [default: 4]
  --ram-master RAM_MASTER      Size of RAM on Flink master (in MB) [default: 4096MB]
  --ram-slave RAM_SLAVE        Size of RAM on Flink slave(s) (in MB) [default: 4096MB]
  --disk-master DISK_MASTER    Size of disk on Flink master (in GB) [default: 40GB]
  --disk-slave DISK_SLAVE      Size of disk on Flink slave(s) (in GB) [default: 40GB]
  --project-name               ~okeanos Project [example: project.grnet.gr]
  --auth-token                 ~okeanos auth token
```


## Testing

To test the library we use `tox`. In order to run the tests:

- Make sure you have tox installed `pip install tox`
- Run `tox`

This will automatically create the testing environments required and run the tests

[api_link]: https://accounts.okeanos.grnet.gr/ui/api_access
