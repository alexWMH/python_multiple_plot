#!/usr/bin/env python3.9

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.patches as patches
import numpy as np
import sys
import plotly.express as px
from tqdm import tqdm, trange
mpl.rcdefaults()

# set path
folder_path = sys.argv[1]
# get csv data
# csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# for file_name in csv_files:

### read species data 

df = pd.read_csv(folder_path, sep = "\t")

for col  in df.columns[1:] :
	smpl = df[["taxonomy", col]]
	print (col + " Processing... \n")
#### bar plot ####

	#df = pd.read_csv(os.path.join(folder_path, file_name))
	unclassified = smpl[smpl.iloc[:, 0] == 'unclassified']
	SUM = smpl[smpl.iloc[:, 0] == 'SUM']
	Lactob = smpl[smpl.iloc[:, 0] == 'Lactobacillus']
	smpl = smpl[smpl.iloc[:, 0] != 'unclassified']
	smpl = smpl[smpl.iloc[:, 0] != 'others']
	smpl = smpl[smpl.iloc[:, 0] != 'SUM']
	smpl_sorted = smpl.sort_values(smpl.columns[1], ascending = True)
	bottom_20 = smpl_sorted.tail(20)
	
	#print(bottom_20)

	
	
	smpl_sorted = smpl.sort_values(smpl.columns[1], ascending = False)
	top_20 = smpl_sorted.head(20)
	
	#print(top_20)


	
	others_total = smpl_sorted.iloc[20:, 1].sum()
	others= pd.DataFrame([['others', others_total]], columns=smpl.columns)
	

	#print(others)
	print("\n")


	last_2 = smpl_sorted.tail(2)
	others_total = smpl_sorted.iloc[20:, 1].sum()
	others= pd.DataFrame([['others', others_total]], columns = smpl.columns)
	result_df = pd.concat([others, unclassified, bottom_20], ignore_index=True)
	result_df = result_df.set_index(smpl.columns[0])
	fig = plt.figure(figsize=(4,6)) 
	ax = result_df.plot(kind="barh", ax=fig.add_subplot(111))
	plt.xlim(0, 100) 
	plt.xticks(range(0, 101, 10))
	for i in ax.patches:
		plt.text(i.get_width()+0.3, i.get_y()+0.1, \
			str(round((i.get_width()), 3)), fontsize=10, color='dimgrey')

# grep lactobacillus 
	
	lactobacillus_value = smpl.loc[smpl[smpl.columns[0]] == "Lactobacillus", smpl.columns[1]].values[0]

	
# find wether lactobicullus are in top 20 bacteria 

	if lactobacillus_value not in result_df[smpl.columns[1]].values[:20] and lactobacillus_value <14:
		ax.text(1.2, 0.8, f'Lactobacillus: {Lactob.iloc[0, 1]:.3f}', transform=ax.transAxes, fontsize=12)
		ax.text(1.7, 0.75, "(Outside of the top 20 ranked microbial taxa )", transform=ax.transAxes, fontsize=12, ha='center')
	else:
		ax.text(1.2, 0.8, f'Lactobacillus: {Lactob.iloc[0, 1]:.3f}', transform=ax.transAxes, fontsize=12)
		if lactobacillus_value > 15:
			print("Value of Lactobacillus 15%\u2265, only for reference")
			ax.text(1.4, 0.75, "(Value of Lactobacillus 15%\u2265, only for reference)", transform=ax.transAxes, fontsize=12, ha='center')

	#file_name, ext = os.path.splitext(file_name)
	#file_name = file_name[:10]
	plt.title(col + '-RS - percentage')
	plt.legend(["percentage"], fontsize=12, loc='upper right', bbox_to_anchor=(1.6, 1) )
 	
	#plt.show()
	plt.savefig(col + "_bar.png", bbox_inches='tight', dpi=300)
	plt.close()


#### pie chart ####
	
	unclassified = smpl[smpl.iloc[:, 0] == 'unclassified']	
	result_df = pd.concat([others, unclassified, bottom_20], ignore_index=True)

	fig, ax = plt.subplots(figsize=(10, 10))

	data = result_df.iloc[:, 1]
	labels = result_df.iloc[:, 0]
	colors = ['#d2d3d4', '#28a745','#ffc107', '#fd7e14','#c1c7c9','#a3b8bf','#007bff', '#6f42c1', 
			  '#e83e8c', '#17a2b8','#c5ff07','#07eaff', '#07b5ff','#077bff','#ff077f','#7b07ff',
			  '#ff6207','#ffda07','#9c07ff','#07a8ff','#5e82b8','#dc3545']
	explode = [0.03] * len(labels)
	
	wedges, _ = ax.pie(data, explode=explode, labels=labels, colors=colors, wedgeprops={'width': 0.7}, startangle=90, rotatelabels = 270)
