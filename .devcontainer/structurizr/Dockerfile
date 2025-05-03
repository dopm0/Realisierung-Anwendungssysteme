FROM structurizr/lite
ENV PORT 8080

EXPOSE ${PORT}

CMD ["java", "-Djdk.util.jar.enableMultiRelease=false", "-Dserver.port=${PORT}", "-jar", "/usr/local/structurizr-lite.war"]