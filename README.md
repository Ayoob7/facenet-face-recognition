# Face Recognition System


This is the research product of the thesis "Manifold Learning of Latent Space Vectors in GAN for Image Synthesis". This has an application to the research, name a facial recognition system. The application was developed by consulting the FaceNet model (https://arxiv.org/pdf/1503.03832.pdf).

## Research Results
Please find the research results of ClusterGAN Manifold Learning Representations in the following link. 
[Results of the research](https://github.com/Ayoob7/facenet-face-recognition/blob/master/research_artifact/ClusterGAN.ipynb)


## How to use
Clone the repository from GitHub

	git clone https://github.com/Ayoob7/facenet-face-recognition.git

Install project requirements

	pip install -r requirements.txt

Run this in the root dir to launch the application.

	python Dashboard.py

This has a extensible, user operable facial recognition application.However, there are limitations with it as well. Anyone wishing to work on the limitations are welcome to do so.

1. Desktop GPU support for CUDA versions > 9.2
2. Python libraries such as Numba and Cython. ()
3. Facilitate FPGA model loading, for IOT applications. (Model Compression)
4. Make an ubiquitous network message broker (Like RabbitMQ) for IOT applications 
5. Research multi-process based threading better to stabilize inter process model inferencing

 
