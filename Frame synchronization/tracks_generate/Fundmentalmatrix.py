#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

human_re_id_file_path_left = r'D:\Praktikum\openvino_output\data1.txt'
human_re_id_file_path_right = r'D:\Praktikum\openvino_output\data2.txt'

open_pose_path_left = r'D:\Praktikum\Openpose\Keypoints\Keypoints1'
open_pose_path_right = r'D:\Praktikum\Openpose\Keypoints\Keypoints2'

openpose_output_left = r'D:\Praktikum\Openpose\Output\output1'
openpose_output_right = r'D:\Praktikum\Openpose\Output\output2'

left_image_path = r'D:\Praktikum\Openpose\Input\data1'
right_image_path = r'D:\Praktikum\Openpose\Input\data2'

left_open_pose_path = r'D:\Praktikum\Openpose\Output\output1'
right_open_pose_path =r'D:\Praktikum\Openpose\Output\output2'


def get_number_frames_and_position(file_path):
	# read the openvino file and get the information about the bounding box
	# (re_id and the center point position) and the frame name included
	frame_id = []
	final_list = []

	with open(file_path) as fl:
		content = fl.readlines()
		for i in range(len(content)):
			# frame id
			value_frame_id = content[i].split(' ')[0]
			# human id
			value_human_id = content[i].split(' ')[1]
			# position
			value_top_left_u = content[i].split(' ')[2]
			value_top_left_v = content[i].split(' ')[3]
			value_box_size_w = content[i].split(' ')[4]
			value_box_size_h = content[i].split(' ')[5]
			# get the center position of bounding box
			value_x = int(value_top_left_u) + 0.5 * int(value_box_size_w)
			vlaue_y = int(value_top_left_v) + 0.5 * int(value_box_size_h)
			# joint human id and center position
			final_list.append((value_frame_id, (value_human_id, value_x, vlaue_y)))

			if len(frame_id) == 0:
				frame_id.append(value_frame_id)
			else:
				if frame_id[-1] == value_frame_id:
					continue
				else:
					frame_id.append(value_frame_id)
	return final_list, frame_id


def get_information_by_frame_name(original_list, str_frame_id):
	# according to the frame name get the information from openvino
	# file in each frame
	list_information = []
	for i in range(len(original_list)):
		if original_list[i][0] == str_frame_id:
			list_information.append(original_list[i][-1])
	return list_information


def get_all_pose_path(left_file_path, right_file_path):
	# the openpose path only give till the folder, so that we need to
	# traverse all the file path in this folder
	left_file_path_list = []
	right_file_path_list = []

	# below we can get the file name, but not a completed path
	# (下面这个可以按照文件名字的顺序，输出文件名列表，但是只是在文件中的文件名，不是完整的)
	left_files = sorted(os.listdir(left_file_path))
	right_files = sorted(os.listdir(right_file_path))

	# to get the completed path of all openpose file
	# (得到完整路径)
	for i in range(len(left_files)):
		str_name_left = open_pose_path_left + '/' + left_files[i]
		left_file_path_list.append(str_name_left)

		str_name_right = open_pose_path_right + '/' + right_files[i]
		right_file_path_list.append(str_name_right)

	# return all the json path
	# (返回完整json路径)
	return left_file_path_list, right_file_path_list


