# FromNothing

Project Creator that allows you to create a basic project C structure and commit it to your git server. Works with GitLab and GitHub.  


You need a **Personal Access Token** to use FromNothing. 
- [GitLab Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [GitHub Token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)


FromNothing requires a YAML file. [Here is an example](https://github.com/daleonpz/FromNothing/blob/master/example.yml).


## Run Tests

```sh
$ python -m unittest discover
```

## C Projects
- Features: 
  - TDD with ceedling and docker
  - Code analysis with docker. 
      - Cyclomatic complexity with [Lizard](https://github.com/terryyin/lizard)
      - Static analyser with [CppCheck](http://cppcheck.sourceforge.net/)
      - Style checking with [AStyle](http://astyle.sourceforge.net/)

# TODO:
```sh
$  todo-txt ls
2 @fromnothing add error handling everywhere
4 @fromnothing add file templates for c project
3 @fromnothing change printfs for logging
5 @fromnothing create docker image QA to pull from in DockerHub
1 @fromnothing add tests
```
