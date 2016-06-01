FROM siddias/java

COPY build-info /opt/test-proj/build-info

CMD ["/bin/bash"]
