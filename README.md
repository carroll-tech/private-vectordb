# Private VectorDB

## Description
This project is targeted for those who want to completely self-host a vector database on a kubernetes cluster, either on a cloud hosted provider, on your own kubernetes cluster, or locally on your machine. The only requirement is a kubernetes cluster. All data is stored on the cluster, and no traffic leaves the cluster during vector retrival. This is ideal for scenarios in which data is considered sensitive and thus has access restrictions.

## Features
- Entirely standalone vector service
- Easy deployment through a helm chart
- Decoupled compute and storage for efficient scaling

## Installation
Installation can be performed on any kubernetes cluster, whether it is local, a cloud offering (AKS, GKS, EKS), or any other. 
An internet connection will be required to download the images from GitHub Container Registry, but those wishing to do airgapped installs can move images onto their clusters in whatever process they currently have.
The project has been tested on both x86 and ARM machines.

### Prerequisites
1. A working kubernetes cluster. If you are unfamiliar with kubernetes or helm, you should start by trying to run a cluster locally using [MicroK8s](https://microk8s.io).
2. Operator Lifecycle Manager installed on cluster. Installation [instructions here](https://sdk.operatorframework.io/docs/cli/operator-sdk_olm_install/)
3. Knative Operator installed on cluster. Installation [instructions here](https://artifacthub.io/packages/olm/community-operators/knative-operator?modal=install)

### Steps


## Thank You
Thank you to Restack for their tutorial, [Lancedb Lambda On Aws](https://www.restack.io/p/lancedb-answer-lambda-aws-cat-ai), which served as a useful guide during development.
