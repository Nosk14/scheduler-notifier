node {
    def image_name = "scheduler-notifier"
    def image = null
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = docker.build("${image_name}:${env.BUILD_ID}")
    }

    stage('Deploy'){
        try{
            sh "docker stop ${image_name} && docker rm ${image_name}"
        }catch(Exception e){
            echo e.getMessage()
        }
        withCredentials([string(credentialsId: 'engendro-telegram-token', variable: 'token')]) {
            withCredentials([string(credentialsId: 'nosk-telegram-chat-id', variable: 'telegram_channel')]) {
                def runArgs = '\
-e "TELEGRAM_TOKEN=$token" \
-e "TELEGRAM_CHAT_ID=$telegram_channel" \
--restart unless-stopped \
--name ' + image_name

                def container = image.run(runArgs)
            }
        }
    }
}