def read_open_pose_file(file_path):
	# read the json file (openpose file)
	# return two matrix, the 8-th points position and all keypoints position
	# according to the body25 structure distribution, 8-th almost the center point of body
	# 8-th point position we will later use to match the bounding box
	use_partnumber_bodymodel = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13]
	use_pointnumber_bodymodel = []
	for i in use_partnumber_bodymodel:
		use_pointnumber_bodymodel.append(i * 3)
		use_pointnumber_bodymodel.append(i * 3 + 1)
		use_pointnumber_bodymodel.append(i * 3 + 2)
	with open(file_path) as f:
		data = json.load(f)
	all_key_points = []
	use_key_points = []
	for points in data['people']:
		# 'people' is the key word that we read from the json
		# VERY IMPORTANT：check the json file before use it ！
		# that means if the output changed, key word might be changed
		a = points['pose_keypoints_2d']
		# 'pose_keypoints_2d' is also a key word, same as 'people'
		# for details, see the explanation above
		all_key_points = all_key_points + [a]
		temp_a = []
		for i in use_pointnumber_bodymodel:
			temp_a.append(a[i])
		use_key_points = use_key_points +[temp_a]

	(row, col) = np.shape(all_key_points)
	all_key_points = np.reshape(all_key_points, (row, col))

	(row, col) = np.shape(use_key_points)
	use_key_points = np.reshape(use_key_points, (row, col))

	center_points_open_pose = []
	for i in range(row):
		# select MidHip poistion to represent the openpose output people box center
		center_points_open_pose.append(all_key_points[i][24:26])

	center_points_open_pose = np.reshape(center_points_open_pose, (row, 2))
	return center_points_open_pose, use_key_points

def sameid_open_pose_output(file_path,same_id_openpose):

	same_id_points = []

	with open(file_path) as f:
		data = json.load(f)
	all_key_points = []
	use_key_points = []
	for points in data['people']:
		# 'people' is the key word that we read from the json
		# VERY IMPORTANT：check the json file before use it ！
		# that means if the output changed, key word might be changed
		a = points['pose_keypoints_2d']
		# 'pose_keypoints_2d' is also a key word, same as 'people'
		# for details, see the explanation above
		all_key_points = all_key_points + [a]
		temp_a = []
		for i in use_pointnumber_bodymodel:
			temp_a.append(a[i])
		use_key_points = use_key_points +[temp_a]


def get_best_correspondences(list_m, list_n):
	# generally openpose get more information as openvino
	# for example, one frame picture include 5 person,
	# normally openpose will get 5 skeleton output
	# but in openvino it may get only 3 or 4 bounding box
	# so the list_m represents openpose, list_n represents openvino
	# m > n
	m = len(list_m)
	n = len(list_n)
	'''
	# for test
	num = 6
	path_openpose_output =  r'D:\Praktikum\Openpose\Output\output1'
	img_num = str('%06d_rendered.png' % num)
	img_path = path_openpose_output + "\\" + img_num
	img_Mat = cv.imread(img_path)

	plt.imshow(img_Mat)
	row, col = list_m.shape
	for i in xrange(row):
		x = list_m[i][0]
		y = list_m[i][1]
		plt.plot(x, y, 'r*')

	for i in xrange(len(list_n)):
		x = list_n[i][1]
		y = list_n[i][2]
		plt.plot(x, y, 'k+')
	#plt.savefig("examples_%s_%s.png" % (k, num))
	#plt.close()
	'''
	list_m2n = []
	list_m2m = []

	for i in range(m):
		for j in range(n):
			# we use the manhattan distance, other distance method also can be used
			distance = abs(list_m[i][0] - list_n[j][1]) + abs(list_m[i][1] - list_n[j][2])
			# value = format(distance, '.2f')
			list_m2n.append(distance)
		min_value = min(list_m2n)

		index_j = list_m2n.index(min_value)
		index_i = i

		#index i represent the sequence of people in openpose json file
		#index j represent the id in openvino
		list_m2m.append([min_value, (index_i, int(list_n[index_j][0]))])
		list_m2n = []

	temp_list = sorted(list_m2m, key=lambda value: value[0])[:n]
	for i in range(len(temp_list)):
		temp_list[i][0] = format(temp_list[i][0], '.2f')
	return temp_list


def get_all_image_path(left_image_file_path, right_image_file_path):
	# todo: write a more general function, combine the 2 function in 1
	# almost same as get_all_pose_path
	left_image_file_path_list = []
	right_image_file_path_list = []

	# 下面这个可以按照文件名字的顺序，输出文件名列表，但是只是在文件中的文件名，不是完整的
	left_image_files = sorted(os.listdir(left_image_file_path))
	right_image_files = sorted(os.listdir(right_image_file_path))

	# 得到完整路径名
	for i in range(len(left_image_files)):
		left_str_name = left_image_path + '/' + left_image_files[i]
		left_image_file_path_list.append(left_str_name)

	for i in range(len(right_image_files)):
		right_str_name = right_image_path + '/' + right_image_files[i]
		right_image_file_path_list.append(right_str_name)

	# 返回完整json路径
	return left_image_file_path_list, right_image_file_path_list


