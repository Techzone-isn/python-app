pipeline {
    agent any
    
    environment {
        // Define your Docker Hub credentials and Kubernetes configuration here
        KUBECONFIG = './python-app'
        docker_user = 'techzoneisn023'
        image_tag = 'latest'
        image_name = 'python-img'
    }
    
    stages {
        stage('Git Check out') {
            steps {
                git branch: 'main', url: 'https://github.com/techzone-isn/python-app.git'
            }
        }
        stage('Docker Build') {
            steps {
                sh "docker build -t ${docker_user}/${image_name}:${image_tag} ."
            }
        }
        stage('Docker Push to Docker Hub') {
            steps {
                script{
                    withDockerRegistry(credentialsId: 'docker-cred') {
                        sh "docker push ${docker_user}/${image_name}:${image_tag}"
                    }
                }
            }
        }
        stage('Update Deployment File Image Tag') {
            steps {
                sh "sed -i 's/python-job:v1/${image_name}:${image_tag}/' ./Deployment.yml"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f Deployment.yml"
            }
        }
    }
}
