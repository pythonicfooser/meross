pipeline {
    agent any
    stages {
        stage('Checkout SCM'){
            steps {
                checkout scm
            }
        }
        stage('Build Docker image'){
            steps {
                def merossImage = docker.build("meross:${env.BUILD_ID}")
            }
        }
        stage('Run Docker image'){
            steps {
                sh 'docker run -d --rm meross:${env.BUILD_ID}'
            }
        }
    }
}
