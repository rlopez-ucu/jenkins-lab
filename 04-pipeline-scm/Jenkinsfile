pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Instalar dependencias') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff check .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
        }
    }
}