#	kw=dict(xycoords='data',textcoords='data',arrowprops=dict(arrowstyle='-'),zorder=0,va='center')	
	for i, wedge in enumerate(wedges):
		angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
		x = wedge.r * 0.7 * np.cos(np.deg2rad(angle))
		y = wedge.r * 0.7 * np.sin(np.deg2rad(angle))
#		horizontalalignment={-1:"right",1:"left"}[int(np.sign(x))]
#		connectionstyle="angle,angleA=0,angleB={}".format(angle)
#		kw["arrowprops"].update({"connectionstyle":connectionstyle})
#		ax.annotate(new_labels[i],xy=(x, y),xytext=(1.35*np.sign(x),1.4*y),
#		horizontalalignment=horizontalalignment,**kw)		
		if angle > 540:
			angle -= 540
		ax.text(x, y, f'{data[i]:.2f}', ha='center', va='center',rotation=angle)
	
	#file_name = file_name[:8]

	plt.title(col + '-RS - percentage', loc='right', pad=20, fontsize=18)
	plt.legend(title='taxonomy', labels=labels, loc='upper right',  fontsize=14, title_fontsize=16, bbox_to_anchor=(1.5, 0.9))
	# file_name, ext = os.path.splitext(file_name)
	
	plt.savefig(col + "_pie.png", bbox_inches='tight', dpi=300)
	plt.close()

##### F/B ratio bar plot 

# open phylum file 
folder_path = sys.argv[2]
df = pd.read_csv(folder_path, sep = "\t") 
for col in df.columns[1:] :

# from all phylum data grep sample colum
	
	a = df[["taxonomy", col]]

# grep Firmicutes and Bacteroidetes and merge to result  

	Fir = a[a.iloc[:,0] == "Firmicutes"]
	Bac = a[a.iloc[:,0] == "Bacteroidetes"]
	result = pd.concat([Fir,Bac])
	
# calculate F/B ratio
	
	ratio = Fir.iat[0,1]/Bac.iat[0,1]
	
# plot 
	
	fig = plt.figure(figsize=(6,2))
	ax = result.plot("taxonomy", col, kind="barh", ax=fig.add_subplot(111))
	
	plt.xlim(0, 100)
	plt.xticks(range(0, 101, 10))
	
	for i in ax.patches:
		plt.text(i.get_width()+0.3, i.get_y()+0.1,str(round((i.get_width()), 3)), fontsize=10, color='dimgrey')
	ax.text(0.65, 0.7, f'F/B Ratio: {ratio:0.3f}', transform=ax.transAxes, fontsize=12)			# {} input calculate value, :0.3f means Number of decimal places
	plt.title(col + '-RS - F/B ')
	plt.legend(["percentage"], fontsize=12, loc='upper right',bbox_to_anchor=(1.2, 1.3))
	
	plt.savefig(col + "_ratio.png", bbox_inches='tight', dpi=300)
	plt.close()

### F/B ratio  plot 

	Firmicutes_sum = Fir.iloc[:, 1:].sum().sum()
	Bacteroidetes_sum = Bac.iloc[:, 1:].sum().sum()
	total_sum = Firmicutes_sum + Bacteroidetes_sum
	Firmicutes_perc = Firmicutes_sum / total_sum * 100
	Bacteroidetes_perc = Bacteroidetes_sum / total_sum * 100

# plot

	fig, ax = plt.subplots(figsize=(4, 2))
	plt.ylim([-0.5, 1])
	plt.grid(axis='x',color='#d3d8db',zorder=1)
	plt.barh(y=0, width=Firmicutes_perc, color='#a7c3cf', zorder=2)
	plt.barh(y=0, width=Bacteroidetes_perc, left=Firmicutes_perc, color='#f7876a', zorder=2)
	plt.text(Firmicutes_perc / 2, 0, str(round(Firmicutes_perc, 2)) + '%', ha='center', va='center', color='black',zorder=3)
	plt.text(Bacteroidetes_perc / 2 + Firmicutes_perc, 0, str(round(Bacteroidetes_perc, 2)) + '%', ha='center', va='center', color='black', zorder=3)
	plt.title(col + '-RS - F/B ', weight='bold')
	plt.legend(['Firmicutes', 'Bacteroidetes'], bbox_to_anchor=(1.1, 0.9))
	
# set no frame

	plt.box(False)

# set range of x and y

	plt.yticks([0], [''])
	plt.xlim([0, 101])
	
# set fig size and margin 

	fig.set_size_inches([6, 3])
	fig.subplots_adjust(left=0.2, bottom=0.2, right=0.95, top=0.8)

	plt.savefig(col + "_perc.png", bbox_inches='tight', dpi=300)
	plt.close()

