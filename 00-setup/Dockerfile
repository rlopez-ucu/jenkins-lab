# Jenkins LTS + Docker CLI + Python. Built once by each student in the prework.
FROM jenkins/jenkins:lts-jdk21

USER root

# Base tools and Python for running the sample app tests on the built-in node.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg lsb-release \
        python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI only (the daemon is the host's, reached through the mounted socket).
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

# Preinstall the "suggested" plugin set so the setup wizard is fast in class.
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
