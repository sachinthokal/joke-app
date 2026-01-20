pipeline {
    agent any

    environment {
        IMAGE_NAME = "jenkins-joke-app:1.0"
        CONTAINER_NAME = "joke-app"
        NGINX_CONF_SRC = "nginx/flaskapp.conf"
        NGINX_CONF_DST = "/etc/nginx/sites-available/flaskapp"
    }

    stages {

        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  -p 127.0.0.1:5000:5000 \
                  ${IMAGE_NAME}
                """
            }
        }

        stage('Apply Nginx Config') {
            steps {
                sh """
                sudo cp ${NGINX_CONF_SRC} ${NGINX_CONF_DST}
                sudo ln -sf ${NGINX_CONF_DST} /etc/nginx/sites-enabled/flaskapp
                """
            }
        }

        stage('Validate & Reload Nginx') {
            steps {
                sh """
                sudo rm -f /etc/nginx/sites-enabled/default || true
                sudo rm -f /etc/nginx/sites-available/flaskapp || true
                sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
                sudo nginx -t
                sudo systemctl reload nginx
                """
            }
        }
    }

    post {
        success {
            echo '✅ Docker + Nginx Pipeline SUCCESS 🎉'
        }
        failure {
            echo '❌ Docker + Nginx Pipeline FAILED'
        }
    }
}
