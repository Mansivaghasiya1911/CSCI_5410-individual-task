# Pulling python image
FROM python:3.9

# Switching working directory
WORKDIR /usr/src/

# Install requirements


# Copy req file
COPY requirement.txt requirement.txt

RUN pip install -r requirement.txt

# copy content
COPY . .

EXPOSE 5002

# config container in an executed manner
# ENTRYPOINT [ "python" ]

# CMD [ "main.py" ]

CMD ["python","-u","main.py"]