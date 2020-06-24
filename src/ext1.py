# 2020.06.24
from base import Base
import setting
import random

class Ext1(Base):

	def __init__(self, param_file_path=''):
		self.b_tps_4_scales = True
		self.non_diatonic_mode = 0
		super().__init__(param_file_path)

	def chord_str_to_tpl(self, chord_str):
		chord_str0 = chord_str.split(':')[0]
		root_pos = self.tone_str_to_pos(chord_str0)
		chord_str1 = chord_str.split(':')[1]
		if chord_str1 == 'maj':
			return (root_pos, setting.CHORD_TYPE_MAJ)
		elif chord_str1 == '7' :
			return (root_pos, setting.CHORD_TYPE_7)
		elif chord_str1 == 'maj7' :
			return (root_pos, setting.CHORD_TYPE_MAJ7)
		elif chord_str1 == 'maj6':
			return (root_pos, setting.CHORD_TYPE_MAJ6)
		elif chord_str1 == 'min':
			return (root_pos, setting.CHORD_TYPE_MIN)
		elif chord_str1 == 'min7':
			return (root_pos, setting.CHORD_TYPE_MIN7)
		elif chord_str1 == 'minmaj7' :
			return (root_pos, setting.CHORD_TYPE_MINMAJ7)
		elif chord_str1 == 'min6':
			return (root_pos, setting.CHORD_TYPE_MIN6)
		elif chord_str1 == 'min7b5':
			return (root_pos, setting.CHORD_TYPE_MIN7_FLAT5)
		elif chord_str1 == 'dim' or chord_str1 == 'dim7':
			return (root_pos, setting.CHORD_TYPE_DIM7)
		else:
			raise Exception('invalid chord expression', chord_str)
			return (0, setting.CHORD_TYPE_MAJ)

	def get_chord_interpretation(self, chord_str):
		(root_pos, chord_type) = self.chord_str_to_tpl(chord_str)
		return self.get_chord_interpretation2(root_pos, chord_type)
	
	def get_chord_root_pos(self, tpl):
		if tpl[1] == setting.SCALE_MAJOR:
			scale = [0, 2, 4, 5, 7, 9, 11]
		elif tpl[1] == setting.SCALE_NATURAL_MINOR:
			scale = [0, 2, 3, 5, 7, 8, 10]
		elif tpl[1] == setting.SCALE_HARMONIC_MINOR:
			scale = [0, 2, 3, 5, 7, 8, 11]
		else:
			scale = [0, 2, 3, 5, 7, 9, 11]
		return (tpl[0] + scale[tpl[2] - 1]) % 12
	
	def get_chord_interpretation2(self, root_pos, chord_type, b_enharmonic = True):
		if chord_type == setting.CHORD_TYPE_MAJ:
			ret = [
					(((root_pos + 0) % 12,  setting.SCALE_MAJOR,          1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_MAJOR,          4, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 5) % 12,  setting.SCALE_MAJOR,          5, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 9) % 12,  setting.SCALE_NATURAL_MINOR,  3, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 5) % 12,  setting.SCALE_HARMONIC_MINOR, 5, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 7) % 12,  setting.SCALE_MELODIC_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 5) % 12,  setting.SCALE_MELODIC_MINOR,  5, chord_type, setting.CHORD_FUNCTION_D),   0)
			]
		elif chord_type == setting.CHORD_TYPE_7:
			ret = [
					(((root_pos + 5) % 12,  setting.SCALE_MAJOR,          5, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 2) % 12,  setting.SCALE_NATURAL_MINOR,  7, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 5) % 12,  setting.SCALE_HARMONIC_MINOR, 5, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 7) % 12,  setting.SCALE_MELODIC_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 5) % 12,  setting.SCALE_MELODIC_MINOR,  5, chord_type, setting.CHORD_FUNCTION_D),   0)
			]
			if self.non_diatonic_mode == 1:
				ret.append((((root_pos + 0) % 12,  setting.SCALE_MAJOR,          1, chord_type, setting.CHORD_FUNCTION_T),   0))
				ret.append((((root_pos + 1) % 12,  setting.SCALE_MELODIC_MINOR,  7, chord_type, setting.CHORD_FUNCTION_SD),  0))
				ret.append((((root_pos + 4) % 12,  setting.SCALE_NATURAL_MINOR,  6, chord_type, setting.CHORD_FUNCTION_SDM), 0))
				ret.append((((root_pos + 4) % 12,  setting.SCALE_HARMONIC_MINOR, 6, chord_type, setting.CHORD_FUNCTION_SDM), 0))
				ret.append((((root_pos + 11) % 12, setting.SCALE_HARMONIC_MINOR, 2, chord_type, setting.CHORD_FUNCTION_D),   0))
			elif self.non_diatonic_mode == 2:
				ret.append((((root_pos + 0) % 12,  setting.SCALE_MAJOR,          1, chord_type, setting.CHORD_FUNCTION_T),   1))
				ret.append((((root_pos + 1) % 12,  setting.SCALE_NATURAL_MINOR,  7, chord_type, setting.CHORD_FUNCTION_SD),  3))
				ret.append((((root_pos + 1) % 12,  setting.SCALE_HARMONIC_MINOR, 7, chord_type, setting.CHORD_FUNCTION_SD),  2))
				ret.append((((root_pos + 1) % 12,  setting.SCALE_MELODIC_MINOR,  7, chord_type, setting.CHORD_FUNCTION_SD),  1))
				ret.append((((root_pos + 4) % 12,  setting.SCALE_NATURAL_MINOR,  6, chord_type, setting.CHORD_FUNCTION_SDM), 1))
				ret.append((((root_pos + 4) % 12,  setting.SCALE_HARMONIC_MINOR, 6, chord_type, setting.CHORD_FUNCTION_SDM), 1))
				ret.append((((root_pos + 4) % 12,  setting.SCALE_MELODIC_MINOR,  6, chord_type, setting.CHORD_FUNCTION_SDM), 2))
				ret.append((((root_pos + 11) % 12, setting.SCALE_MAJOR,          2, chord_type, setting.CHORD_FUNCTION_D),   2))
				ret.append((((root_pos + 11) % 12, setting.SCALE_NATURAL_MINOR,  2, chord_type, setting.CHORD_FUNCTION_D),   2))
				ret.append((((root_pos + 11) % 12, setting.SCALE_HARMONIC_MINOR, 2, chord_type, setting.CHORD_FUNCTION_D),   1))
				ret.append((((root_pos + 11) % 12, setting.SCALE_MELODIC_MINOR,  2, chord_type, setting.CHORD_FUNCTION_D),   2))
		elif chord_type == setting.CHORD_TYPE_MAJ7:
			ret = [
					(((root_pos + 0) % 12,  setting.SCALE_MAJOR,          1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_MAJOR,          4, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 9) % 12,  setting.SCALE_NATURAL_MINOR,  3, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 4) % 12,  setting.SCALE_NATURAL_MINOR,  6, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 4) % 12,  setting.SCALE_HARMONIC_MINOR, 6, chord_type, setting.CHORD_FUNCTION_SDM), 0)
			]
			if self.non_diatonic_mode == 1:
				ret.append((((root_pos + 11) % 12,  setting.SCALE_NATURAL_MINOR,  2, chord_type, setting.CHORD_FUNCTION_SDM), 0))
				ret.append((((root_pos + 11) % 12,  setting.SCALE_HARMONIC_MINOR, 2, chord_type, setting.CHORD_FUNCTION_SDM), 0))
			elif self.non_diatonic_mode == 2:
				ret.append((((root_pos + 11) % 12,  setting.SCALE_NATURAL_MINOR,  2, chord_type, setting.CHORD_FUNCTION_SDM), 1))
				ret.append((((root_pos + 11) % 12,  setting.SCALE_HARMONIC_MINOR, 2, chord_type, setting.CHORD_FUNCTION_SDM), 1))
				ret.append((((root_pos + 11) % 12,  setting.SCALE_MELODIC_MINOR,  2, chord_type, setting.CHORD_FUNCTION_SDM), 2))
		elif chord_type == setting.CHORD_TYPE_MAJ6:
			ret = [
					(((root_pos + 0) % 12,  setting.SCALE_MAJOR,          1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_MAJOR,          4, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 7) % 12,  setting.SCALE_MELODIC_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SD),  0)
			]
		elif chord_type == setting.CHORD_TYPE_MIN:
			ret = [
					(((root_pos + 0) % 12,  setting.SCALE_NATURAL_MINOR,  1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_NATURAL_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 0) % 12,  setting.SCALE_HARMONIC_MINOR, 1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_HARMONIC_MINOR, 4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 0) % 12,  setting.SCALE_MELODIC_MINOR , 1, chord_type, setting.CHORD_FUNCTION_T),   0)
			]
		elif chord_type == setting.CHORD_TYPE_MIN7:
			ret = [
					(((root_pos + 10) % 12, setting.SCALE_MAJOR,          2, chord_type, setting.CHORD_FUNCTION_SD),  0),
					(((root_pos + 8) % 12,  setting.SCALE_MAJOR,          3, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 3) % 12,  setting.SCALE_MAJOR,          6, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 0) % 12,  setting.SCALE_NATURAL_MINOR,  1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 7) % 12,  setting.SCALE_NATURAL_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 5) % 12,  setting.SCALE_NATURAL_MINOR,  5, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 7) % 12,  setting.SCALE_HARMONIC_MINOR, 4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 10) % 12, setting.SCALE_MELODIC_MINOR , 2, chord_type, setting.CHORD_FUNCTION_SD),  0)
			]
		elif chord_type == setting.CHORD_TYPE_MINMAJ7:
			ret = [
					(((root_pos + 0) % 12,  setting.SCALE_HARMONIC_MINOR, 1, chord_type, setting.CHORD_FUNCTION_T),   0),
					(((root_pos + 0) % 12,  setting.SCALE_MELODIC_MINOR , 1, chord_type, setting.CHORD_FUNCTION_T),   0)
			]
		elif chord_type == setting.CHORD_TYPE_MIN6:
			ret = [
					(((root_pos + 7) % 12,  setting.SCALE_NATURAL_MINOR,  4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 7) % 12,  setting.SCALE_HARMONIC_MINOR, 4, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 0) % 12,  setting.SCALE_MELODIC_MINOR , 1, chord_type, setting.CHORD_FUNCTION_T),   0)
			]
		elif chord_type == setting.CHORD_TYPE_MIN7_FLAT5:
			ret = [
					(((root_pos + 1) % 12,  setting.SCALE_MAJOR,          7, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 10) % 12, setting.SCALE_NATURAL_MINOR,  2, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 10) % 12, setting.SCALE_HARMONIC_MINOR, 2, chord_type, setting.CHORD_FUNCTION_SDM), 0),
					(((root_pos + 1) % 12,  setting.SCALE_MELODIC_MINOR , 7, chord_type, setting.CHORD_FUNCTION_D),   0)
			]
			if self.non_diatonic_mode == 1:
				ret.append((((root_pos + 6) % 12,   setting.SCALE_MAJOR,          4, chord_type, setting.CHORD_FUNCTION_T),   0))
			elif self.non_diatonic_mode == 2:
				ret.append((((root_pos + 6) % 12,   setting.SCALE_MAJOR,          4, chord_type, setting.CHORD_FUNCTION_T),   1))
		elif chord_type == setting.CHORD_TYPE_DIM7:
			ret = [
					(((root_pos + 1) % 12,  setting.SCALE_HARMONIC_MINOR, 7, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 4) % 12,  setting.SCALE_HARMONIC_MINOR, 7, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 7) % 12,  setting.SCALE_HARMONIC_MINOR, 7, chord_type, setting.CHORD_FUNCTION_D),   0),
					(((root_pos + 10) % 12, setting.SCALE_HARMONIC_MINOR, 7, chord_type, setting.CHORD_FUNCTION_D),   0) 
			]
		else:
			raise Exception('no interpretation', chord_str)
			ret = []
		return ret
	
	def chord_tpl_to_str(self, tpl):
		(key, scale, degree, chord_type, chord_function) = tpl
		arr = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
		ret = str(degree) + '/' + arr[key] + ' ('
		if scale == setting.SCALE_MAJOR:
			ret += 'Maj'
		elif scale == setting.SCALE_NATURAL_MINOR:
			ret += 'Nat'
		elif scale == setting.SCALE_HARMONIC_MINOR:
			ret += 'Har'
		elif scale == setting.SCALE_MELODIC_MINOR:
			ret += 'Mel'
		ret += ') '
		root_pos = self.get_chord_root_pos(tpl)
		ret += arr[root_pos] + ':'
		if chord_type == setting.CHORD_TYPE_MAJ:
			ret += 'maj'
		elif chord_type == setting.CHORD_TYPE_7:
			ret += '7'
		elif chord_type == setting.CHORD_TYPE_MAJ7:
			ret += 'maj7'
		elif chord_type == setting.CHORD_TYPE_MAJ6:
			ret += 'maj6'
		elif chord_type == setting.CHORD_TYPE_MIN:
			ret += 'min'
		elif chord_type == setting.CHORD_TYPE_MIN7:
			ret += 'min7'
		elif chord_type == setting.CHORD_TYPE_MINMAJ7:
			ret += 'minmaj7'
		elif chord_type == setting.CHORD_TYPE_MIN6:
			ret += 'min6'
		elif chord_type == setting.CHORD_TYPE_MIN7_FLAT5:
			ret += 'min7b5'
		elif chord_type == setting.CHORD_TYPE_DIM7:
			ret += 'dim7'
		else:
			ret += 'error'
		ret += ' '
		if chord_function == setting.CHORD_FUNCTION_T:
			ret += 'T'
		elif chord_function == setting.CHORD_FUNCTION_SD:
			ret += 'SD'
		elif chord_function == setting.CHORD_FUNCTION_SDM:
			ret += 'SDM'
		elif chord_function == setting.CHORD_FUNCTION_D:
			ret += 'D'
		elif chord_function == setting.CHORD_FUNCTION_NONE:
			ret += 'N'
		else:
			ret += 'error'
		return ret
	
	def get_tps_distance(self, tpl1, tpl2):
		if self.b_tps_4_scales:
			return self.tps.get_distance2(tpl1[0], tpl1[1], tpl1[2], tpl2[0], tpl2[1], tpl2[2])
		else:
			scale_1 = tpl1[1]
			if scale_1 != setting.SCALE_MAJOR:
				scale_1 = setting.SCALE_NATURAL_MINOR
			scale_2 = tpl2[1]
			if scale_2 != setting.SCALE_MAJOR:
				scale_2 = setting.SCALE_NATURAL_MINOR
			return self.tps.get_distance2(tpl1[0], scale_1, tpl1[2], tpl2[0], scale_2, tpl2[2])
	
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
			current_index += 1
			if len(check_index_list) == 0 or i in check_index_list:
				if pos1 == pos2 and type1 == type2:
					correct_count += 1
		if len(check_index_list) > 0:
			return correct_count / len(check_index_list)
		else:
			return correct_count / len(chord_str_list)
	
	def get_chord_distances_from_notes(self, tone_pos_set):
		arr1 = []
		for key in range(12):
			for chord_type in range(1, setting.CHORD_TYPE_COUNT + 1):
				arr1.append((key, chord_type))
		arr2 = []
		for tpl1 in arr1:
			arr2.extend(self.get_chord_interpretation2(tpl1[0], tpl1[1]))
		set2 = set(arr2)
		dic3 = {}
		for tpl2 in set2:
			dic3[tpl2[0]] = tpl2[1]
			for tone_pos in tone_pos_set:
				dic3[tpl2[0]] += self.get_chord_distance_from_note(tone_pos, tpl2[0]) / len(tone_pos_set)
		return dic3
	
	def get_related_tones(self, chode_tpl):
		(key, scale, degree, chord_type, chord_function) = chode_tpl
		if scale == setting.SCALE_MAJOR:
			scale = [key, (key + 2) % 12, (key + 4) % 12, (key + 5) % 12, (key + 7) % 12, (key + 9) % 12, (key + 11) % 12]
		elif scale == setting.SCALE_NATURAL_MINOR:
			scale = [key, (key + 2) % 12, (key + 3) % 12, (key + 5) % 12, (key + 7) % 12, (key + 8) % 12, (key + 10) % 12]
		elif scale == setting.SCALE_HARMONIC_MINOR:
			scale = [key, (key + 2) % 12, (key + 3) % 12, (key + 5) % 12, (key + 7) % 12, (key + 8) % 12, (key + 11) % 12]
		else:
			scale = [key, (key + 2) % 12, (key + 3) % 12, (key + 5) % 12, (key + 7) % 12, (key + 9) % 12, (key + 11) % 12]
		base_pos = scale[degree - 1]
		if chord_type == setting.CHORD_TYPE_MAJ:
			chord_tone_list = [base_pos, (base_pos + 4) % 12, (base_pos + 7) % 12]
		elif chord_type == setting.CHORD_TYPE_7:
			chord_tone_list = [base_pos, (base_pos + 4) % 12, (base_pos + 7) % 12, (base_pos + 10) % 12]
		elif chord_type == setting.CHORD_TYPE_MAJ7:
			chord_tone_list = [base_pos, (base_pos + 4) % 12, (base_pos + 7) % 12, (base_pos + 11) % 12]
		elif chord_type == setting.CHORD_TYPE_MAJ6:
			chord_tone_list = [base_pos, (base_pos + 4) % 12, (base_pos + 7) % 12, (base_pos + 9) % 12]
		elif chord_type == setting.CHORD_TYPE_MIN:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 7) % 12]
		elif chord_type == setting.CHORD_TYPE_MIN7:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 7) % 12, (base_pos + 10) % 12]
		elif chord_type == setting.CHORD_TYPE_MINMAJ7:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 7) % 12, (base_pos + 11) % 12]
		elif chord_type == setting.CHORD_TYPE_MIN6:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 7) % 12, (base_pos + 9) % 12]
		elif chord_type == setting.CHORD_TYPE_MIN7_FLAT5:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 6) % 12, (base_pos + 10) % 12]
		else:
			chord_tone_list = [base_pos, (base_pos + 3) % 12, (base_pos + 6) % 12, (base_pos + 9) % 12]
		return (chord_tone_list, scale)
	
	def get_chord_interpretation_list_list_from_melody_and_chord_list(self, note_set_list, chord_str_list):
		if len(chord_str_list) != len(note_set_list):
			return []
		chord_interpretation_list_list = self.get_chord_interpretation_list_list_for_melody(note_set_list, False)
		for c_dic_i, c_dic_v in enumerate(chord_interpretation_list_list):
			temp_list = []
			if type(chord_str_list[c_dic_i]) is str:
				pos1, type1 = self.chord_str_to_tpl(chord_str_list[c_dic_i])
			else:
				(pos1, type1) = chord_str_list[c_dic_i]
			for int_i, int_v in enumerate(c_dic_v):
				pos2 = self.get_chord_root_pos(int_v[0])
				type2 = int_v[0][3]
				if pos1 == pos2 and type1 == type2:
					temp_list.append(int_v)
			chord_interpretation_list_list[c_dic_i] = temp_list
		return chord_interpretation_list_list

	def get_random_chord_str_list(self, chord_str_list, change_rate = 1.0):
		arr = []
		for key in range(12):
			for chord_type in range(1, setting.CHORD_TYPE_COUNT + 1):
				arr.append((key, chord_type))
		ret = []
		for i in chord_str_list:
			if random.uniform(0, 1) <= change_rate:
				ret.append(random.choice(arr))
			else:
				ret.append(i)
		return ret
