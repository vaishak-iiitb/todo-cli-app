// Jenkins Pipeline defined using the declarative syntax
pipeline {
    agent any 

    environment {
        // --- Placeholders defined ---
        DOCKERHUB_USERNAME = 'vaishak2005'
        ROLL_NUMBER = 'imt2023085'
        // Credential ID (Ensure this matches the ID in Jenkins Credentials)
        DOCKER_CREDS_ID = 'dockerhub-creds' 
        
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${ROLL_NUMBER}-cli-todo"
        // Define the full path for the Docker executable once
        DOCKER_CLI = '/usr/local/bin/docker'
    }

    stages {
        // 1. Checkout Stage: Pulls the code from GitHub
        stage('Pull Code (Checkout)') {
            steps {
                git branch: 'main', url: 'https://github.com/vaishak-iiitb/todo-cli-app'
            }
        }

        // 2. Build Stage: Creates and configures the Python environment
        stage('Create Virtual Environment & Install Deps') {
            steps {
                echo 'Creating Python Virtual Environment...'
                sh '/usr/bin/python3 -m venv .venv'
                
                echo 'Installing Pytest and other dependencies from requirements.txt...'
                sh '.venv/bin/pip install --upgrade pip'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        // 3. Test Stage: Runs the automated tests using Pytest
        stage('Run Tests (Pytest)') {
            steps {
                script {
                    echo 'Running Pytest tests...'
                    withEnv(['PYTHONPATH=src/main/python']) {
                        def testResult = sh(returnStatus: true, script: '.venv/bin/pytest -v')
                        if (testResult != 0) {
                            error 'Pytest failed. Aborting pipeline.'
                        }
                    }
                }
            }
        }

        // 4. Docker Build Stage: Logs in to bypass rate limits and builds the image.
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:latest"
                
                script {
                    def docker_config_dir = "docker_temp_config_build" // Unique temp config folder

                    // Setup: Create minimal config to disable credential helper
                    sh """
                        mkdir -p ${docker_config_dir}
                        echo '{"credHelpers":{}}' > ${docker_config_dir}/config.json
                    """
                    
                    // Login, Build, and Logout using the temporary config
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        withEnv([
                            "DOCKER_CONFIG=${docker_config_dir}",
                            "DOCKER_BUILDKIT=0" // Disables BuildKit which often causes credential errors
                        ]) {
                            echo 'Logging into DockerHub to bypass pull rate limits...'
                            sh "echo \$DOCKER_PASSWORD | ${DOCKER_CLI} login -u \$DOCKER_USERNAME --password-stdin"
                            
                            echo 'Starting Docker image build...'
                            sh "${DOCKER_CLI} build -t ${IMAGE_NAME}:latest ."
                            
                            // Logout immediately
                            sh "${DOCKER_CLI} logout"
                        }
                    }
                    
                    // Cleanup: Remove the temporary config folder
                    sh "rm -rf ${docker_config_dir}"
                }
                
                // Check the image was created
                sh "${DOCKER_CLI} images | grep ${IMAGE_NAME}"
            }
        }
        
        // 5. Docker Push Stage: Re-logs in to push the built image.
        stage('Push Docker Image to Hub') {
            steps {
                script {
                    def docker_config_dir = "docker_temp_config_push" // Unique temp config folder

                    // Setup: Create minimal config to disable credential helper
                    sh """
                        mkdir -p ${docker_config_dir}
                        echo '{"credHelpers":{}}' > ${docker_config_dir}/config.json
                    """

                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        withEnv(["DOCKER_CONFIG=${docker_config_dir}"]) {
                            echo 'Re-logging into DockerHub for push...'
                            sh "echo \$DOCKER_PASSWORD | ${DOCKER_CLI} login -u \$DOCKER_USERNAME --password-stdin"
                            
                            echo "Pushing Docker image ${IMAGE_NAME}:latest..."
                            sh "${DOCKER_CLI} push ${IMAGE_NAME}:latest"
                            
                            sh "${DOCKER_CLI} logout"
                        }
                    }
                    // Cleanup: Remove the temporary config folder
                    sh "rm -rf ${docker_config_dir}"
                }
            }
        }
    }
    
    // Post-build actions
    post {
        always {
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Pipeline succeeded! Docker image pushed to DockerHub.'
        }
        failure {
            echo 'Pipeline failed! Check logs for errors.'
        }
        cleanup {
            deleteDir() 
        }
    }
}
