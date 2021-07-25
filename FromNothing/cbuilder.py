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

    @staticmethod
    def __create_test_example_file(filename):
        with open(filename, 'w') as f:
            f.write(""" // Ceedling test example
#include "unity.h"
#include "cmock.h"
#include "dummy.h"

void setUp() 
{
}

void tearDown() 
{
}

void test_example()
{
    TEST_ASSERT_TRUE(1,1);
}
            """)

    @staticmethod
    def __create_main_file(filename):
        with open(filename, 'w') as f:
            f.write("""#include "<stdint.h>"

int main(void)
{
    // Your application
}
            """)

    def create(self):
        print("CREATING C PROJECT TEMPLATE...")

        utils_dir = "utils"
        os.mkdir("test")
        os.mkdir("test/test_files")
        self.__create_test_example_file("test/test_files/test_dummy.c")

        os.mkdir("src")
        self.__create_main_file("src/main.c")

        os.mkdir("include")
        open('./include/dummy.h', 'a').close()

        os.mkdir("doc")
        open('./doc/dummy.md', 'a').close()
        os.mkdir(utils_dir)

        self.__create_docker_runner( self.current_prj['c_project']['codeanalysis_image'],
                    utils_dir + '/run_c_checkers.sh',
                    '''sh -c "\\
                    bash /usr/checkers/00-style-analysis.sh     -I src/ -I include/  && \\
                    bash /usr/checkers/01-code-complexity.sh    -I src/ -I include/  && \\
                    bash /usr/checkers/02-static-analysis.sh    -I src/ -I include/"
                    ''')

        self.__load_buildsystem()

        print("Success: C PROJECT TEMPLATE CREATED")


