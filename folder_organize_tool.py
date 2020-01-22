# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:28:37 2019

@author: zona8001
"""

import os
import shutil
import pandas as pd
import time
import numpy as np
import pdb

pd.set_option('display.width', None) # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)
def folder_file(item_name):
	'''
	identify file name, suffix for a string.
	if string don't have suffix, then identify as folder
	return (file_name, file_suffix, file_type) for later string split. 
	'''
	#item_name = '__MACOSX'
	file_name,file_suffix = os.path.splitext(item_name)
	if file_suffix=='':
		file_type='folder'
	else:
		file_type='file'
	return file_name,file_suffix,file_type

def update_log(mess_folder):
	file_list = pd.DataFrame({'name':os.listdir(mess_folder)})
	file_list['file_key'] = file_list['name'].apply(lambda x: folder_file(x))
	file_list['file_name'] = file_list['file_key'].apply(lambda x: x[0])
	file_list['file_suffix'] = file_list['file_key'].apply(lambda x: x[1])
	file_list['file_type'] = file_list['file_key'].apply(lambda x: x[2])
	file_list['file_created'] = file_list['name'].apply(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getctime(os.path.join(mess_folder,x)))))
	file_list['file_modified'] = file_list['name'].apply(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getmtime(os.path.join(mess_folder,x)))))
	file_list.drop(['file_key'],axis=1,inplace=True)
	file_list['file_content'] = ''
	file_list['name_history'] = ''
	file_list['rename_request'] = ''
	file_list['rename_str'] = ''
	file_list['move_request'] =''
	file_list['move_str'] = ''
	file_list['search_label'] = ''
	old_list = pd.read_excel(os.path.join(mess_folder+'folder_file_log.xlsx'),index_col=0)
	updated_list = old_list.append(file_list)
	updated_list = updated_list.drop_duplicates(subset=['name','file_created'])
	#droped_list = old_list[~old_list.name.isin(file_list.name)]
	#new_list = file_list[~file_list.name.isin(old_list.name)]
	return updated_list


def generate_log(mess_folder):
	'''
	if new folder, then generate log file. 
	if not, update log file. (will add in next version).
	'''
	if os.path.exists(os.path.join(mess_folder,'folder_file_log.xlsx')):	
		print('Log file already existed in %s'%mess_folder)
		updated_list = update_log(mess_folder)
		updated_list.to_excel(os.path.join(mess_folder,'folder_file_log.xlsx'))
		print('Update and Fetch lastest log')
	else:
		file_list = pd.DataFrame({'name':os.listdir(mess_folder)})
		file_list['file_key'] = file_list['name'].apply(lambda x: folder_file(x))
		file_list['file_name'] = file_list['file_key'].apply(lambda x: x[0])
		file_list['file_suffix'] = file_list['file_key'].apply(lambda x: x[1])
		file_list['file_type'] = file_list['file_key'].apply(lambda x: x[2])
		file_list['file_created'] = file_list['name'].apply(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getctime(os.path.join(mess_folder,x)))))
		file_list['file_modified'] = file_list['name'].apply(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getmtime(os.path.join(mess_folder,x)))))
		file_list.drop(['file_key'],axis=1,inplace=True)
		file_list['file_content'] = ''
		file_list['name_history'] = ''
		file_list['rename_request'] = ''
		file_list['rename_str'] = ''
		file_list['move_request'] =''
		file_list['move_str'] = ''
		file_list['search_label'] = ''
		file_list.to_excel(os.path.join(mess_folder,'folder_file_log.xlsx'))
		print('New log file has been generated')

def rename_process(rename_items):
	#rename_items = file_list.loc[rename_logic]
	rename_items['old_name'] = rename_items['name']
	rename_items['name'] = rename_items['rename_str']+rename_items['file_suffix']
	if isinstance(rename_items,pd.DataFrame):
		for ii in rename_items.index:
			#pdb.set_trace()
				os.rename(os.path.join(mess_folder,rename_items.loc[ii,'old_name']),os.path.join(mess_folder,rename_items.loc[ii,'name']))
	elif isinstance(rename_items,pd.Series):
		os.rename(os.path.join(mess_folder,rename_items['old_name']),os.path.join(mess_folder,rename_items['name']))
	#rename_items.drop(['old_name'],axis=1,inplace=True)

def move_process(move_items):
	#move_items = file_list.loc[move_logic]
	#pdb.set_trace()
	if isinstance(move_items,pd.DataFrame):
		for ii in move_items.index:
			shutil.move(os.path.join(mess_folder,move_items.loc[ii,'name']),os.path.join(move_items.loc[ii,'move_str'],move_items.loc[ii,'name'])) 
	elif isinstance(move_items,pd.Series):
		shutil.move(os.path.join(mess_folder,move_items['name']),os.path.join(move_items['move_str'],move_items['name'])) 


def rename_move_batch(mess_folder):
	file_list = pd.read_excel(os.path.join(mess_folder+'folder_file_log.xlsx'),index_col=0)
	rename_logic = file_list['rename_request']==1
	print(file_list.loc[rename_logic,['file_name','rename_str','file_content']])
	print('======'*6)
	print('Rename request all correct?')
	rename_confirm = input("TYPE NUMBER TO CONFIRM:\n 0: I need revise rename request and stop whole process \n 1: I need revise rename request, but can go for move request \n 2: all correct \n Here(ONLY 0 OR 1 OR 2):")
	if rename_confirm =='0':
		os._exit(0)
	elif rename_confirm == '1':
		pass
	elif rename_confirm == '2':
		file_list.loc[rename_logic].apply(rename_process,axis=1)
		file_list.loc[rename_logic,'name_history'] = file_list.loc[rename_logic,'file_name']
		file_list.loc[rename_logic,'file_name'] = file_list.loc[rename_logic,'rename_str']
		file_list.loc[rename_logic,'name'] = file_list.loc[rename_logic,'file_name']+file_list.loc[rename_logic,'file_suffix']
		file_list.loc[rename_logic,'rename_request'] = np.nan
	move_logic = file_list['move_request']==1
	print(file_list.loc[move_logic,['move_str','file_name','file_content']])
	print('======'*6)
	print('Move request all correct?')
	move_confirm = input("TYPE NUMBER TO CONFIRM:\n 0: I need revise move request and stop whole process \n 1: all correct \n Here(ONLY 0 OR 1):")
	if move_confirm =='0':
		os._exit(0)
	elif move_confirm == '1':
		file_list.loc[move_logic].apply(move_process,axis=1)
		file_list.drop(list(file_list.loc[move_logic].index),inplace = True)
	file_list.to_excel(os.path.join(mess_folder,'folder_file_log.xlsx'))

if __name__ == '__main__':
	mess_folder = 'C:/Users/zona8001/Downloads/'
	generate_log(mess_folder)
	
	step1_confirm = input("TYPE NUMBER TO CONFIRM:\n 0: stop process \n 1: update log file \n Here(ONLY 0 OR 1):")
	if step1_confirm == '0':
		os._exit(0)
	elif step1_confirm == '1':
		update_log(mess_folder)
		
	step2_confirm = input("TYPE NUMBER TO CONFIRM:\n 0: stop process \n 1: go to rename & move \n Here(ONLY 0 OR 1):")
	if step2_confirm == '0':
		os._exit(0)
	elif step2_confirm == '1':
		rename_move_batch(mess_folder)