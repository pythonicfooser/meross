node {
    stage('Checkout SCM'){
        checkout scm
    }
    stage('Build Docker image'){
        def merossImage = docker.build("meross:${env.BRANCH_NAME}")
    }
    stage('Run Docker image'){
        sh 'docker run -d --rm meross:$BRANCH_NAME'
    }
}
