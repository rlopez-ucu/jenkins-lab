// Uso en un Jenkinsfile: notificar('Build OK', 3066993)
def call(String titulo, int color) {
    node {
        withCredentials([string(credentialsId: 'discord-webhook', variable: 'WEBHOOK')]) {
            sh """
                curl -s -H 'Content-Type: application/json' -d @- "\$WEBHOOK" <<'JSON'
                {
                  "embeds": [{
                    "title": "${titulo}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    "description": "Rama: ${env.BRANCH_NAME ?: '-'}\\nDuracion: ${currentBuild.durationString}",
                    "url": "${env.BUILD_URL}",
                    "color": ${color}
                  }]
                }
JSON
            """
        }
    }
}
