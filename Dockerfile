FROM ubuntu:22.04

RUN apt-get update \
 && apt-get install -y blender python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x start.sh
CMD ["./start.sh"]
