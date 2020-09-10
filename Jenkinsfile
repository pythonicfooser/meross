node {
    stage('Checkout SCM'){
        checkout scm
    }
    stage('Build Docker image'){
        def merossImage = docker.build("meross:${env.BUILD_ID}")
    }
    stage('Run Docker image'){
        sh 'Test webhook'
        sh 'docker run -d --rm meross:$BUILD_ID'
    }
}
