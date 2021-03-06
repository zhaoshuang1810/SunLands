# coding=utf-8
from ParserSwagger import *
from Conf.Properties import *


class CreateAPICases(object):

	def __init__(self,filename):
		self.parser = ParserSwagger(filename)

	def fileOne(self, suitname):
		dir = os.path.join(api_cases_dir, suitname + ".robot")
		f = open(dir, "w")
		setting = []
		setting.append("*** Settings ***\n")
		setting.append("Force Tags        DocTest    " + suitname + "\n")
		setting.append("Library           ../../Lib/JsonRead.py\n")
		setting.append("Resource          ../../Res/Common.robot\n")
		setting.append("Variables         ../../Variables.py\n")
		setting.append("\n\n")
		setting.append("*** Test Cases ***\n")
		f.writelines(setting)
		f.close()

	def newFile(self):
		tags = self.parser.tags
		for tag in tags:
			self.fileOne(tag)

	def caseOne(self, path):
		modes = self.parser.get_path_modes(path)
		for mode in modes:
			tags = self.parser.get_path_tags(path)
			for tag in tags:
				dir = os.path.join(api_cases_dir, tag + ".robot")
				f = open(dir, 'a+')
				content = self._caseContent(path, mode, tag)
				f.writelines(content)
				f.write("\n")
				f.close()

	def caseTag(self, tag):
		tags_paths = self.parser.get_tags_paths()
		for path in tags_paths[tag]:
			self.caseOne(path)

	def caseAll(self):
		paths = self.parser.paths
		for path in paths:
			self.caseOne(path)

	def _caseContent(self, path, mode, tag):
		data = self.parser.paths_data[path][mode]
		content = []
		parameters = data['parameters']
		summary = data['summary']

		suitename = tag
		casename = mode + path

		documentation = "\t[Documentation]    " + summary.encode("utf-8") + "\n"
		tags = "\t[Tags]    NotRun\n"
		if len(parameters) > 0:
			json_param = "\t${params}    getParam_data    " + suitename + "    " + casename + "\n"
			resp = "\t${resp}    getApiResp    ${token}    " + mode + "    " + path + "    ${params}\n"
		else:
			json_param = ""
			resp = "\t${resp}    getApiResp    ${token}    " + mode + "    " + path + "\n"

		assertd = "\t${result}    docmentAssert    " + mode + "    " + path + "    ${resp}\n"
		assertc = "\tshould be true     ${result[0]}     ${result}\n"

		content.append(casename)
		content.append("\n")
		content.append(documentation)
		content.append(tags)
		content.append(json_param)
		content.append(resp)
		content.append(assertd)
		content.append(assertc)
		return content
