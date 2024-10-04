## Operator Lifecycle Manager
curl -L https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.28.0/install.sh -o install.sh
chmod +x install.sh
./install.sh v0.28.0
rm install.sh

## Knative Operator
cat <<EOF | kubectl apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: knative
  namespace: operators
spec:
  channel: stable
  name: knative-operator
  source: operatorhubio-catalog
  sourceNamespace: olm
EOF

## Rook Ceph Operator
cat <<EOF | kubectl apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: rook-ceph
  namespace: operators
spec:
  channel: beta
  name: rook-ceph
  source: operatorhubio-catalog
  sourceNamespace: olm
EOF