def create_correspondence_points_list(path_left, path_right, left_center_points_human_reid, frameid_list_left, right_center_points_human_reid, frameid_list_right):
	# according to the same re_id to get the correspondence keypoints from the openpose
	correspondences_points_matrix_left_dict = {}
	correspondences_points_matrix_right_dict = {}

	for num_index in range(len(frame_id_list_left)):
		temp_path_left, temp_path_right = get_all_pose_path(path_left, path_right)
		temp_eight_left, temp_use_keypoints_left = read_open_pose_file(temp_path_left[num_index])
		temp_eight_right, temp_use_keypoints_right = read_open_pose_file(temp_path_right[num_index])

		temp_best_left = best_left_dict[frame_id_list_left[num_index]]
		temp_best_right = best_right_dict[frame_id_list_right[num_index]]

		length_left = len(temp_best_left)
		length_right = len(temp_best_right)

		correspondences_points_matrix_left = []
		correspondences_points_matrix_right = []
		for i in range(length_left):
			for j in range(length_right):
				temp_reid_index_left = temp_best_left[i][1][1]
				temp_reid_index_right = temp_best_right[j][1][1]
				temp_pose_index_left = temp_best_left[i][1][0]
				temp_pose_index_right = temp_best_right[j][1][0]
				if temp_reid_index_left == temp_reid_index_right:
					correspondences_points_matrix_left.append(temp_use_keypoints_left[temp_pose_index_left])
					correspondences_points_matrix_right.append(temp_use_keypoints_right[temp_pose_index_right])
				pass


		correspondences_points_matrix_left_dict[
			'{}'.format(frame_id_list_left[num_index])] = correspondences_points_matrix_left
		correspondences_points_matrix_right_dict[
			'{}'.format(frame_id_list_right[num_index])] = correspondences_points_matrix_right

	return correspondences_points_matrix_left_dict, correspondences_points_matrix_right_dict


def get_all_correspondence_points(correspondence_dict_left, correspondence_dict_right, frameid_list_left, frameid_list_right):

	correspondence_points_List_left = []
	correspondence_points_List_right = []
	num_correspondence_points = 0
	for frameid_num in range(len(frameid_list_left)):
		if len(correspondence_dict_left[frameid_list_left[frameid_num]]):
			temp_r, temp_c = np.shape(correspondence_dict_left[frameid_list_left[frameid_num]])
			temp_c = temp_c/3
			temp_final_left = []
			temp_final_right = []

			for k in range(temp_r):
				for l in range(int(temp_c)):
					temp_final_left.append(correspondence_dict_left[frame_id_list_left[frameid_num]][k][l*3:l*3+2])
					temp_final_right.append(correspondence_dict_right[frame_id_list_right[frameid_num]][k][l*3:l*3+2])

			temp_final_left = np.array(temp_final_left)
			temp_final_right = np.array(temp_final_right)
			# TODO  solve the situation when temp_final_left not equal temp_final_right
			row = temp_final_left.shape[0]
			num_correspondence_points = num_correspondence_points + row

			correspondence_points_List_left.append(temp_final_left)
			correspondence_points_List_right.append(temp_final_right)


		else:
			pass

	return num_correspondence_points, correspondence_points_List_left, correspondence_points_List_right


def get_all_pose_result_path(left_pose_path, right_pose_path):
	# todo: write a more general function, combine the 2 function in 1
	# almost same as get_all_pose_path
	left_pose_path_list = []
	right_pose_path_list = []

	# 下面这个可以按照文件名字的顺序，输出文件名列表，但是只是在文件中的文件名，不是完整的
	left_image_files = sorted(os.listdir(left_pose_path))
	right_image_files = sorted(os.listdir(right_pose_path))

	# 得到完整路径名
	for i in range(len(left_image_files)):
		left_str_name = left_open_pose_path + '/' + left_image_files[i]
		left_pose_path_list.append(left_str_name)

	for i in range(len(right_image_files)):
		right_str_name = right_open_pose_path + '/' + right_image_files[i]
		right_pose_path_list.append(right_str_name)

	# 返回完整json路径
	return left_pose_path_list, right_pose_path_list

