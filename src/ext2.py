# 2020.06.24
from ext1 import Ext1
import util

class Ext2(Ext1):
	
	def load_params2(self):
		super().load_params2()
		if 'interpretation_change_cost' not in self.params:
			self.params['interpretation_change_cost'] = 0.5

	def get_interpretation_graph_construct_graph(self, chord_interpretation_list_list, graph):
		graph.add_node('start', label='start')
		prev_c_dic_v = []
		for c_dic_i, c_dic_v in enumerate(chord_interpretation_list_list):
			for dst_i, dst_v in enumerate(c_dic_v):
				dst_node = str(c_dic_i) + '_i,' + str(dst_i)
				graph.add_node(dst_node, tpl=dst_v[0], label=dst_v[0])
				if c_dic_i == 0:
					graph.add_edge('start', dst_node, weight=dst_v[1])
				else:
					for src_i, src_v in enumerate(prev_c_dic_v):
						src_node = str(c_dic_i - 1) + '_o,' + str(src_i)
						graph.add_edge(src_node, dst_node, weight=self.get_tps_distance(src_v[0], dst_v[0]) + dst_v[1])
			for dst_i, dst_v in enumerate(c_dic_v):
				dst_node = str(c_dic_i) + '_o,' + str(dst_i)
				graph.add_node(dst_node, tpl=dst_v[0], label=dst_v[0])
				target_list = self.get_chord_interpretation2(self.get_chord_root_pos(dst_v[0]), dst_v[0][3])
				target_list = [elm[0] for elm in target_list]
				for src_i, src_v in enumerate(c_dic_v):
						src_node = str(c_dic_i) + '_i,' + str(src_i)
						graph.add_edge(src_node, dst_node, weight=dst_v[1] + (self.params['interpretation_change_cost'] if src_v[0] != dst_v[0] else 0))
			prev_c_dic_v = c_dic_v
		graph.add_node('end', label='end')
		for src_i, src_v in enumerate(prev_c_dic_v):
			src_node = str(c_dic_i) + '_o,' + str(src_i)
			graph.add_edge(src_node, 'end', weight=0)
	
	def get_chord_accuracy(self, graph, chord_str_list, path, graph_nodes = None, check_index_list = []):
		correct_count = 0
		if graph_nodes == None:
			graph_nodes = dict(graph.nodes)
		current_index = 1
		for i, chord_str in enumerate(chord_str_list):
			pos1, type1 = self.chord_str_to_tpl(chord_str)
			tpl2 = graph_nodes[path[current_index]]['tpl']
			pos2 = self.get_chord_root_pos(tpl2)
			type2 = tpl2[3]
			current_index += 2
			if path[current_index].find('inter') >= 0:
				current_index += 1
			if len(check_index_list) == 0 or i in check_index_list:
				if pos1 == pos2 and type1 == type2:
					correct_count += 1
		if len(check_index_list) > 0:
			return correct_count / len(check_index_list)
		else:
			return correct_count / len(chord_str_list)
	
