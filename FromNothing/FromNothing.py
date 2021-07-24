import yaml
import sys
import os
import subprocess
PIPE = subprocess.PIPE

from .cbuilder import CBuilder

class FromNothing(object):
    def __init__(self, yml_file: str): 
        try: 
           with open(yml_file, 'r') as file:
                dictionary = yaml.full_load(file)
                self.projects = dictionary 
        except IOError: 
            sys.exit("YAML couldn't be opened")
        
    def new_project(self):
        for prj, prj_info in self.projects.items():
            self.__create(prj_info)

    def __create(self, prj):
        self.current_prj = prj
        prj_type = prj['type']

        if prj_type == 'c':
            self.__create_c()
        elif prj_type == 'bash':
            self.__create_bash()
        else:
            print("Unknow project type")

    def __go_to_project_dir(self):
        prj_path = self.current_prj['path'] + '/' + self.current_prj['name']
        try: 
            os.mkdir(prj_path)
        except FileExistsError:
            sys.exit("An existing project with the following path already exist: " + prj_path)
        os.chdir(prj_path)
        print(os.getcwd())

    def __create_c(self):
        self.__go_to_project_dir()

        process = subprocess.Popen(['git', 'init'], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()

        cbuilder = CBuilder(self.current_prj) 
        cbuilder.create()

        #TODO: maybe use logging to print everything
#     # To Create A New GitLab Project
#     git add --all
#     git commit -m "New project: ${PRJ_NAME}"
#     if [ "${SSH}" == "ssh" ]; then
#         git remote add origin https://"${SERVER_GIT}":"${NAMESPACE}"/"${PRJ_NAME}".git
#         git push --set-upstream https://"${SERVER_GIT}":"${NAMESPACE}"/"${PRJ_NAME}".git master
#     else
#         git remote add origin git@"${SERVER_GIT}":"${NAMESPACE}"/"${PRJ_NAME}".git
#         git push --set-upstream git@"${SERVER_GIT}":"${NAMESPACE}"/"${PRJ_NAME}".git master
#     fi