def points_List2Mat(points_List,num_Mat):
	temp = np.zeros((num_Mat,2))
	count = 0
	for i in xrange(len(points_List)):
		temp_points_Mat = points_List[i]
		row = temp_points_Mat.shape[0]
		temp[count : count+row] = temp_points_Mat
		count += row
	return temp

def output_points_txt(Mat, num_Mat):
	Res = open('tracks.txt', 'a')
	Res.write('%s' % num_Mat)
	for i in xrange(num_Mat):
		temp = Mat[i]
		Res.write(' %d %f %f' % (i + 1, temp[0], temp[1]))
	Res.write('\n')
	Res.close()

def all_points_same_reid(frame_ID_list, best_dict):
	best_stable_reid_correspondence = []
	for frameid_num in xrange(len(frame_ID_list)):
		i = frame_ID_list[frameid_num]
		temp = best_dict[i]
		for j in xrange(len(temp)):
			temp_id_fit_list = temp[j]
			if temp_id_fit_list[1][1] == 2:
				temp_list = [frameid_num+1, temp_id_fit_list[1][0]]
				best_stable_reid_correspondence.append(temp_list)
	return best_stable_reid_correspondence

def same_id_correspondence_points_Mat(same_id_openpose, path_openpose_file, path_openpose_output, filepath, setnum=1  , offset=0):
	use_partnumber_bodymodel = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13]
	#use_partnumber_bodymodel = [2]
	use_pointnumber_bodymodel = []
	for i in use_partnumber_bodymodel:
		temp_sequence = [i* 3, i*3+1, i*3+2]
		use_pointnumber_bodymodel.append(temp_sequence)
	for k in xrange(len(use_pointnumber_bodymodel)):
		Mat_list = []
		partnumber_correspondence = use_pointnumber_bodymodel[k]
		#for i in xrange(len(same_id_openpose)):
		for i in xrange(100):
				num = same_id_openpose[i][0]
				s = str ('%06d_keypoints.json' %num)
				file = path_openpose_file + "\\"+ s
				f = open(file)
				temp = json.loads(f.read())
				id_openpose = same_id_openpose[i][1]
				temp_Mat = temp['people'][id_openpose]['pose_keypoints_2d']
				# for test
				if temp_Mat[partnumber_correspondence[2]]:
					temp_points = [num, temp_Mat[partnumber_correspondence[0]], temp_Mat[partnumber_correspondence[1]]]

					'''
					x = temp_points[1]
					y = temp_points[2]
					img_num = str('%06d_rendered.png' % num)
					img_path = path_openpose_output + "\\" + img_num
					img_Mat = cv.imread(img_path)

					plt.imshow(img_Mat)
					plt.plot (x,y,'r*')
					plt.savefig("examples_%s_%s_%s.png" % (k,num,setnum) )
					plt.close()
					'''

					Mat_list.append(temp_points)
				'''
				x = np.zeros(len(Mat_list))
				y = np.zeros(len(Mat_list))
				for i in xrange(len(Mat_list)):
					x[i] = Mat_list[i][1]
					y[i] = Mat_list[i][2]
				plt.imshow(img_Mat)
				plt.plot(x, y, 'r*')
				plt.show()
				plt.savefig("examples_%s.png" % i)
				'''
		#'''
		tracks_plot_x = np.zeros(len(Mat_list))
		tracks_plot_y = np.zeros(len(Mat_list))
		for i in xrange(len(Mat_list)):
			tracks_plot_x[i] = Mat_list[i][1]
			tracks_plot_y[i] = Mat_list[i][2]
		plt.plot(tracks_plot_x, tracks_plot_y)
		plt.plot(tracks_plot_x,tracks_plot_y,'r*')
		plt.axis((0,1920,0,1200))
		ax = plt.gca()
		ax.xaxis.set_ticks_position('top')
		ax.invert_yaxis()
		plt.savefig("tracks_%s_%s_100.png" %(k,setnum))
		plt.close()
		#'''
		Res = open(filepath, 'a')
		num_Mat = len(Mat_list)
		count = 0
		for i in xrange(num_Mat):
			temp = Mat_list[i]
			if int(temp[0]) <= offset :
				count +=1
		temp_num = num_Mat - count
		Res.write('%s' % temp_num)
		for i in xrange(num_Mat):
			temp = Mat_list[i]
			if int(temp[0]) > offset:
				Res.write(' %d %f %f' % (temp[0]-offset, temp[1], temp[2]))
		Res.write('\n')
		Res.close()

	return Mat_list



