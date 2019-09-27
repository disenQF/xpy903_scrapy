FROM realite/python3.6
MAINTAINER disen 610039018@qq.com
WORKDIR /usr/src
RUN mkdir chinaz
ADD . chinaz
WORKDIR /usr/src/chinaz
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
VOLUME /usr/src/chinaz
RUN chmod 775 /usr/src/chinaz/run.sh
RUN ln -s /usr/src/chinaz/run.sh /usr/bin/runspider
CMD /usr/src/chinaz/run.sh