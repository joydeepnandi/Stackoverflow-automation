import shlex
from subprocess import Popen, PIPE
import requests
import webbrowser


# Execute the external command and get its exitcode, stdout and stderr

def getData(cmd):
    args = shlex.split(cmd)
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    return output, error


# checks for errors and makes a request in encountering an error
def make_request(error):
    print("Searching for " + error)
    response = requests.get(
        "https://api.stackexchange.com/" + "/2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(
            error))
    return response.json()


# gets the specified url for the error in the code
def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == 3:
            break
    for i in url_list:
        webbrowser.open(i)


# give the path for input file
filePath = input("Enter the name of the python file you want to check:")

# running the main function calling all other functions

if __name__ == "__main__":
    output, error = getData("python {}".format(filePath))
    error = error.decode("utf-8").strip().split("\r\n")[-1]
    print("Error found: ", error)
    if (error):
        error_list = error.split(":", 1)
        json1 = make_request(error_list[0])
        json2 = make_request(error_list[1])
        json3 = make_request(error)
        get_urls(json1)
        get_urls(json2)
        get_urls(json3)
    else:
        print("Congratulations! Your code is error free.")