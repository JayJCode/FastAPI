FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY processor/ /var/task/processor/
COPY watcher/ /var/task/watcher/
COPY api/ /var/task/api/

RUN pip install mangum

CMD ["processor.handler.categorize_wines"]