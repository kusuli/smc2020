# coding: utf-8
# 2020.06.24
import sys
sys.path.append("tps")
from tps import TPS
import setting
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
import json

class Base:

	def __init__(self, param_file_path=''):
		self.tps = TPS()
		self.load_params(param_file_path)
		self.print_min_level = 1
	
	def load_params(self, param_file_path):
		if param_file_path != '':
			with open(param_file_path, mode='r') as fp:
				self.params = json.load(fp)
		else:
			self.params = {}
		self.load_params2()
	
	def load_params2(self):
		if 'tps_coef_i' not in self.params:
			self.params['tps_coef_i'] = 0.5
		if 'tps_coef_j' not in self.params:
			self.params['tps_coef_j'] = 0.5
		if 'tps_coef_k' not in self.params:
			self.params['tps_coef_k'] = 0.5
		if 'note_on_chord' not in self.params:
			self.params['note_on_chord'] = 0.5
		if 'note_out_of_scale' not in self.params:
			self.params['note_out_of_scale'] = 0.5
		if 'note_out_of_chord' not in self.params:
			self.params['note_out_of_chord'] = 0.5
		self.tps.coef_i = self.params['tps_coef_i']
		self.tps.coef_j = self.params['tps_coef_j']
		self.tps.coef_k = self.params['tps_coef_k']

	def chord_str_to_tpl(self, chord_str):
		chord_str0 = chord_str.split(':')[0]
		tone_pos = self.tone_str_to_pos(chord_str0)
		if 'min' in chord_str:
			return (tone_pos, False, 1)
		else:
			return (tone_pos, True, 1)
	
	def tone_str_to_pos(self, tone_str):
		tone_str = tone_str.replace('Ab', 'G#')
		tone_str = tone_str.replace('Bb', 'A#')
		tone_str = tone_str.replace('Cb', 'B')
		tone_str = tone_str.replace('B#', 'C')
		tone_str = tone_str.replace('Db', 'C#')
		tone_str = tone_str.replace('Eb', 'D#')
		tone_str = tone_str.replace('Fb', 'E')
		tone_str = tone_str.replace('E#', 'F')
		tone_str = tone_str.replace('Gb', 'F#')
		dic = {'A': 0, 'A#': 1, 'B': 2, 'C': 3, 'C#': 4, 'D': 5, 'D#': 6, 'E': 7, 'F': 8, 'F#': 9, 'G': 10, 'G#': 11}
		if tone_str in dic.keys():
			return dic[tone_str]
		else:
			raise Exception('invalid tone expression', tone_str)
			return -1

	def get_chord_interpretation(self, chord_str):
		tpl = self.chord_str_to_tpl(chord_str)
		if tpl[1]: # major
			return [
					(tpl, 0),
					(((tpl[0] + 9) % 12, False, 3), 0),
					(((tpl[0] + 7) % 12, True, 4), 0),
					(((tpl[0] + 4) % 12, False, 6), 0),
					(((tpl[0] + 5) % 12, True, 5), 0),
					(((tpl[0] + 2) % 12, False, 7), 0)
			]
		else: #minor
			return [
					(tpl, 0),
					(((tpl[0] + 3) % 12, True, 6), 0),
					(((tpl[0] + 7) % 12, False, 4), 0),
					(((tpl[0] + 10) % 12, True, 2), 0),
					(((tpl[0] + 5) % 12, False, 5), 0),
					(((tpl[0] + 8) % 12, True, 3), 0)
			]
	
	def get_chord_root_pos(self, tpl):
		if tpl[1]: # major
			scale = [0, 2, 4, 5, 7, 9, 11]
		else: #minor
			scale = [0, 2, 3, 5, 7, 8, 10]
		return (tpl[0] + scale[tpl[2] - 1]) % 12
	
	def chord_tpl_to_str(self, tpl):
		(key, b_major, degree) = tpl
		arr = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
		ret = ''
		if b_major:
			if degree == 1:
				ret = 'I'
			elif degree == 2:
				ret = 'ii'
			elif degree == 3:
				ret = 'iii'
			elif degree == 4:
				ret = 'IV'
			elif degree == 5:
				ret = 'V'
			elif degree == 6:
				ret = 'vi'
			else:
				ret = 'ERROR'
		else:
			if degree == 1:
				ret = 'i'
			elif degree == 3:
				ret = 'III'
			elif degree == 4:
				ret = 'iv'
			elif degree == 5:
				ret = 'v'
			elif degree == 6:
				ret = 'VI'
			elif degree == 7:
				ret = 'VII'
			else:
				ret = 'ERROR'
		ret += '/'
		if b_major:
			ret += arr[key]
		else:
			ret += arr[key].lower()
		return ret
	
	def get_tps_distance(self, rt1, rt2):
		scale_1 = setting.SCALE_MAJOR
		if not rt1[1]:
			scale_1 = setting.SCALE_NATURAL_MINOR
		scale_2 = setting.SCALE_MAJOR
		if not rt2[1]:
			scale_2 = setting.SCALE_NATURAL_MINOR
		return self.tps.get_distance2(rt1[0], scale_1, rt1[2], rt2[0], scale_2, rt2[2])
	
	def get_optimal_path_for_chord_str_list(self, chord_str_list, b_noise = True):
		chord_interpretation_list_list = []
		for c in chord_str_list:
			if type(c) == set:
				chord_interpretation_list = []
				for c2 in c:
					temp = self.get_chord_interpretation(c2)
					chord_interpretation_list.extend(temp)
				chord_interpretation_list_list.append(chord_interpretation_list)
			else:
				chord_interpretation_list_list.append(self.get_chord_interpretation(c))
		return self.get_optimal_path(self.get_interpretation_graph(chord_interpretation_list_list, b_noise))
	
	def get_optimal_path(self, graph):
		path_list_gen = nx.all_shortest_paths(graph, source='start', target='end', weight='weight')
		return graph, path_list_gen
	
	def get_interpretation_graph(self, chord_interpretation_list_list, b_noise = True):
		graph = nx.DiGraph()
		self.get_interpretation_graph_construct_graph(chord_interpretation_list_list, graph)
		self.get_interpretation_graph_modify_graph(chord_interpretation_list_list, graph)
		if b_noise:
			for edge in graph.edges(data=True):
				graph.add_edge(edge[0], edge[1], weight=edge[2]['weight'] + abs(np.random.normal(0, setting.NOISE_SD) if b_noise else 0))
		return graph
	
	def get_interpretation_graph_construct_graph(self, chord_interpretation_list_list, graph):
		graph.add_node('start', label='start')
		prev_c_dic_v = []
		for c_dic_i, c_dic_v in enumerate(chord_interpretation_list_list):
			for dst_i, dst_v in enumerate(c_dic_v):
				dst_node = str(c_dic_i) + ',' + str(dst_i)
				graph.add_node(dst_node, tpl=dst_v[0], label=dst_v[0])
				if c_dic_i == 0:
					graph.add_edge('start', dst_node, weight=dst_v[1])
				else:
					for src_i, src_v in enumerate(prev_c_dic_v):
						src_node = str(c_dic_i - 1) + ',' + str(src_i)
						graph.add_edge(src_node, dst_node, weight=self.get_tps_distance(src_v[0], dst_v[0]) + dst_v[1])
			prev_c_dic_v = c_dic_v
		graph.add_node('end', label='end')
		for src_i, src_v in enumerate(prev_c_dic_v):
			src_node = str(c_dic_i) + ',' + str(src_i)
			graph.add_edge(src_node, 'end', weight=0)
	
	def get_interpretation_graph_modify_graph(self, chord_interpretation_list_list, graph):
		pass
	
	def graph_add_interpretation(self, graph, new_interpretation, path, label_dic):
		END_INDEX = 0
		START_INDEX = 1
		node_count = len(graph.nodes)
		if node_count == 0:
			graph.add_node(END_INDEX, label='end')
			label_dic[END_INDEX] = 'end'
			node_count += 1
			graph.add_node(START_INDEX, label='start')
			label_dic[START_INDEX] = 'start'
			node_count += 1
			for i in range(1, len(new_interpretation) - 1):
				graph.add_node(node_count, label=new_interpretation[i])
				label_dic[node_count] = str(i) + ': ' + self.chord_tpl_to_str(new_interpretation[i]) + ': ' + path[i]
				graph.add_edge(node_count - 1, node_count)
				node_count += 1
			graph.add_edge(node_count - 1, END_INDEX)
		else:
			(forward_index, forward_node_index) = self.graph_add_interpretation_check_forward(graph, START_INDEX, new_interpretation, 0)
			if forward_index == -1:
				return
			(backword_index, backword_node_index) = self.graph_add_interpretation_check_backword(graph, END_INDEX, new_interpretation, len(new_interpretation) - 1, forward_index + 1)
			src_node_index = forward_node_index
			if forward_index < backword_index:
				for i in range(forward_index + 1, backword_index):
					graph.add_node(node_count, label=new_interpretation[i])
					label_dic[node_count] = str(i) + ': ' + self.chord_tpl_to_str(new_interpretation[i]) + ': ' + path[i]
					graph.add_edge(src_node_index, node_count)
					src_node_index = node_count
					node_count += 1
				graph.add_edge(src_node_index, backword_node_index)
	
	def graph_add_interpretation_check_forward(self, graph, node_index, new_interpretation, index):
		if new_interpretation[index] == graph.nodes[node_index]['label']:
			ret_index = index
			ret_node_index = node_index
			for child_node_index in graph.successors(node_index):
				(temp_index, temp_node_index) = self.graph_add_interpretation_check_forward(graph, child_node_index, new_interpretation, index + 1)
				if temp_index > ret_index:
					ret_index = temp_index
					ret_node_index = temp_node_index
			return (ret_index, ret_node_index)
		else:
			return (-1, None)
	
	def graph_add_interpretation_check_backword(self, graph, node_index, new_interpretation, index, min_index):
		if new_interpretation[index] == graph.nodes[node_index]['label']:
			ret_index = index
			ret_node_index = node_index
			if ret_index > min_index:
				for parent_node_index in graph.predecessors(node_index):
					(temp_index, temp_node_index) = self.graph_add_interpretation_check_backword(graph, parent_node_index, new_interpretation, index - 1, min_index)
					if temp_index < ret_index:
						ret_index = temp_index
						ret_node_index = temp_node_index
			return (ret_index, ret_node_index)
		else:
			return (len(new_interpretation), None)
	
	def show_path(self, graph, path_list_gen, mode):
		START_INDEX = 1
		if mode == 1:
			pass
		elif mode == 2:
			path_count = 0
			nodes = dict(graph.nodes)
			all_path_graph = nx.DiGraph()
			label_dic = {}
			for i0, path in enumerate(path_list_gen):
				path_count += 1
				interpretation_list = []
				for i, v in enumerate(path):
					interpretation_list.append(nodes[v]['label'])
				self.graph_add_interpretation(all_path_graph, interpretation_list, path, label_dic)
			all_path_graph.add_node('dummy1')
			graph_pos = {'dummy1': [20, 0]}
			current_x = 0
			current_y = 0
			current_node_list = [START_INDEX]
			next_node_list = []
			while len(current_node_list) > 0:
				current_x = 0
				for n in current_node_list:
					child_list = all_path_graph.successors(n)
					graph_pos[n] = [current_x, current_y]
					current_x += 1
					for c in child_list:
						if c not in next_node_list:
							next_node_list.append(c)
				current_node_list = next_node_list
				next_node_list = []
				current_y -= 1
			nx.draw(all_path_graph, graph_pos, with_labels=True, labels=label_dic)
			plt.show()
		elif mode == 4:
			nodes = dict(graph.nodes)
			for i, path in enumerate(path_list_gen):
				for i2, p in enumerate(path):
					node = nodes[p]
					if 'tpl' in node:
						temp = str(node['tpl']) + ' ' + self.chord_tpl_to_str(node['tpl'])
					else:
						temp = node
		elif mode == 3:
			node_index = 'start'
			total_distance = 0
			for i, tpl in enumerate(check_path):
				for e in graph.out_edges(node_index, data=True):
					if graph.nodes[e[1]]['tpl'] == tpl:
						node_index = e[1]
						total_distance += int(e[2]['weight'])
						break
				else:
					pass
	
	def get_chord_accuracy(self, graph, chord_str_list, path, graph_nodes = None, check_index_list = []):
		return -1
	
	def get_average_chord_accuracy(self, graph, chord_str_list, path_gen, check_index_list = []):
		path_count = 0
		accuracy = 0
		graph_nodes = dict(graph.nodes)
		for path in path_gen:
			path_count += 1
			accuracy += self.get_chord_accuracy(graph, chord_str_list, path, graph_nodes, check_index_list)
		return path_count, accuracy / path_count
	
	def get_random_chord_str_list(self, chord_str_list):
		return []
	
	def train(self, training_file_path_set, validation_file_path_set, epoch = 10, batch_size = 10, param_save_path = './new_params.txt'):
		learning_rate = 0.0001
		training_list = []
		validation_list = []
		for file_path in training_file_path_set:
			chord_str_list, note_set_list = self.load_music_data(file_path)
			training_list.append((chord_str_list, note_set_list))
		for file_path in validation_file_path_set:
			chord_str_list, note_set_list = self.load_music_data(file_path)
			validation_list.append((chord_str_list, note_set_list))
		graph, path_list_gen = self.get_optimal_path_for_melody(validation_list[0][1])
		del graph, path_list_gen
		for ep in range(epoch):
			grad = self.get_param_update_dict(training_list[0][1], training_list[0][0], random_count=5, change_rate=0.1)
			for key in grad:
				if key == 'interpretation_change_cost' or key.find('note') >= 0:
					self.params[key] = max(0, (1 - learning_rate) * self.params[key] + learning_rate * grad[key])
				else:
					self.params[key] = (1 - learning_rate) * self.params[key] + learning_rate * grad[key]
			if ep > 0 and ep % 100 == 0:
				with open(param_save_path, mode='w') as fp:
					json.dump(self.params, fp, indent=2)
				graph, path_list_gen = self.get_optimal_path_for_melody(validation_list[0][1])
				del graph, path_list_gen
	
	def train2(self, training_file_path_set, validation_file_path_set, epoch = 10, batch_size = 10, param_save_path = './new_params.txt'):
		learning_rate = 0.001
		chord_str_list, note_set_list = self.load_music_data(list(training_file_path_set)[0])
		chord_interpretation_list_list = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, chord_str_list)
		random_chord_str_list = self.get_random_chord_str_list(chord_str_list, change_rate=1)
		chord_interpretation_list_list2 = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, random_chord_str_list)
		for chord_i, chord_v in enumerate(chord_interpretation_list_list):
			if chord_interpretation_list_list[chord_i][0] != chord_interpretation_list_list2[chord_i][0]:
				chord_interpretation_list_list[chord_i].extend(chord_interpretation_list_list2[chord_i])
		graph = self.get_interpretation_graph(chord_interpretation_list_list, False)
		graph, path_list_gen = self.get_optimal_path(graph)
		del graph, path_list_gen
		for ep in range(epoch):
			grad = self.get_param_update_dict(note_set_list, chord_str_list, random_count=1, the_chord_str_list=random_chord_str_list)
			for key in grad:
				if key == 'interpretation_change_cost' or key.find('note') >= 0:
					self.params[key] = max(0, (1 - learning_rate) * self.params[key] + learning_rate * grad[key])
				else:
					self.params[key] = (1 - learning_rate) * self.params[key] + learning_rate * grad[key]
			if ep > 0 and ep % 1 == 0:
				with open(param_save_path, mode='w') as fp:
					json.dump(self.params, fp, indent=2)
				chord_interpretation_list_list = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, chord_str_list)
				chord_interpretation_list_list2 = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, random_chord_str_list)
				for chord_i, chord_v in enumerate(chord_interpretation_list_list):
					if chord_interpretation_list_list[chord_i][0] != chord_interpretation_list_list2[chord_i][0]:
						chord_interpretation_list_list[chord_i].extend(chord_interpretation_list_list2[chord_i])
				graph = self.get_interpretation_graph(chord_interpretation_list_list, False)
				graph, path_list_gen = self.get_optimal_path(graph)
				del graph, path_list_gen
	
	def get_param_update_dict(self, note_set_list, chord_str_list, random_count = 1, change_rate = 0.1, the_chord_str_list = []):
		interpretation_list_list = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, chord_str_list)
		graph = self.get_interpretation_graph(interpretation_list_list)
		_, path_list_gen = self.get_optimal_path(graph)
		positive_grad = self.get_params_coef(graph, note_set_list, next(path_list_gen))
		negative_grad_list = []
		for i in range(random_count):
			if len(the_chord_str_list) > 0:
				random_chord_str_list = the_chord_str_list
			else:
				random_chord_str_list = self.get_random_chord_str_list(chord_str_list, change_rate=change_rate)
			interpretation_list_list = self.get_chord_interpretation_list_list_from_melody_and_chord_list(note_set_list, random_chord_str_list)
			graph = self.get_interpretation_graph(interpretation_list_list)
			_, path_list_gen = self.get_optimal_path(graph)
			temp = self.get_params_coef(graph, note_set_list, next(path_list_gen))
			negative_grad_list.append(temp)
		ret = {}
		for key in positive_grad:
			ret[key] = -positive_grad[key]
			for i in range(random_count):
				ret[key] += negative_grad_list[i][key] / random_count
		return ret
	
	def get_params_coef(self, graph, note_set_list, path):
		org_cost = self.get_new_path_cost(graph, note_set_list, path)
		param_keys = self.params.keys()
		delta = 0.001
		grad = {}
		for k in param_keys:
			self.params[k] += delta
			new_cost = self.get_new_path_cost(graph, note_set_list, path)
			self.params[k] -= delta
			grad[k] = (new_cost - org_cost) / delta
		return grad
	
	def get_new_path_cost(self, graph, note_set_list, path):
		self.tps.coef_i = self.params['tps_coef_i']
		self.tps.coef_j = self.params['tps_coef_j']
		self.tps.coef_k = self.params['tps_coef_k']
		self.tps.stored_distances = {}
		chord_interpretation_list_list = self.get_chord_interpretation_list_list_for_melody(note_set_list, False)
		nodes = dict(graph.nodes)
		current_index = 1
		for chord_i, chord_v in enumerate(chord_interpretation_list_list):
			tpl1 = nodes[path[current_index]]['tpl']
			tpl2 = nodes[path[current_index + 1]]['tpl']
			if path[current_index + 2].find('inter') >= 0:
				current_index += 1
			current_index += 2
			temp_list = []
			for int_i, int_v in enumerate(chord_v):
				if int_v[0] == tpl1 or int_v[0] == tpl2:
					temp_list.append(int_v)
			chord_interpretation_list_list[chord_i] = temp_list
		graph2 = self.get_interpretation_graph(chord_interpretation_list_list, False)
		nodes2 = dict(graph2.nodes)
		nodes2_org = nodes2.copy()
		current_index = 1
		for chord_i, chord_v in enumerate(chord_interpretation_list_list):
			tpl1 = nodes[path[current_index]]['tpl']
			tpl2 = nodes[path[current_index + 1]]['tpl']
			if path[current_index + 2].find('inter') >= 0:
				current_index += 1
			current_index += 2
			for node_id in nodes2_org:
				if node_id.find(str(chord_i) + '_i') == 0 and nodes2_org[node_id]['tpl'] != tpl1:
					graph2.remove_node(node_id)
				if node_id.find(str(chord_i) + '_o') == 0 and nodes2_org[node_id]['tpl'] != tpl2:
					graph2.remove_node(node_id)
		_, path2_gen = self.get_optimal_path(graph2)
		path2 = next(path2_gen)
		return self.get_path_cost(graph2, path2)
	
	def get_path_cost(self, graph, path):
		cost = 0
		nodes = dict(graph.nodes)
		for node_i, node in enumerate(path):
			if node_i > 0:
				edge = graph.get_edge_data(path[node_i - 1], node)
				cost += float(edge['weight'])
		return cost
	
	def load_music_data(self, data_path):
		chord_str_list = []
		note_set_list = []
		f = open(data_path, "r")
		reader = csv.reader(f)
		for row in reader:
			if row[0][0:2] == '//':
				pass
			else:
				chord_str_list.append(row[0].strip())
				temp = set()
				for i in range(1, len(row)):
					temp.add(row[i].strip())
				note_set_list.append(temp)
		f.close()
		return chord_str_list, note_set_list
	
	def get_optimal_path_for_melody(self, note_set_list, b_noise = True):
		return self.get_optimal_path(self.get_interpretation_graph(self.get_chord_interpretation_list_list_for_melody(note_set_list), b_noise))
	
	def get_chord_interpretation_list_list_from_melody_and_chord_list(self, note_set_list, chord_str_list):
		return []
	
	def get_chord_interpretation_list_list_for_melody(self, note_set_list, b_reduce = True):
		chord_interpretation_list_list = []
		for note_set_i, note_set in enumerate(note_set_list):
			tone_pos_set = set(self.tone_str_to_pos(note) for note in note_set)
			temp = self.get_chord_distances_from_notes(tone_pos_set)
			if b_reduce:
				chord_interpretation_list_list.append([(k, temp[k]) for k in temp if len(set(self.get_related_tones(k)[0]) & tone_pos_set) > 0])
			else:
				chord_interpretation_list_list.append([(k, temp[k]) for k in temp])
		return chord_interpretation_list_list
	
	def get_chord_distances_from_notes(self, tone_pos_set):
		count = len(tone_pos_set)
		all = []
		for tone_pos in tone_pos_set:
			all.append(self.get_chord_distances_from_note(tone_pos))
		ret = {}
		for k in all[0]:
			ret[k] = 0
			for i in range(count):
				ret[k] += all[i][k] / count
		return ret
	
	def get_chord_distances_from_note(self, tone_pos):
		ret = {}
		for key in range(12):
			for b_major in (True, False):
				for degree in range(1, 8):
					if (b_major and degree != 7) or (not b_major and degree != 2):
						ret[(key, b_major, degree)] = self.get_chord_distance_from_note(tone_pos, (key, b_major, degree))
		return ret
	
	def get_chord_distance_from_note(self, tone_pos, chode_tpl):
		(chord_tone_list, scale) = self.get_related_tones(chode_tpl)
		if tone_pos in chord_tone_list:
			return self.params['note_on_chord']
		elif tone_pos in scale:
			return self.params['note_out_of_chord']
		else:
			return self.params['note_out_of_scale']
	
	def get_related_tones(self, chode_tpl):
		(key, b_major, degree) = chode_tpl
		if b_major:
			scale = [key, (key + 2) % 12, (key + 4) % 12, (key + 5) % 12, (key + 7) % 12, (key + 9) % 12, (key + 11) % 12]
		else:
			scale = [key, (key + 2) % 12, (key + 3) % 12, (key + 5) % 12, (key + 7) % 12, (key + 8) % 12, (key + 10) % 12]
		chord_tone_list = [scale[degree - 1], scale[(degree - 1 + 2) % 7], scale[(degree - 1 + 4) % 7]]
		return (chord_tone_list, scale)
