# coding: utf-8
# 2020.06.24

import heapq
import math
import util
import setting
class TPS:
	
	def __init__(self):
		self.coef_i = 1.0
		self.coef_j = 1.0
		self.coef_k = 1.0
		self.stored_distances = {}
	
	get_distance_dic = {'A': 0, 'A#': 1, 'Bb': 1, 'B': 2, 'Cb': 2, 'C': 3, 'B#': 3, 'C#': 4, 'Db': 4, 'D': 5, 'D#': 6, 'Eb': 6, 'E': 7, 'Fb': 7, 'F': 8, 'E#': 8, 'F#': 9, 'Gb': 9, 'G': 10, 'G#': 11, 'Ab': 11}
	def get_distance(self, keynote_1, b_major_1, degree_1, keynote_2, b_major_2, degree_2):
		#dic = {'A': 0, 'A#': 1, 'Bb': 1, 'B': 2, 'Cb': 2, 'C': 3, 'B#': 3, 'C#': 4, 'Db': 4, 'D': 5, 'D#': 6, 'Eb': 6, 'E': 7, 'Fb': 7, 'F': 8, 'E#': 8, 'F#': 9, 'Gb': 9, 'G': 10, 'G#': 11, 'Ab': 11}
		keypos_1 = self.get_distance_dic[keynote_1]
		keypos_2 = self.get_distance_dic[keynote_2]
		if b_major_1:
			scale_1 = setting.SCALE_MAJOR
		else:
			scale_1 = setting.SCALE_NATURAL_MINOR
		if b_major_2:
			scale_2 = setting.SCALE_MAJOR
		else:
			scale_2 = setting.SCALE_NATURAL_MINOR
		return self.get_distance2(keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2)
	
	def get_distance2(self, keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2, b_close = False):
		if (keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2) in self.stored_distances:
			return self.stored_distances[(keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2)]
		b_major_1 = (scale_1 == setting.SCALE_MAJOR)
		b_major_2 = (scale_2 == setting.SCALE_MAJOR)
		if b_close or self.is_close_key(keypos_1, b_major_1, keypos_2, b_major_2):
			sum1 = self.get_region_distance(keypos_1, b_major_1, keypos_2, b_major_2)
			sum2 = self.get_chord_distance(keypos_1, degree_1, keypos_2, degree_2)
			sum3 = self.get_basicspace_distance(keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2)
			return sum1 * util.sigmoid(self.coef_i) + sum2 * util.sigmoid(self.coef_j) + sum3 * util.sigmoid(self.coef_k)
		else:
			sum = self.get_distance2(keypos_1, scale_1, degree_1, keypos_1, scale_1, 1, True)
			reached = {(keypos_1, b_major_1): 0}
			for i in range(100):
				k1 = min(reached, key=reached.get)
				v1 = reached[k1]
				if (keypos_2, b_major_2) in reached and reached[(keypos_2, b_major_2)] == v1:
					sum += v1
					break
				close_key_list = self.get_close_key_list(k1[0], k1[1], True, reached)
				reached[k1] = 99999
				for k2, v2 in close_key_list.items():
					if (not k2 in reached) or (reached[k2] != 99999 and reached[k2] > v1 + v2):
						reached[k2] = v1 + v2
			sum += self.get_distance2(keypos_2, scale_2, 1, keypos_2, scale_2, degree_2, True)
		self.stored_distances[(keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2)] = sum
		return sum
	
	def is_close_key(self, keypos_1, b_major_1, keypos_2, b_major_2):
		if (keypos_1, b_major_1) == (keypos_2, b_major_2):
			return True
		else:
			close_key_list = self.get_close_key_list(keypos_1, b_major_1)
			for k in close_key_list:
				if (keypos_2, b_major_2) == (k[0], k[1]):
					return True
			return False

	def get_close_key_list(self, keypos, b_major, b_with_distance = False, reached = []):
		ret = {(keypos, not b_major): -1, ((keypos + 7) % 12, b_major): -1, ((keypos + 5) % 12, b_major): -1};
		if b_major:
			ret[((keypos - 3) % 12, not b_major)] = -1
			ret[((keypos + 7 - 3) % 12, not b_major)] = -1
			ret[((keypos + 5 - 3) % 12, not b_major)] = -1
		else:
			ret[((keypos + 3) % 12, not b_major)] = -1
			ret[((keypos + 7 + 3) % 12, not b_major)] = -1
			ret[((keypos + 5 + 3) % 12, not b_major)] = -1
		if b_with_distance:
			for k in ret:
				if k not in reached or reached[k] != 99999:
					scale_1 = setting.SCALE_MAJOR if b_major else setting.SCALE_NATURAL_MINOR
					scale_2 = setting.SCALE_MAJOR if k[1] else setting.SCALE_NATURAL_MINOR
					ret[k] = self.get_distance2(keypos, scale_1, 1, k[0], scale_2, 1, True)
		return ret

	get_region_distance_arr = [9, 2, 7, 0, 5, 10, 3, 8, 1, 6, 11, 4]
	def get_region_distance(self, keypos_1, b_major_1, keypos_2, b_major_2):
		modpos_1 = keypos_1
		if not b_major_1:
			modpos_1 = (modpos_1 + 3) % 12
		modpos_2 = keypos_2
		if not b_major_2:
			modpos_2 = (modpos_2 + 3) % 12
		mod = (self.get_region_distance_arr[modpos_1] - self.get_region_distance_arr[modpos_2]) % 12;
		return min(mod, 12 - mod)

	keypos_to_digree = {0: 0, 2: 1, 3: 2, 4: 2, 5: 3, 7: 4, 8: 5, 9: 5, 10: 6}
	get_chord_distance_arr = [0, 5, 3, 1, 6, 4, 2]
	def get_chord_distance(self, keypos_1, degree_1, keypos_2, degree_2):
		mod = (self.get_chord_distance_arr[((degree_2 + self.keypos_to_digree[(keypos_2 - keypos_1) % 12]) % 7) - (degree_1 % 7)]) % 7
		return min(mod, 7 - mod)

	scales = {
		setting.SCALE_MAJOR:          [0, 2, 4, 5, 7, 9, 11],
		setting.SCALE_NATURAL_MINOR:  [0, 2, 3, 5, 7, 8, 10],
		setting.SCALE_HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],
		setting.SCALE_MELODIC_MINOR:  [0, 2, 3, 5, 7, 9, 11]
	}
	def get_basicspace_distance(self, keypos_1, scale_1, degree_1, keypos_2, scale_2, degree_2):
		bs1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		bs2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		scale1 = self.scales[scale_1]
		scale2 = self.scales[scale_2]
		bs1[(scale1[0] + keypos_1) % 12] += 1
		bs1[(scale1[1] + keypos_1) % 12] += 1
		bs1[(scale1[2] + keypos_1) % 12] += 1
		bs1[(scale1[3] + keypos_1) % 12] += 1
		bs1[(scale1[4] + keypos_1) % 12] += 1
		bs1[(scale1[5] + keypos_1) % 12] += 1
		bs1[(scale1[6] + keypos_1) % 12] += 1
		bs2[(scale2[0] + keypos_2) % 12] += 1
		bs2[(scale2[1] + keypos_2) % 12] += 1
		bs2[(scale2[2] + keypos_2) % 12] += 1
		bs2[(scale2[3] + keypos_2) % 12] += 1
		bs2[(scale2[4] + keypos_2) % 12] += 1
		bs2[(scale2[5] + keypos_2) % 12] += 1
		bs2[(scale2[6] + keypos_2) % 12] += 1
		bs1[(scale1[(0 + degree_1 - 1) % 7] + keypos_1) % 12] += 3
		bs1[(scale1[(2 + degree_1 - 1) % 7] + keypos_1) % 12] += 1
		bs1[(scale1[(4 + degree_1 - 1) % 7] + keypos_1) % 12] += 2
		bs2[(scale2[(0 + degree_2 - 1) % 7] + keypos_2) % 12] += 3
		bs2[(scale2[(2 + degree_2 - 1) % 7] + keypos_2) % 12] += 1
		bs2[(scale2[(4 + degree_2 - 1) % 7] + keypos_2) % 12] += 2
		sum = 0
		for i in range(12):
			sum += max(0, bs2[i] - bs1[i])
		return sum
