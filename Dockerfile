# Dockerfile for 
FROM ubuntu:16.04

MAINTAINER Paul Manninger<paul.manninger@inspection.gc.ca>

ENV DEBIAN_FRONTEND noninteractive

# Install packages
RUN apt-get update -y -qq && apt-get install -y --allow \
	python-dev \
	git \
	curl \
#	libexpat1-dev \
#	libxml2-dev \
#	libxslt-dev \
#	zlib1g-dev \
#	libbz2-dev \
#	software-properties-common \
#	xsltproc \
#	libncurses5-dev \ 
#        pkg-config \ 
#        automake \
#	libtool \
	build-essential \
#	autoconf \
#	python-pip \
#	samtools \
#	bowtie2 \	
	nano && \
    	apt-get clean  && \
    	rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install biopython
RUN pip install numpy==1.9.1
RUN pip install biopython==1.69

# Install pysamstats
RUN pip install pysam==0.8.4
RUN pip install pysamstats==0.24.2

# Install the pipeline
RUN git clone https://github.com/OLC-LOC-Bioinformatics/geneSipprV2.git

# Edit the path

ENV PATH /geneSipprV2/sipprverse:$PATH
