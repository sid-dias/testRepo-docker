FROM siddias/java

MAINTAINER Siddharth Dias

COPY ./getArtifacts.py /opt/test-proj

RUN /opt/test-proj/getArtifacts.py

CMD ["/bin/bash"]