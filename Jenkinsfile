// Root Jenkinsfile for the multibranch demo. Runs the sample app in sample-app/.
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        APP_DIR = 'sample-app'
    }

    parameters {
        string(name: 'VERSION', defaultValue: '1.1.0', description: 'Version a desplegar')
        booleanParam(name: 'EJECUTAR_TESTS', defaultValue: true, description: 'Correr los tests')
    }

    stages {
        stage('Info') {
            steps {
                echo "Rama: ${env.BRANCH_NAME}"
                echo "PR: ${env.CHANGE_ID ?: 'no es un PR'}"
                sh 'git log -1 --oneline'
            }
        }

        stage('Instalar dependencias') {
            steps {
                dir(APP_DIR) {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --quiet -r requirements.txt
                    '''
                }
            }
        }

        stage('Lint') {
            steps {
                dir(APP_DIR) {
                    sh '''
                        . .venv/bin/activate
                        ruff check .
                    '''
                }
            }
        }

        stage('Test') {
            when {
                expression { params.EJECUTAR_TESTS }
            }
            steps {
                dir(APP_DIR) {
                    sh '''
                        . .venv/bin/activate
                        pytest --junitxml=reports/junit.xml
                    '''
                }
            }
        }

        stage('Build imagen') {
            steps {
                dir(APP_DIR) {
                    sh 'docker build --build-arg APP_VERSION=${VERSION} -t libreria-api:${VERSION} .'
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch pattern: 'release/.*', comparator: 'REGEXP'
                }
            }
            steps {
                echo "Desplegando ${params.VERSION} desde ${env.BRANCH_NAME}"
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: "${APP_DIR}/reports/junit.xml"
        }
    }
}
