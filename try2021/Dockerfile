FROM python:3.8.12-buster


RUN mkdir /root/mnlg
WORKDIR /root/mnlg
COPY . .


RUN mkdir /root/tmp
WORKDIR /root/tmp

RUN apt update

RUN wget https://www.grammaticalframework.org/download/gf_3.10-2_amd64.deb
RUN apt install -y ./gf_3.10-2_amd64.deb

RUN wget https://github.com/GrammaticalFramework/gf-rgl/archive/refs/tags/20201114.zip
RUN unzip 20201114.zip
RUN cd gf-rgl-20201114 && mkdir -p /root/opt/gf-rgl/dist && ./Setup.sh --dest=/root/opt/gf-rgl/dist


WORKDIR /root/mnlg

# 'make' will take several minutes
RUN cd gf && make
RUN cd gf && make test-bank

RUN pip install -r requirements.txt
RUN make
RUN make -C tests-i9n


ENTRYPOINT ["/usr/local/bin/python3", "/root/mnlg/gen.py", "--pgf", "/root/mnlg/gf/dist/Mnlg.pgf"]
CMD ["--lang", "en,de,es,ru,zh"]
