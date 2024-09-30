FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
# workdir
WORKDIR /pro_gym
# copy files
COPY . /pro_gym
# install dependency
RUN apt-get update && apt-get install -y dpkg \
    dpkg \
    wget \
    git \ 
    python3.10 \
    python3-pip \
    python-is-python3 \
    vim \
    mono-complete \
    mono-vbnc \
    gtk-sharp2 \
    libfontconfig1-dev \
    coinor-libipopt1v5 \ 
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# install dwsim
RUN wget -O /tmp/dwsim_8.8.0-amd64.deb https://github.com/DanWBR/dwsim/releases/download/v8.8.0/dwsim_8.8.0-amd64.deb
RUN dpkg -i /tmp/dwsim_8.8.0-amd64.deb || true

# clean up to reduce image size
RUN rm /tmp/dwsim_8.8.0-amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pythonnet tabulate numpy matplotlib tqdm pyyaml
# install pro_gym
RUN pip3 install -e .
# keep the container running
CMD ["tail", "-f", "/dev/null"]
