pipeline {
    agent any

    environment {
        IMAGE_NAME = "jenkins-joke-app:1.0"
        CONTAINER_NAME = "joke-app"
        NGINX_CONF_SRC = "nginx/flaskapp.conf"
        NGINX_CONF_DST = "/etc/nginx/sites-available/flaskapp"
        NGINX_ENABLED = "/etc/nginx/sites-enabled/flaskapp"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build Image') {
            steps { sh 'docker build -t ${IMAGE_NAME} .' }
        }

        stage('Restart Container') {
            steps {
                sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker run -d --name ${CONTAINER_NAME} -p 127.0.0.1:5000:5000 ${IMAGE_NAME}
                '''
            }
        }

        stage('Apply Nginx Config') {
            steps {
                sh '''
                sudo rm -f /etc/nginx/sites-enabled/default
                sudo rm -f ${NGINX_ENABLED}
                sudo cp ${NGINX_CONF_SRC} ${NGINX_CONF_DST}
                sudo ln -s ${NGINX_CONF_DST} ${NGINX_ENABLED}
                sudo nginx -t
                sudo systemctl reload nginx
                '''
            }
        }
    }

    post {
        success { echo '✅ DEPLOY SUCCESS 🎉' }
        failure { echo '❌ DEPLOY FAILED' }
    }
}
