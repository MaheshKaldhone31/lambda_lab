FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
COPY requirements.txt ./
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install -r requirements.txt -t "${LAMBDA_RUNTIME_DIR}"

# Copy function code and UI
COPY lambda_function.py ${LAMBDA_RUNTIME_DIR}
COPY index.html ${LAMBDA_RUNTIME_DIR}

# Set the CMD to your handler (module.function)
# Replace lambda_function.lambda_handler with the correct module.function if different
CMD ["lambda_function.handler"]