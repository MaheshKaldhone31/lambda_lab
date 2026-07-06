FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
COPY requirements.txt ./
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install -r requirements.txt -t "${LAMBDA_RUNTIME_DIR}"

# Copy function code
COPY lambda_function.py ${LAMBDA_RUNTIME_DIR}
# If you have additional modules/folders, copy them here:
# COPY mymodule ${LAMBDA_RUNTIME_DIR}/mymodule

# Set the CMD to your handler (module.function)
# Replace lambda_function.lambda_handler with the correct module.function if different
CMD ["lambda_function.handler"]
