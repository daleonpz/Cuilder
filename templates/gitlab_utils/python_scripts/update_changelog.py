#!/usr/bin/python3.7

import sys, json
import re
import requests
import getopt
from datetime import datetime
from urllib.parse import urlparse

class Changelogs:
    def __init__(self, filename, url, token, project_id):
        self.filename   = filename
        self.url        = url
        self.token      = token
        self.project_id = project_id

    def __parse_gitlab_tags(self):
        headers = {'content-type': 'application/json', 
                'Accept-Charset': 'UTF-8', 
                'PRIVATE-TOKEN' : self.token}
        r = requests.get(self.url + 'tags', headers=headers)

        return r.json()

    def __get_date_last_release(self):
        try:
            with open(self.filename,'r') as contents:
                first_line = contents.readline()
            if not first_line.strip():
                first_line = "1900-01-01"
        except IOError:
            first_line = "1900-01-01"
        finally:
            match = re.search(r'\d{4}-\d{2}-\d{2}', first_line)
            date_last_release = datetime.strptime(match.group(), '%Y-%m-%d').date().strftime("%Y-%m-%d")
            return date_last_release

    def __get_last_changelogs(self):
        date_last_release = self.__get_date_last_release()
        gitlab_tags = self.__parse_gitlab_tags()

        new_changelogs = []

        for x in range(len(gitlab_tags)):
            current_tag = gitlab_tags[x]
            if current_tag['release'] is not None:

                tag_name    =   current_tag['release']['tag_name']
                tag_notes   =   current_tag['release']['description']
                tag_timestamp = current_tag['commit']['created_at']
                tag_date    =   datetime.fromisoformat(tag_timestamp).strftime("%Y-%m-%d")

                if tag_date > date_last_release:
                    new_changelogs.append('[' + tag_name + '] ' + tag_date + '\n')
                    new_changelogs.append(tag_notes + '\n\n')

        return new_changelogs

    def update_changelogs(self):
        new_changelogs = self.__get_last_changelogs()
        changelog_file = self.filename

        if new_changelogs:
            try:
                with open(changelog_file,'r') as contents:
                    save = contents.read()
                with open(changelog_file,'w') as contents:
                    contents.writelines(new_changelogs)
                with open(changelog_file,'a') as contents:
                    contents.write(save)
            except IOError:
                with open(changelog_file,'w') as contents:
                    contents.writelines(new_changelogs)
            finally:
                print("ChangeLog updated")
                contents.close()
        else:
            print("ChangeLogs wasn't updated")

    def push_commit(self):
        data = {
            "branch": "develop/changelog",
            "commit_message": "Update CHANGELOG",
            "actions": [
                {
                    "action": "update",
                    "file_path": self.filename,
                    'content': open(self.filename).read()
                }
                ]
            }
        headers = {'Content-type': 'application/json', 
                'Accept': 'text/plain',
                'PRIVATE-TOKEN' : self.token}
        r = requests.post(self.url + 'commits', json=data,  headers=headers)
        print(r.status_code)

def parse_arg(argv):
    url = ''
    token = ''
    prj_id  = ''
    url_found = False
    token_found = False
    prj_id_found = False
    try:
        opts, args = getopt.getopt(argv,"hi:u:t:",["id=","url=","token="])
    except getopt.GetoptError:
        print('update_changelog.py -i ${CI_PROJECT_ID} -t ${PRIVATE_TOKEN} -u ${CI_PROJECT_URL}')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('update_changelog.py -i ${CI_PROJECT_ID} -t ${PRIVATE_TOKEN} -u ${CI_PROJECT_URL}')
            sys.exit()
        elif opt in ("-i", "--id"):
            prj_id = arg
            prj_id_found = True
        elif opt in ("-u", "--url"):
            url = arg
            urlparsed = urlparse(url)
        #     urlparsed._replace(path='/api/v4/projects/' + prj_id + '/repository/tags')
        #     url_tags = urlparsed.geturl()
            url = urlparsed.scheme + '://' + urlparsed.netloc + '/api/v4/projects/' + prj_id + '/repository/'
            url_found = True
        elif opt in ("-t", "--token"):
            token = arg
            token_found = True

    if token_found and url_found and prj_id_found:
        return url, token, prj_id
    else:
        print("Not enough arguments...")
        print('update_changelog.py -i ${CI_PROJECT_ID} -t ${PRIVATE_TOKEN} -u ${CI_PROJECT_URL}')
        sys.exit(2)


if __name__ == "__main__":
    url, token, prj_id = parse_arg(sys.argv[1:])
    print("url: " + url)
    print("token: " + token)
    print("prj_id: " + prj_id)

    changelogs = Changelogs('CHANGELOG.md', url, token, prj_id)
    changelogs.update_changelogs()
    changelogs.push_commit()

