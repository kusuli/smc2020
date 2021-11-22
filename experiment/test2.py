import sys
import os
import copy
from base import Base
from ext1 import Ext1
from ext2 import Ext2
from ext3 import Ext3
import util
import setting

base = Base('params.txt')
ext1 = Ext1('params.txt')
ext2 = Ext2('params.txt')
ext3 = Ext3('params.txt')

cadence_pattern_list = [
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD],
		[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D]
]

degree_pattern_list = [
		[1, 2],
		[1, 3],
		[1, 4],
		[1, 5],
		[1, 6],
		[1, 7],
		[2, 1],
		[2, 3],
		[2, 4],
		[2, 5],
		[2, 6],
		[2, 7],
		[3, 1],
		[3, 2],
		[3, 4],
		[3, 5],
		[3, 6],
		[3, 7],
		[4, 1],
		[4, 2],
		[4, 3],
		[4, 5],
		[4, 6],
		[4, 7],
		[5, 1],
		[5, 2],
		[5, 3],
		[5, 4],
		[5, 6],
		[5, 7],
		[6, 1],
		[6, 2],
		[6, 3],
		[6, 4],
		[6, 5],
		[6, 7],
		[7, 1],
		[7, 2],
		[7, 3],
		[7, 4],
		[7, 5],
		[7, 6],
		[1, 2, 1],
		[1, 2, 3],
		[1, 2, 4],
		[1, 2, 5],
		[1, 2, 6],
		[1, 2, 7],
		[1, 3, 1],
		[1, 3, 2],
		[1, 3, 4],
		[1, 3, 5],
		[1, 3, 6],
		[1, 3, 7],
		[1, 4, 1],
		[1, 4, 2],
		[1, 4, 3],
		[1, 4, 5],
		[1, 4, 6],
		[1, 4, 7],
		[1, 5, 1],
		[1, 5, 2],
		[1, 5, 3],
		[1, 5, 4],
		[1, 5, 6],
		[1, 5, 7],
		[1, 6, 1],
		[1, 6, 2],
		[1, 6, 3],
		[1, 6, 4],
		[1, 6, 5],
		[1, 6, 7],
		[1, 7, 1],
		[1, 7, 2],
		[1, 7, 3],
		[1, 7, 4],
		[1, 7, 5],
		[1, 7, 6],
		[2, 1, 2],
		[2, 1, 3],
		[2, 1, 4],
		[2, 1, 5],
		[2, 1, 6],
		[2, 1, 7],
		[2, 3, 1],
		[2, 3, 2],
		[2, 3, 4],
		[2, 3, 5],
		[2, 3, 6],
		[2, 3, 7],
		[2, 4, 1],
		[2, 4, 2],
		[2, 4, 3],
		[2, 4, 5],
		[2, 4, 6],
		[2, 4, 7],
		[2, 5, 1],
		[2, 5, 2],
		[2, 5, 3],
		[2, 5, 4],
		[2, 5, 6],
		[2, 5, 7],
		[2, 6, 1],
		[2, 6, 2],
		[2, 6, 3],
		[2, 6, 4],
		[2, 6, 5],
		[2, 6, 7],
		[2, 7, 1],
		[2, 7, 2],
		[2, 7, 3],
		[2, 7, 4],
		[2, 7, 5],
		[2, 7, 6],
		[3, 1, 2],
		[3, 1, 3],
		[3, 1, 4],
		[3, 1, 5],
		[3, 1, 6],
		[3, 1, 7],
		[3, 2, 1],
		[3, 2, 3],
		[3, 2, 4],
		[3, 2, 5],
		[3, 2, 6],
		[3, 2, 7],
		[3, 4, 1],
		[3, 4, 2],
		[3, 4, 3],
		[3, 4, 5],
		[3, 4, 6],
		[3, 4, 7],
		[3, 5, 1],
		[3, 5, 2],
		[3, 5, 3],
		[3, 5, 4],
		[3, 5, 6],
		[3, 5, 7],
		[3, 6, 1],
		[3, 6, 2],
		[3, 6, 3],
		[3, 6, 4],
		[3, 6, 5],
		[3, 6, 7],
		[3, 7, 1],
		[3, 7, 2],
		[3, 7, 3],
		[3, 7, 4],
		[3, 7, 5],
		[3, 7, 6],
		[4, 1, 2],
		[4, 1, 3],
		[4, 1, 4],
		[4, 1, 5],
		[4, 1, 6],
		[4, 1, 7],
		[4, 2, 1],
		[4, 2, 3],
		[4, 2, 4],
		[4, 2, 5],
		[4, 2, 6],
		[4, 2, 7],
		[4, 3, 1],
		[4, 3, 2],
		[4, 3, 4],
		[4, 3, 5],
		[4, 3, 6],
		[4, 3, 7],
		[4, 5, 1],
		[4, 5, 2],
		[4, 5, 3],
		[4, 5, 4],
		[4, 5, 6],
		[4, 5, 7],
		[4, 6, 1],
		[4, 6, 2],
		[4, 6, 3],
		[4, 6, 4],
		[4, 6, 5],
		[4, 6, 7],
		[4, 7, 1],
		[4, 7, 2],
		[4, 7, 3],
		[4, 7, 4],
		[4, 7, 5],
		[4, 7, 6],
		[5, 1, 2],
		[5, 1, 3],
		[5, 1, 4],
		[5, 1, 5],
		[5, 1, 6],
		[5, 1, 7],
		[5, 2, 1],
		[5, 2, 3],
		[5, 2, 4],
		[5, 2, 5],
		[5, 2, 6],
		[5, 2, 7],
		[5, 3, 1],
		[5, 3, 2],
		[5, 3, 4],
		[5, 3, 5],
		[5, 3, 6],
		[5, 3, 7],
		[5, 4, 1],
		[5, 4, 2],
		[5, 4, 3],
		[5, 4, 5],
		[5, 4, 6],
		[5, 4, 7],
		[5, 6, 1],
		[5, 6, 2],
		[5, 6, 3],
		[5, 6, 4],
		[5, 6, 5],
		[5, 6, 7],
		[5, 7, 1],
		[5, 7, 2],
		[5, 7, 3],
		[5, 7, 4],
		[5, 7, 5],
		[5, 7, 6],
		[6, 1, 2],
		[6, 1, 3],
		[6, 1, 4],
		[6, 1, 5],
		[6, 1, 6],
		[6, 1, 7],
		[6, 2, 1],
		[6, 2, 3],
		[6, 2, 4],
		[6, 2, 5],
		[6, 2, 6],
		[6, 2, 7],
		[6, 3, 1],
		[6, 3, 2],
		[6, 3, 4],
		[6, 3, 5],
		[6, 3, 6],
		[6, 3, 7],
		[6, 4, 1],
		[6, 4, 2],
		[6, 4, 3],
		[6, 4, 5],
		[6, 4, 6],
		[6, 4, 7],
		[6, 5, 1],
		[6, 5, 2],
		[6, 5, 3],
		[6, 5, 4],
		[6, 5, 6],
		[6, 5, 7],
		[6, 7, 1],
		[6, 7, 2],
		[6, 7, 3],
		[6, 7, 4],
		[6, 7, 5],
		[6, 7, 6],
		[7, 1, 2],
		[7, 1, 3],
		[7, 1, 4],
		[7, 1, 5],
		[7, 1, 6],
		[7, 1, 7],
		[7, 2, 1],
		[7, 2, 3],
		[7, 2, 4],
		[7, 2, 5],
		[7, 2, 6],
		[7, 2, 7],
		[7, 3, 1],
		[7, 3, 2],
		[7, 3, 4],
		[7, 3, 5],
		[7, 3, 6],
		[7, 3, 7],
		[7, 4, 1],
		[7, 4, 2],
		[7, 4, 3],
		[7, 4, 5],
		[7, 4, 6],
		[7, 4, 7],
		[7, 5, 1],
		[7, 5, 2],
		[7, 5, 3],
		[7, 5, 4],
		[7, 5, 6],
		[7, 5, 7],
		[7, 6, 1],
		[7, 6, 2],
		[7, 6, 3],
		[7, 6, 4],
		[7, 6, 5],
		[7, 6, 7]
]

