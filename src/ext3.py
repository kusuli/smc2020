# 2020.06.24
from ext2 import Ext2
import copy
import util
import setting

class Ext3(Ext2):

	def __init__(self, param_file_path=''):
		self.extend_limit = 0
		self.is_cadence_pattern = True
		self.cadence_restriction = 1
		self.cadence_shortcut_order = 1
		self.added_count = 0
		self.cadence_pattern_list = self.get_cadence_patterns(0)
		super().__init__(param_file_path)
	
	def load_params2(self):
		super().load_params2()
		for cadence_i, cadence in enumerate(self.cadence_pattern_list):
			if 'cadence_weight' + str(cadence_i) not in self.params:
				self.params['cadence_weight' + str(cadence_i)] = 0.0
		if 'basic_cost' not in self.params:
			self.params['basic_cost'] = 0.1
	
	def get_tps_distance(self, tpl1, tpl2):
		return super().get_tps_distance(tpl1, tpl2) + float(self.params['basic_cost'])
	
	def get_cadence_patterns(self, cadence_pattern_type):
		if cadence_pattern_type == 0:
			return [
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T]
			]
		elif cadence_pattern_type == 1:
			return [
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
		elif cadence_pattern_type == 2:
			return [
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T]
			]
		elif cadence_pattern_type == 3:
			return [
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T]
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_T, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_SD, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
					[setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_SDM, setting.CHORD_FUNCTION_D, setting.CHORD_FUNCTION_T],
			]
		elif cadence_pattern_type == 4:
			return [
					[2, 5, 1]
			]
	
	def get_interpretation_graph_modify_graph(self, chord_interpretation_list_list, graph):
		self.added_count = 0
		for cadence_i, cadence in enumerate(self.cadence_pattern_list):
			for c_dic_i, c_dic_v in enumerate(chord_interpretation_list_list):
				for int_i, int_v in enumerate(c_dic_v):
					self.get_interpretation_graph_modify_graph2(chord_interpretation_list_list, graph, cadence_i, cadence, c_dic_i, int_i, 0, 0, [])
	
	def get_interpretation_graph_modify_graph2(self, chord_interpretation_list_list, graph, cadence_i, cadence, c_dic_i, int_i, cadence_inner_i, extend_count, path):
		tpl_index = 4
		if not self.is_cadence_pattern:
			tpl_index = 2
		b = False
		if len(path) == 0:
			b = True
		elif path[-1][2][0] == chord_interpretation_list_list[c_dic_i][int_i][0][0]:
			if self.cadence_restriction == 2 and ((path[-1][2][1] == setting.SCALE_MAJOR and chord_interpretation_list_list[c_dic_i][int_i][0][1] == setting.SCALE_MAJOR) or (path[-1][2][1] != setting.SCALE_MAJOR and chord_interpretation_list_list[c_dic_i][int_i][0][1] != setting.SCALE_MAJOR)):
				b = True
			elif self.cadence_restriction == 3 and path[-1][2][1] == chord_interpretation_list_list[c_dic_i][int_i][0][1]:
				b = True
			elif self.cadence_restriction == 1:
				b = True
		if b:
			if chord_interpretation_list_list[c_dic_i][int_i][0][tpl_index] == cadence[cadence_inner_i]:
				path.append((c_dic_i, int_i, chord_interpretation_list_list[c_dic_i][int_i][0]))
				if len(cadence) == cadence_inner_i + 1:
					self.added_count += 1
					postfix = ',' + str(self.added_count) + ',c' + str(cadence_i)
					prev_node_index = ''
					for path_i, p in enumerate(path):
						if path_i == 0:
							prev_node_index = str(p[0]) + '_o,' + str(p[1])
						elif path_i == len(path) - 1:
							node_index = str(p[0]) + '_i,' + str(p[1])
							original_edge = graph.get_edge_data(prev_node_index, node_index)
							original_weight = float(original_edge['weight'])
							if path_i == 1:
								graph.add_node(prev_node_index + postfix + ',inter', tpl=path[path_i - 1][2], label=path[path_i - 1][2])
								graph.add_edge(prev_node_index, prev_node_index + postfix + ',inter', weight=original_weight * util.sigmoid(self.params['cadence_weight' + str(cadence_i)]))
								graph.add_edge(prev_node_index + postfix + ',inter', node_index, weight=0)
							else:
								graph.add_edge(prev_node_index + postfix, node_index, weight=original_weight * util.sigmoid(self.params['cadence_weight' + str(cadence_i)]))
						else:
							node_index = str(p[0]) + '_i,' + str(p[1])
							original_edge = graph.get_edge_data(prev_node_index, node_index)
							original_weight = float(original_edge['weight'])
							graph.add_node(node_index + postfix, tpl=p[2], label=p[2])
							if path_i == 1:
								graph.add_edge(prev_node_index, node_index + postfix, weight=original_weight * util.sigmoid(self.params['cadence_weight' + str(cadence_i)]))
							else:
								graph.add_edge(prev_node_index + postfix, node_index + postfix, weight=original_weight * util.sigmoid(self.params['cadence_weight' + str(cadence_i)]))
							prev_node_index = node_index
							node_index = str(p[0]) + '_o,' + str(p[1])
							original_edge = graph.get_edge_data(prev_node_index, node_index)
							original_weight = float(original_edge['weight'])
							graph.add_node(node_index + postfix, tpl=p[2], label=p[2])
							graph.add_edge(prev_node_index + postfix, node_index + postfix, weight=0)
							prev_node_index = node_index
				c_dic_i2 = c_dic_i + 1
				if len(chord_interpretation_list_list) > c_dic_i2:
					for int_i2, int_v2 in enumerate(chord_interpretation_list_list[c_dic_i2]):
						if extend_count < self.extend_limit:
							self.get_interpretation_graph_modify_graph2(chord_interpretation_list_list, graph, cadence_i, cadence, c_dic_i2, int_i2, cadence_inner_i, extend_count + 1, copy.copy(path))
						if len(cadence) > cadence_inner_i + 1:
							self.get_interpretation_graph_modify_graph2(chord_interpretation_list_list, graph, cadence_i, cadence, c_dic_i2, int_i2, cadence_inner_i + 1, 0, copy.copy(path))