best_left_dict = {}
best_right_dict = {}
left_center_points_human_re_id, frame_id_list_left = get_number_frames_and_position(human_re_id_file_path_left)
right_center_points_human_re_id, frame_id_list_right = get_number_frames_and_position(human_re_id_file_path_right)
num_frames = len(frame_id_list_left)
left_json_file_path, right_json_file_path = get_all_pose_path(open_pose_path_left, open_pose_path_right)
left_all_image_path, right_all_image_path = get_all_image_path(left_image_path, right_image_path)
left_open_pose_result_path, right_open_pose_result_path = get_all_pose_result_path(left_open_pose_path, right_open_pose_path)
# here use a loop, to get the list_m from the open_pose file
# (在这里设置循环 从open_pose产生的文件中得到对应的list_m)
# and the list_n from the human reID
# (和来自human reID的list_n)

for INDEX in range(num_frames):
	#INDEX = 5
	l_open_file_path = left_json_file_path[INDEX]
	r_open_file_path = right_json_file_path[INDEX]

	left_m, use_key_points_left = read_open_pose_file(l_open_file_path)
	right_m, use_key_points_right = read_open_pose_file(r_open_file_path)

	left_n = get_information_by_frame_name(left_center_points_human_re_id, frame_id_list_left[INDEX])
	right_n = get_information_by_frame_name(right_center_points_human_re_id, frame_id_list_right[INDEX])

	best_left = get_best_correspondences(left_m, left_n)
	best_right = get_best_correspondences(right_m, right_n)

	best_left_dict['{}'.format(frame_id_list_left[INDEX])] = best_left
	best_right_dict['{}'.format(frame_id_list_right[INDEX])] = best_right




a, b = create_correspondence_points_list(open_pose_path_left, open_pose_path_right, left_center_points_human_re_id, frame_id_list_left, right_center_points_human_re_id, frame_id_list_right)
same_id_openpose_left = all_points_same_reid(frame_id_list_left, best_left_dict)
same_id_openpose_right = all_points_same_reid(frame_id_list_right, best_right_dict)

num_correspondence_points, correspondence_points_left, correspondence_points_right = get_all_correspondence_points(a, b, frame_id_list_left, frame_id_list_right)

correspondence_points_left_Mat = points_List2Mat(correspondence_points_left, num_correspondence_points)
correspondence_points_right_Mat = points_List2Mat(correspondence_points_right, num_correspondence_points)

tracks_Mat = 0
#Res = open('tarcks.txt', 'w')
#Res.close()
#output_points_txt(correspondence_points_left_Mat, num_correspondence_points)
#output_points_txt(correspondence_points_right_Mat, num_correspondence_points)

test = same_id_correspondence_points_Mat(same_id_openpose_left, open_pose_path_left, openpose_output_left, 'tracks.txt')
test2 = same_id_correspondence_points_Mat(same_id_openpose_right, open_pose_path_right, openpose_output_right, 'tracks.txt', setnum = 2)
f, mask = cv.findFundamentalMat(correspondence_points_left_Mat, correspondence_points_right_Mat, method=cv.RANSAC, ransacReprojThreshold=1, confidence=0.99)

print f
#print(left_open_pose_result_path[0])


