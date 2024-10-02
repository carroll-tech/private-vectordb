# Private VectorDB

## Description
This project is targeted for those who want to completely self-host a vector database, either on a cloud hosted provider, on your own kubernetes cluster, or locally on your machine. The only requirement is a kubernetes cluster. All data is stored on the cluster, and no traffic leaves the cluster during vector retrival. This is ideal for scenarios in which data is considered sensitive and thus has access restrictions.

## Features
- Entirely standalone vector service
- Easy deployment through a helm chart

## Installation
Installation can be performed one of three ways, with instructions given for each. If you are unfamiliar with kubernetes or helm, you should start by trying to run the service locally.

### Local

### Cloud Provider

### BYO Cluster

## Thank You
Thank you to Restack for their tutorial, [Lancedb Lambda On Aws](https://www.restack.io/p/lancedb-answer-lambda-aws-cat-ai), which served as a useful guide during development.
