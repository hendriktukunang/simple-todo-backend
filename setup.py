import sys
import os
import subprocess


def main(argv):
    path = os.getcwd()
    os.chdir(path + "/")

    # try to get the repo url
    try:
        repo_url = argv[0]
    except:
        repo_url = None

    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    if repo_url:
        subprocess.call(["rm", "-rf", ".git"])
        subprocess.run(["git", "init"])
        subprocess.run(["git", "remote", "add", "origin", repo_url])
    subprocess.run(["pre-commit", "install"])
    print("repository setup ok!")

    subprocess.run(["docker-compose", "up", "-d", "--build"])
    print("docker setup ok!")


if __name__ == "__main__":
    main(sys.argv[1:])
