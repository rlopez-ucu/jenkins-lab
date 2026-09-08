// Uso en un Jenkinsfile:
//   @Library('ucu-lib') _
//   pipelinePython(imagen: 'usuario/app')
def call(Map config = [:]) {
    pipeline {
        agent any

        options {
            timestamps()
        }

        stages {
            stage('Instalar') {
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
                    sh '. .venv/bin/activate && ruff check .'
                }
            }
            stage('Test') {
                steps {
                    sh '. .venv/bin/activate && pytest --junitxml=reports/junit.xml'
                }
            }
            stage('Build imagen') {
                when { expression { config.imagen } }
                steps {
                    sh "docker build -t ${config.imagen}:${BUILD_NUMBER} ."
                }
            }
        }

        post {
            always {
                junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            }
            success {
                notificar('Build OK', 3066993)
            }
            failure {
                notificar('Build FALLO', 15158332)
            }
        }
    }
}
