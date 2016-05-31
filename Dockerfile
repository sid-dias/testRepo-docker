FROM siddias/java

# Dependencies
RUN yum groupinstall -y "Development tools"
RUN yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline
RUN yum install -y tar

# Python 3.4.2
WORKDIR /usr/local/src
RUN curl -O https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
RUN tar -xvzf Python-3.4.2.tgz

WORKDIR /usr/local/src/Python-3.4.2
RUN ./configure --enable-shared --prefix=/usr/local LDFLAGS="-Wl,-rpath /usr/local/lib"
RUN make
RUN make altinstall

RUN ls /opt

COPY getArtifacts.py /opt/test-proj/
COPY deploy /opt/test-proj/

RUN chmod u+x /opt/test-proj/getArtifacts.py
RUN /opt/test-proj/getArtifacts.py

CMD ["/bin/bash"]
