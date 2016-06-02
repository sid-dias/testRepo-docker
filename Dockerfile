FROM siddias/java

COPY artifacts /opt/test-proj

WORKDIR /opt/test-proj/testRepo1
CMD ["java","Whoami"]
