node {
    stage('Checkout SCM'){
        checkout scm
    }
    stage('Build Docker image'){
        def merossImage = docker.build("meross:${env.BUILD_ID}")
    }
    stage('Run Docker image'){
        sh 'docker run -d --rm meross:${env.BUILD_ID}'
    }
}
