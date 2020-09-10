node {
    checkout scm

    def merossImage = docker.build("meross:${env.BUILD_ID}")

    merossImage.withRun('-d -p 9999:8080')
}
