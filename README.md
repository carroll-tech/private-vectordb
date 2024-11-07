# 🚧 Private VectorDB - Work in Progress 🚧

> **⚠️ Warning: This project is currently under development and is not functional yet.**

Please check back later for updates! 🛠️

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
- A Kubernetes cluster
- Operator Lifecycle Manager installed on cluster. Installation [instructions here](https://github.com/operator-framework/operator-lifecycle-manager/releases)
- Knative Operator installed on cluster. Installation [instructions here](https://artifacthub.io/packages/olm/community-operators/knative-operator?modal=install)
- Rook Ceph Operator installed on cluster. Installation [instructions here](https://artifacthub.io/packages/olm/community-operators/rook-ceph?modal=install) *NOTE*: you should put the operator in the `operators` namespace, not a new `rook-ceph` namespace. This keeps consistency with other installed operators.

Prerequisites can be installed and configured by running the included script:
```bash
chmod +x install-prerequisites.sh
./install-prerequisites.sh
```

### Steps


## Thank You
Thank you to LanceDB for their tutorial, [Serverless LanceDB](https://lancedb.com/gallery/serverless-lancedb-with-s3-and-lambda), which served as a useful guide during development.
