FROM public.ecr.aws/lambda/python:3.11

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["lambda_function.handler"]
