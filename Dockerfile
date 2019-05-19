FROM python:3.6
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


COPY ./requirements.txt /tmp

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt --no-cache-dir --disable-pip-version-check -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /project208
EXPOSE 5000
CMD ["uwsgi", "--ini", "/project208/uwsgi.ini"]
