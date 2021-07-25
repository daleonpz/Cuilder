import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import yaml
import shutil
import subprocess
import requests
PIPE = subprocess.PIPE

from FromNothing.cbuilder import *

def parse_test_data(current_path, test_path):
    yaml_template = """
        project:
            name: "python_test_prj"
            clone_type: "ssh"
            type: "c"
            path: "{test_path}"
            templates_path: "{current_path}/templates"
            extra_files:
                file1:
                    - '{current_path}/templates/gitlab-ci.yml' 
                    - '{test_path}/path_target/here/copy'
                anotherfile:
                    - '{current_path}/templates/gitlab-ci.yml'
                    - '{test_path}/cacalandia.yml'
            git:
                authors:
                        name:
                            - 'aoeu'
                            - 'name 3'
                            - 'daniel p'
                        email:
                            - 'email@test.de' 
                            - ''
                            - 'eouaoe.aue@email.de' 
                service: 'github'
                user: 'gituser'
                server: 'github.com'
                api_token: 'TestToken'
            c_project:
                mcu_family: "msp430"
                mcu: "msp430fr2433"
                build_system: "rake"
                toolchain_image: "toolchain_image.docker"
                codeanalysis_image: "codeanalysis_image.docker"
    """.format(current_path=current_path, test_path=test_path)

    return yaml.full_load(yaml_template)

class TestCBuilder(unittest.TestCase):

    def setUp(self):
        self.current_path = os.path.abspath(os.getcwd())
        self.test_path = self.current_path + "/__temp_test_folder"

        os.makedirs(self.test_path)
        os.chdir(self.test_path)

        project = parse_test_data(self.current_path, self.test_path) 
        cbuilder = CBuilder(project['project']) 
        cbuilder.create()

    def tearDown(self):
        os.chdir(self.current_path)
        shutil.rmtree(self.test_path)

    def test_src_dir_exist(self):
        self.assertTrue(os.path.isdir('src'))

    def test_include_dir_exist(self):
        self.assertTrue(os.path.isdir('include'))
    
    def test_test_dir_exist(self):
        self.assertTrue(os.path.isdir('test'))

    def test_doc_dir_exist(self):
        self.assertTrue(os.path.isdir('doc'))

    def test_utils_dir_exist(self):
        self.assertTrue(os.path.isdir('utils'))

    def test_run_checkers_file_exist(self):
        self.assertTrue(os.path.isfile('utils/run_c_checkers.sh'))

    def test_run_checkers_content(self):
        raw_content = """#!/bin/bash 

IMAGE_NAME="codeanalysis_image.docker"

LOCAL_WORKING_DIR="$(pwd)"
DOCKER_WORKING_DIR="/usr/$(basename "${LOCAL_WORKING_DIR}")"
COMMAND_TO_RUN_ON_DOCKER=(sh -c "\\
                    bash /usr/checkers/00-style-analysis.sh     -I src/ -I include/  && \\
                    bash /usr/checkers/01-code-complexity.sh    -I src/ -I include/  && \\
                    bash /usr/checkers/02-static-analysis.sh    -I src/ -I include/"
                    )

echo "###############################"
echo -e "Working Directory: 	 ${LOCAL_WORKING_DIR}"
echo -e "Executing: 	 ${COMMAND_TO_RUN_ON_DOCKER[*]}"
echo "###############################"

sudo docker run \\
                --rm \\
                -v "${LOCAL_WORKING_DIR}":"${DOCKER_WORKING_DIR}"\\
                -w "${DOCKER_WORKING_DIR}"\\
                --name my_container "${IMAGE_NAME}"  \\
                "${COMMAND_TO_RUN_ON_DOCKER[@]}"
            """
        with open(self.test_path + '/utils/run_c_checkers.sh') as f:
                checker_content = f.read()

        self.assertTrue(raw_content == checker_content)

if __name__ == "__main__":
    unittest.main()

