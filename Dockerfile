FROM dockerproxy.cn/nvidia/cuda:11.8.0-runtime-ubuntu22.04
LABEL \
    author="huangpeijun" \
    email="huangpeijun@everreachai.cn"
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt update && apt install dmidecode -y && apt install wget -y && apt clean all

RUN wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py310_23.9.0-0-Linux-x86_64.sh && \
    chmod 755 Miniconda3-py310_23.9.0-0-Linux-x86_64.sh && \
    ./Miniconda3-py310_23.9.0-0-Linux-x86_64.sh -b -p /opt/conda  && \
    rm -rf  ./Miniconda3-py310_23.9.0-0-Linux-x86_64.sh

RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda init bash && \
    conda activate base && \
    conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/ && \
    conda config --set show_channel_urls yes && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"

# Set PATH
ENV PATH=/opt/conda/bin:$PATH

# Install python requirements.txt
ADD requirements.txt .
RUN pip install -r requirements.txt  && pip cache purge && rm -f requirements.txt
ADD . /home/steps-chat
WORKDIR /home/steps-chat
EXPOSE 8501
CMD ["streamlit", "run", "./main.py", "--server.port", "8501"]
