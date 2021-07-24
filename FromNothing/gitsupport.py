import shutil
import subprocess
import requests
PIPE = subprocess.PIPE

class GitSupport(object):

    def __init__(self, git_info: dict, prjname: str, clone_type: str):
        self.server = git_info['server'] 
        self.user = git_info['user']
        self.api_token = git_info['api_token']
        self.service = git_info['service']
        self.prjname = prjname
        self.clone_type = clone_type
        self.authors = None
        if 'authors' in git_info:
            self.authors = git_info['authors']


    def init_repo(self):
        process = subprocess.Popen(['git', 'init'], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()

    def create_gitlab_cicd_file(self):
        #TODO: use also template, maybe this in prjbuilder.py
        print("Creating gitlab CI/CD file...")
#         shutil.copy( self.current_prj['templates_path']+ '/gitlab-ci.yml',  '.gitlab-ci.yml')

    def __create_authors_file(self):
        with open('AUTHORS','w') as f: 
            f.write("AUTHORS:\n")

            if self.authors is not None:
                for x in range(0, len(self.authors['name'])):
                    f.write("* " + self.authors['name'][x] + " ")
                    f.write("("  + self.authors['email'][x] + ")\n")
            else:
                f.write("<Your-Name> <youre_mail> (your_website)")

    def create_info_files(self):
        print("Creating general git files...")
        open('.gitignore', 'a').close() 
        open('README', 'a').close() 
        open('LICENSE', 'a').close() 
        open('CHANGELOG', 'a').close() 
        self.__create_authors_file()

    def push_project(self):

        if self.service == 'github':
            r = requests.post('https://api.github.com/user/repos', 
                    auth=(self.user, self.api_token),
                    json = {"name": self.prjname} )
            print("Request Status :")
            print(r.status_code)

        process = subprocess.Popen(['git', 'add','--all'], stdout=PIPE, stderr=PIPE)
        process = subprocess.Popen(['git', 'commit','--m', 'New Project'], stdout=PIPE, stderr=PIPE)

        gitpath = self.server + ":" + self.user + "/" + self.prjname  + '.git'
        
        if self.clone_type == 'ssh':
            gitpath = 'git@' +  gitpath
        else:
            gitpath = 'https://' +  gitpath

        print('GitPath: ' + gitpath)
        process = subprocess.Popen(['git', 'remote', 'add','origin', gitpath], stdout=PIPE, stderr=PIPE)
        process = subprocess.Popen(['git', 'push','--set-upstream', 'origin', 'master'], stdout=PIPE, stderr=PIPE)

