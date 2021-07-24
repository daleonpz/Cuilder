import yaml
import sys
import os
import shutil

from .cbuilder import CBuilder
from .gitsupport import GitSupport

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

    def __go_to_project_dir(self):
        prj_path = self.current_prj['path'] + '/' + self.current_prj['name']
        try: 
            os.mkdir(prj_path)
        except FileExistsError:
            sys.exit("An existing project with the following path already exist: " + prj_path)
        os.chdir(prj_path)
        print(os.getcwd())

    def __create(self, prj):
        self.current_prj = prj
        prj_type = prj['type']

        gitsupport = GitSupport(self.current_prj['git'],
                                self.current_prj['name'],
                                self.current_prj['clone_type'])

        self.__go_to_project_dir()


        if prj_type == 'c':
            cbuilder = CBuilder(self.current_prj) 
            cbuilder.create()
#         elif prj_type == 'bash':
#             self.__create_bash()
        else:
            print("Unknow project type")
        
        gitsupport.init_repo()
        gitsupport.create_info_files()
        gitsupport.create_gitlab_cicd_file()
        gitsupport.push_project()

