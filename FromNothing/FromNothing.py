import yaml
import sys
import os
import shutil
import errno
import logging 

from .cbuilder import CBuilder
from .gitsupport import GitSupport

logger = logging.getLogger(__name__)

def copy_file(src: str, dest: str):
    try:
        shutil.copy(src, dest)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)

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

    
    @staticmethod
    def __move_extra_files(current_prj: dict, prj_path: str):
        logger.info(os.path.abspath(os.getcwd()))
        if 'extra_files' in current_prj :
            logger.info("Moving extra files...")

            for filetag, filepaths in current_prj['extra_files'].items():
                copy_file( filepaths[0], 
                        prj_path + '/' + filepaths[1])

    def __create(self, prj):
        self.current_prj = prj
        prj_type = prj['type']

        gitsupport = GitSupport(self.current_prj['git'],
                                self.current_prj['name'],
                                self.current_prj['clone_type'])

        prj_dir = self.current_prj['path'] + '/' + self.current_prj['name']

        try: 
            os.mkdir(prj_dir)
        except FileExistsError:
            sys.exit("An existing project with the following path already exist: " + prj_dir)

        self.__move_extra_files(self.current_prj, prj_dir)
        os.chdir(prj_dir)
        logger.info(os.getcwd())

        if prj_type == 'c':
            cbuilder = CBuilder(self.current_prj) 
            cbuilder.create()
#         elif prj_type == 'bash':
#             self.__create_bash()
        else:
            sys.exist("Unknow project type")
        
        gitsupport.init_repo()
        gitsupport.create_info_files()
        gitsupport.push_project()

