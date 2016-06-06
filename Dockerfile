FROM siddias/java

COPY artifacts /opt/test-proj

WORKDIR /opt/test-proj/testRepo
CMD ["java","HelloWorld"]
