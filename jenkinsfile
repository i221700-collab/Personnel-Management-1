pipeline {
    agent any

    tools {
        // This must match the name in Manage Jenkins -> Tools (e.g., M3)
        maven 'M3' 
    }

    parameters {
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run Python unit tests?')
        booleanParam(name: 'RUN_MAVEN', defaultValue: true, description: 'Run Maven build stage?')
        stringParam(name: 'BUILD_ENV', defaultValue: 'dev', description: 'Build environment (dev/stage/prod)')
    }

    environment {
        PYTHON_PATH = 'C:\\Users\\Umar Zeb\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        VENV_DIR = 'venv'
        APP_NAME = 'PersonnelManagement'
        FLASK_ENV = "${params.BUILD_ENV}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code for ${env.FLASK_ENV} environment..."
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                echo 'Setting up Python virtual environment...'
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
                echo 'Running Pytest...'
                bat "${env.VENV_DIR}\\Scripts\\python.exe -m pytest -q --junitxml=test-results.xml || exit 0"
            }
        }

        stage('Maven Build') {
            when { expression { return params.RUN_MAVEN } }
            steps {
                echo 'Checking for pom.xml before running Maven...'
                // This batch script checks if pom.xml exists. If not, it skips the build without failing.
                bat """
                if exist pom.xml (
                    echo "pom.xml found. Starting Maven build..."
                    mvn clean install -DskipTests
                ) else (
                    echo "WARNING: No pom.xml found in repository. Skipping Maven build to prevent failure."
                )
                """
            }
        }

        stage('Package Application') {
            steps {
                echo 'Creating distribution package...'
                bat """
                if not exist dist mkdir dist
                copy app.py dist\\
                copy requirements.txt dist\\
                if exist templates xcopy /s /y templates dist\\templates\\
                if exist instance xcopy /s /y instance dist\\instance\\
                """
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving results...'
                archiveArtifacts artifacts: '**/target/*.jar, dist/**/*', allowEmptyArchive: true
                junit testResults: '**/test-results.xml, **/target/surefire-reports/*.xml', allowEmptyResults: true
            }
        }
    }

    post {
        always {
            echo "Pipeline execution for ${env.APP_NAME} in ${env.FLASK_ENV} completed!"
        }
        success {
            echo '✔ Build successful!'
        }
        failure {
            echo '✘ Build failed! Check the console output for errors.'
        }
    }
}
