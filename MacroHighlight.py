import os
from xml.etree import ElementTree
import sublime, sublime_plugin

class MacroHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_path = sublime.active_window().folders()[0]
		files = os.listdir(file_path);

		all_data = '\\b(ThisIsMacroList'
		typedef_data = '\\b(ThisIsTypedefList'
		for filename in files:
		    if filename[-2:] == '.h' or filename[-2:] == '.H' or filename[-2:] == '.c' or filename[-4:] == '.cpp':
		        f = open(file_path + '\\' + filename) 
		        lines = f.readlines()

		        for line in lines:
		            data = line.strip().split()
		            if not data:
		                continue
		            if data[0] == '#define':
		                all_data = all_data + '|' + data[1].split('(')[0]
		            elif data[0] == 'typedef':
		            	if data[-1] == ';':
		            		typedef_data = typedef_data + '|' + data[-2].strip('*();[]')
		            	elif data[-1][-1] == ';':
		            		typedef_data = typedef_data + '|' + data[-1].strip('*();[]')
		        f.close()
		    
		all_data = all_data + ')\\b' 
		typedef_data = typedef_data + ')\\b'   

		xml_file= sublime.packages_path() + '\\C++\\C.tmLanguage'
		xml=ElementTree.ElementTree(file=xml_file)
		root = xml.getroot()

		string_node = root.findall('dict')[0].findall('array')[1][0].getchildren()[1];
		string_node.text = all_data
		string_node = root.findall('dict')[0].findall('array')[1][1].getchildren()[1];
		string_node.text = typedef_data
		xml.write(xml_file,  "UTF-8")
