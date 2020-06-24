import sys
from base import Base
from ext1 import Ext1
from ext2 import Ext2
from ext3 import Ext3
import util

base = Base('params.txt')
ext1 = Ext1('params.txt')
ext2 = Ext2('params.txt')
ext3 = Ext3('params.txt')

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
