// Jenkins Pipeline defined using the declarative syntax
pipeline {
    // Agent specifies where the pipeline will execute. 
    // 'any' uses any available agent (node/executor).
    agent any 

    // Define environment variables, especially for DockerHub credentials
    environment {
        // --- ⚠️ REPLACE THESE PLACEHOLDERS ⚠️ ---
        // Your DockerHub username
        DOCKERHUB_USERNAME = 'vaishak2005'
        // Your roll number (used for the image tag)
        ROLL_NUMBER = 'imt2023085'
        // ID of the Jenkins 'Username with password' credential for DockerHub login
        DOCKER_CREDS_ID = 'dockerhub-creds	' 
        
        // Assembled image name
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${ROLL_NUMBER}-cli-todo"
    }

    // Stages define a conceptual division of the pipeline
    stages {
        // 1. Checkout Stage: Pulls the code from GitHub
        stage('Pull Code (Checkout)') {
            steps {
                // You can also add the 'credentialsId' here if you want to be explicit,
                // but it often defaults correctly from the job configuration.
                git branch: 'main', url: 'https://github.com/vaishak-iiitb/todo-cli-app'
            }
        }

        // 2. Build Stage: Creates and configures the Python environment
        stage('Create Virtual Environment & Install Deps') {
            steps {
                echo 'Creating Python Virtual Environment...'
                sh '/usr/bin/python3 -m venv .venv'
                
                echo 'Installing Pytest and other dependencies from requirements.txt...'
                // This step assumes 'requirements.txt' is present and contains 'pytest'
                sh '.venv/bin/pip install --upgrade pip'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        // 3. Test Stage: Runs the automated tests using Pytest
        stage('Run Tests (Pytest)') {
            steps {
                script {
                    echo 'Running Pytest tests...'
                    // Execute pytest using the virtual environment's executable
                    // Use returnStatus: true to check the exit code for pass/fail
                    def testResult = sh(returnStatus: true, script: '.venv/bin/pytest -v')
                    if (testResult != 0) {
                        error 'Pytest failed. Aborting pipeline.'
                    }
                }
            }
        }

        // 4. Docker Build Stage: Creates the Docker Image
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:latest"
                // The '.' assumes the Dockerfile is in the root of the workspace
                sh "docker build -t ${IMAGE_NAME}:latest ."
                
                // Check the image was created (using 'docker images')
                sh "docker images | grep ${IMAGE_NAME}"
            }
        }
        
        // 5. Docker Push Stage: Pushes the image to DockerHub
        stage('Push Docker Image to Hub') {
            steps {
                script {
                    // Login to DockerHub using the stored Jenkins credential
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        echo 'Logging into DockerHub...'
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                        
                        echo "Pushing Docker image ${IMAGE_NAME}:latest..."
                        sh "docker push ${IMAGE_NAME}:latest"
                        
                        // Logout is optional but good practice
                        sh "docker logout"
                    }
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
        // Optional: Clean up workspace (removes .venv, code, etc.)
        cleanup {
            deleteDir() 
        }
    }
}
