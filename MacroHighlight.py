import os
from xml.etree import ElementTree
import sublime, sublime_plugin

class MacroHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_path = sublime.active_window().folders()[0]
		files = os.listdir(file_path);

		all_data = '\\b(ThisIsMacroList'
		for filename in files:
		    if filename[-2:] == '.h' or filename[-2:] == '.H':
		        f = open(file_path + '\\' + filename) 
		        lines = f.readlines()

		        for line in lines:
		            data = line.split()
		            if not data:
		                continue
		            if data[0] == '#define':
		                all_data = all_data + '|' + data[1].split('(')[0]
		        f.close()
		    
		all_data = all_data + ')\\b'    

		xml_file= sublime.packages_path() + '\\C++\\C.tmLanguage'
		xml=ElementTree.ElementTree(file=xml_file)
		root = xml.getroot()

		string_node = root.findall('dict')[0].findall('array')[1].find('dict').getchildren()[1]
		string_node.text = all_data
		xml.write(xml_file,  "UTF-8")
