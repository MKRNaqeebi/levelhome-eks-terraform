curl --location --request POST "http://localhost:8000/signin" --header 'Content-Type: application/json' -d '{"user_email":"montyw@example.com", "user_password":"123456"}'

=====

curl --location --request GET "http://127.0.0.1:8000/products" --header 'Content-Type: application/json' --header 'Access-Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb250eXdAZXhhbXBsZS5jb20iLCJleHAiOjE2ODg3MTM3MjF9.Gx4OWNj_MpLXzA5uP7sXtiaaVIEjk4Rm27_TpByn0Ek'


# tag docker image
docker tag levelhome 417722183802.dkr.ecr.us-west-2.amazonaws.com/levelhome

# push docker image
docker push 417722183802.dkr.ecr.us-west-2.amazonaws.com/levelhome

curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.23.6/bin/linux/amd64/kubectl

aws eks update-kubeconfig --region us-west-2 --name learn-terraform-eks

terraform init
terraform validate
terraform plan
terraform apply

terraform destroy

# forward port
kubectl port-forward service/levelhome 8000:8000


kubectl apply -f deployment.yaml
helm repo add eks https://aws.github.io/eks-charts

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --set autoDiscoverAwsRegion=true \
  --set autoDiscoverAwsVpcID=true \
  --set clusterName=learnk8s

kubectl get pods -l "app.kubernetes.io/name=aws-load-balancer-controller"



kubectl annotate serviceaccount -n kube-system aws-load-balancer-controller eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/aws-load-balancer-controller


kubectl run -i --tty --rm debug --image=busybox --restart=Never -- nc -vz levelhome1.cmiih24acwxl.us-west-2.rds.amazonaws.com 5432
