import os
import shutil

class CBuilder(object):
    def __init__(self, current_prj: dict):
        self.current_prj = current_prj

    @staticmethod
    def __create_docker_runner(image:str, filename: str, command:str):
        print("Loading Code Checkers...")
        print("Filename: " + filename)
        with open(filename, 'w') as f:
            f.write('#!/bin/bash \n\n')
            
            f.write('IMAGE_NAME="' + image + '"\n\n')

            f.write('LOCAL_WORKING_DIR="$(pwd)"\n')
            f.write('DOCKER_WORKING_DIR="/usr/$(basename "${LOCAL_WORKING_DIR}")"\n')

            f.write('COMMAND_TO_RUN_ON_DOCKER=('+ command + ')\n\n')

            f.write('echo "###############################"\n')
            f.write('echo -e "Working Directory: \t ${LOCAL_WORKING_DIR}"\n')
            f.write('echo -e "Executing: \t ${COMMAND_TO_RUN_ON_DOCKER[*]}"\n')
            f.write('echo "###############################"\n')

            f.write("\n")
            f.write('''sudo docker run \\
                --rm \\
                -v "${LOCAL_WORKING_DIR}":"${DOCKER_WORKING_DIR}"\\
                -w "${DOCKER_WORKING_DIR}"\\
                --name my_container "${IMAGE_NAME}"  \\
                "${COMMAND_TO_RUN_ON_DOCKER[@]}"
            ''')

    def __create_git_files(self):
        print("Creating general git files...")
        shutil.copy( self.current_prj['templates_path'] + '/gitignore', '.gitignore')
        shutil.copy( self.current_prj['templates_path'] + '/authors', 'AUTHORS')
        open('README', 'a').close() 
        open('LICENSE', 'a').close() 
        open('CHANGELOG', 'a').close() 

    def __load_buildsystem(self):
        build_system = self.current_prj['c_project']['build_system']
        mcu_family = self.current_prj['c_project']['mcu_family']
        mcu = self.current_prj['c_project']['mcu']
        
        buildsystem_prefix = self.current_prj['templates_path'] + '/mcu/' +  \
                        mcu_family + '/' + build_system

        print("Loading Build System '"+ build_system + "' for MCU: " + mcu)
       
        if build_system == 'rake':
            shutil.copy( buildsystem_prefix + 'file.rb',  './')

            self.__create_docker_runner( self.current_prj['c_project']['toolchain_image'],
                    build_system + 'build.sh', 
                    'sh -c "rake clean DEVICE=' + mcu + ' && rake DEVICE=' + mcu + '"')


    def __create_gitlab_cicd_file(self):
        #TODO: use also template, maybe this in prjbuilder.py
        print("Creating gitlab CI/CD file...")
        shutil.copy( self.current_prj['templates_path']+ '/gitlab-ci.yml',  '.gitlab-ci.yml')

    def create(self):
        print("CREATING C PROJECT TEMPLATE...")

        utils_dir = "utils"
        os.mkdir("test")
        os.mkdir("src")
        os.mkdir("include")
        os.mkdir("doc")
        os.mkdir(utils_dir)

        self.__create_docker_runner( self.current_prj['c_project']['codeanalysis_image'],
                    utils_dir + '/run_c_checkers.sh',
                    '''sh -c "\\
                    bash /usr/checkers/00-style-analysis.sh     -I src/ -I include/  && \\
                    bash /usr/checkers/01-code-complexity.sh    -I src/ -I include/  && \\
                    bash /usr/checkers/02-static-analysis.sh    -I src/ -I include/"
                    ''')

        self.__create_git_files()

        self.__load_buildsystem()

        self.__create_gitlab_cicd_file()

        print("Success: C PROJECT TEMPLATE CREATED")


