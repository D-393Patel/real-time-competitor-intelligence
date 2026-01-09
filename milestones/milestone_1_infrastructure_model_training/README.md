📌 Milestone 1: Project infrastructure, Installing essential tools required for project and Trained model from scratch.

📖 Overview

This milestone focuses on setting up the project infrastructure, installing essential tools, and implementing a Deep Neural Network from scratch using NumPy.
The model is designed for classification tasks, with a primary focus on MNIST digit recognition. No high-level deep learning frameworks (TensorFlow/PyTorch) are used, ensuring a strong understanding of core neural network concepts.

🛠️ Tools & Technologies

Python

NumPy – Numerical computation

Pillow (PIL) – Image preprocessing

Matplotlib – Training visualization

🧠 DeepNeuralNetwork Architecture

The DeepNeuralNetwork class implements a 4-layer feedforward neural network:

Input Layer (784)
↓
Hidden Layer 1 (128 neurons)
↓
Hidden Layer 2 (64 neurons)
↓
Output Layer (10 classes)

Key Parameters

sizes: Defines neurons per layer (e.g., [784, 128, 64, 10])

epochs: Number of full training passes

learning rate: Controls weight update step size

Weights are initialized using scaled random normal initialization to reduce exploding/vanishing gradients.

🔁 Core Components
Activation Functions

Sigmoid
Used in hidden layers; maps values between 0 and 1.
Includes derivative computation for backpropagation.

Softmax
Used in the output layer to convert scores into probability distributions.

Loss Function

Binary Cross-Entropy Loss
Computes prediction error and supports gradient calculation.

🔄 Forward & Backward Propagation
Forward Pass

Computes weighted sums and activations layer by layer

Stores intermediate values for backpropagation

Backward Pass

Implements backpropagation to compute gradients

Uses chain rule with activation and loss derivatives

Parameter Update

Uses Stochastic Gradient Descent (SGD)

Updates weights using:

W = W - learning_rate × gradient

📊 Training & Evaluation

The train() method handles epoch-wise training

Computes training and validation accuracy & loss

Metrics are stored and plotted to visualize learning trends

🖼️ Image Preprocessing

The preprocess_image() function:

Loads image using Pillow

Converts to grayscale

Resizes to 28 × 28

Normalizes pixel values

Flattens into a 784-length vector

🔍 Digit Prediction

The predict_digit() function:

Reshapes image input into column format

Performs a forward pass

Uses argmax to predict the digit (0–9)

📈 Experimental Observations (ReLU Activation)

Configuration

Learning Rate: 0.01

Epochs: 100

Results

Training Accuracy: 99.90%

Validation Accuracy: 97.45%

Training Loss: 0.0117

Validation Loss: 0.0825

Analysis

ReLU activation significantly outperforms sigmoid in convergence speed and validation accuracy.
A small train–validation gap indicates mild overfitting, but overall performance is strong, making ReLU the most effective activation tested for this architecture.

✅ Milestone Outcome

Neural network successfully implemented from scratch

End-to-end training and inference pipeline completed

Strong validation performance achieved

Solid foundation established for future milestones
