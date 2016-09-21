from scipy.io import wavfile
import numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../")))
from args import args
from model import params, wavenet
from train import create_padded_batch
import data

def generate_audio():
	receptive_field_width_steps = 5

	batch_size = 1
	max_dilation = max(params.residual_conv_dilations)
	target_width = receptive_field_width_steps
	padded_input_width = receptive_field_width_steps + max_dilation

	# quantized signals generated by WaveNet
	generated_quantized_audio = np.zeros((padded_input_width, ), dtype=np.int32)

	for time_step in xrange(200):
		# quantized signals in receptive field
		padded_quantized_x_batch = generated_quantized_audio[-padded_input_width:].reshape((1, -1))

		# convert to image
		padded_x_batch = data.onehot_pixel_image(padded_quantized_x_batch, quantized_channels=params.quantization_steps)

		# generate next signal
		softmax = wavenet.forward_one_step(padded_x_batch, softmax=True, return_numpy=True)
		softmax = softmax[0, :, 0, -1]
		generated_quantized_signal = np.random.choice(np.arange(params.quantization_steps), p=softmax)
		generated_quantized_audio = np.append(generated_quantized_audio, [generated_quantized_signal], axis=0)

	print generated_quantized_audio

def main():
	generate_audio()

if __name__ == '__main__':
	main()
