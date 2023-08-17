FROM public.ecr.aws/amazonlinux/amazonlinux:2
RUN yum update -y && \
    yum install -y python3 && \
    yum clean all && \
    rm -rf /var/cache/yum

COPY . ./
RUN chmod +x ./client.py

CMD ["python3", "-u", "./client.py"]