chord_length = 9
fork_index = 5 
dir_path = './data/'
output_file = 'output.txt'
output_string = ''
inst = base
inst.print_min_level = 6
all_pattern_list = copy.copy(cadence_pattern_list)
all_pattern_list.extend(degree_pattern_list)
for the_index, pattern in enumerate(all_pattern_list):
	inst.is_cadence_pattern = (the_index < len(cadence_pattern_list))
	#inst.cadence_pattern_list = [pattern]
	file_count = 0
	average_path_count = 0
	average_path_count_variance = 0
	average_accuracy = 0
	average_node_count = 0
	average_edge_count = 0
	average_slide_count = 0
	for file_name in os.listdir(dir_path):
		song_name, ext = os.path.splitext(file_name)
		if ext == '.txt':
			file_count += 1
			song_average_path_count = 0
			song_average_path_powered_count = 0
			song_average_accuracy = 0
			song_average_node_count = 0
			song_average_edge_count = 0
			song_slide_count = 0
			chord_str_list_y_org, _ = base.load_music_data(os.path.join(dir_path, file_name));
			if len(chord_str_list_y_org) < chord_length:
				file_count -= 1
				continue
			for start_pos in range(len(chord_str_list_y_org) - chord_length + 1):
				song_slide_count += 1
				chord_str_list_y = chord_str_list_y_org[start_pos : start_pos + chord_length]
				chord_str_list_x = copy.copy(chord_str_list_y);
				if fork_index > 0:
					all_chord_str_set = set()
					for key in ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']:
						if key != chord_str_list_y[fork_index - 1].split(':')[0] and key != chord_str_list_y[fork_index + 1].split(':')[0]:
							for chord_type in ['maj', '7', 'maj7', 'min', 'min7', 'dim', 'minmaj7', 'min7b5']:
								all_chord_str_set.add(key + ':' + chord_type)
					all_chord_str_set.add(chord_str_list_y[fork_index])
					chord_str_list_x[fork_index] = all_chord_str_set; 
				graph, path_list_gen = inst.get_optimal_path_for_chord_str_list(chord_str_list_x, b_noise=False);
				#inst.show_path(graph, path_list_gen, 4)
				count, average = inst.get_average_chord_accuracy(graph, chord_str_list_y, path_list_gen, [fork_index]);
				song_average_path_count += count
				#print('count: ', count)
				song_average_path_powered_count += count ** 2
				song_average_accuracy += average
				song_average_node_count += len(graph.nodes)
				song_average_edge_count += len(graph.edges)
			song_average_path_count /= song_slide_count
			song_path_count_variance = song_average_path_powered_count / song_slide_count - song_average_path_count ** 2
			song_average_accuracy /= song_slide_count
			song_average_node_count /= song_slide_count
			song_average_edge_count /= song_slide_count
			print('cadence {}, {}, {}, {}, {}, {:1.4f}, {}, {}, {}'.format(the_index, file_count, song_name, song_average_path_count, song_path_count_variance, song_average_accuracy, song_average_node_count, song_average_edge_count, song_slide_count))
			average_path_count += song_average_path_count
			average_accuracy += song_average_accuracy
			average_path_count_variance += song_path_count_variance
			average_node_count += song_average_node_count
			average_edge_count += song_average_edge_count
			average_slide_count += song_slide_count
	average_path_count /= file_count
	average_accuracy /= file_count
	average_path_count_variance /= file_count
	average_node_count /= file_count
	average_edge_count /= file_count
	average_slide_count /= file_count
	print('{}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}'.format(file_count, average_path_count, average_path_count_variance, average_accuracy, average_node_count, average_edge_count, average_slide_count))
	output_string += '{}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}, {:1.4f}\n'.format(file_count, average_path_count, average_path_count_variance, average_accuracy, average_node_count, average_edge_count, average_slide_count)
with open(os.path.join('./', output_file), mode='w') as f:
	f.write(output_string)
