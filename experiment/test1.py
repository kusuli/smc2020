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

song_chords, _ = base.load_music_data("./data/fly_me_to_the_moon.txt") # Fly Me to the Moon （34 chords）
#song_chords, _ = base.load_music_data("./data/autumn_leaves.txt") # Autumn Leaves （31 chords）

#obj = base # original
#obj = ext1 # +tetrads, 4 scales
#obj = ext2 # +ε-transition
obj = ext3 # +cadence shortcuts
graph, path_list_gen = obj.get_optimal_path_for_chord_str_list(song_chords, b_noise=False);
#obj.show_path(graph, path_list_gen, 2)
count = 0
for p in path_list_gen:
	count += 1
	if count % 10000 == 0:
		print('\rcount: ', count , end='')
		#break
print('\nnodes: {}, edges: {}, shortest paths: {}'.format(len(graph.nodes), len(graph.edges), count))
