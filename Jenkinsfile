pipeline {
    agent any

    tools {
        // IMPORTANT: Ensure "M3" matches the Name in Manage Jenkins -> Tools
        maven 'M3' 
    }

    parameters {
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run Python unit tests?')
        booleanParam(name: 'RUN_MAVEN', defaultValue: true, description: 'Run Maven build stage?')
        // Changed "stringParam" to "string" to fix your compilation error
        string(name: 'BUILD_ENV', defaultValue: 'dev', description: 'Build environment (dev/stage/prod)')
    }

    environment {
        PYTHON_PATH = 'C:\\Users\\Umar Zeb\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        VENV_DIR = 'venv'
        FLASK_ENV = "${params.BUILD_ENV}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat """
                "${env.PYTHON_PATH}" -m venv ${env.VENV_DIR}
                ${env.VENV_DIR}\\Scripts\\python.exe -m pip install --upgrade pip
                ${env.VENV_DIR}\\Scripts\\python.exe -m pip install -r requirements.txt
                """
            }
        }

        stage('Python Tests') {
            when { expression { return params.RUN_TESTS } }
            steps {
                bat "${env.VENV_DIR}\\Scripts\\python.exe -m pytest -q --junitxml=test-results.xml || exit 0"
            }
        }

        stage('Maven Build') {
            when { expression { return params.RUN_MAVEN } }
            steps {
                bat """
                if exist pom.xml (
                    mvn clean install -DskipTests
                ) else (
                    echo "No pom.xml found, skipping..."
                )
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('SonarQube-server') {
                        bat "\"${scannerHome}\\bin\\sonar-scanner\""
                    }
                }
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'dist/**/*', allowEmptyArchive: true
                junit testResults: '**/test-results.xml', allowEmptyResults: true
            }
        }
    }

    post {
        success { echo '✔ Build successful!' }
        failure { echo '✘ Build failed!' }
    }
}
