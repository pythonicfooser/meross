node {
    stage('Checkout SCM'){
        checkout scm
        BRANCH_NAME=env.BRANCH_NAME
    }
    stage('Build Docker image'){
        def merossImage = docker.build("meross:${BRANCH_NAME}")
    }
    stage('Run Docker image'){
        sh 'echo "fast test"'
        sh 'docker run -d --rm meross:$BRANCH_NAME'
    }
}
