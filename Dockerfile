FROM python:3.6.5
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /project208
EXPOSE 80
CMD ["uwsgi", "--ini", "/myblog/myblog-uwsgi.ini"]
