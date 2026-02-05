#! /usr/bin/env python3
import os
import shutil
import subprocess
from queue import Queue

SEP = os.sep
BROWSER = "chrome" if os.name == "nt" else "firefox"

def get_data_from_txt_file(file):
    with open(file) as report:
        words = report.read().strip().split(" ")

    filename = []
    for i in range(len(words) - 1, 0, -1):
        if "Filename" in words[i]:
            break
        filename.append(words[i]) 

    filename.reverse()

    return (f"{words[1]} {words[2]}", " ".join(filename))

def find_html_file(path="current"):
    # perform breadth-first search
    queue = Queue()
    queue.enqueue(path)

    while queue.count > 0:
        current = queue.dequeue()

        if "__MACOSX" in current:
            continue

        if os.path.isdir(current):
            for item in os.listdir(current):
                queue.enqueue(f"{current}{SEP}{item}")
        elif current[-4:].lower() == "html":
            return current

    return None


def process_submissions(subs):
    count = 0
    for key, val in subs.items():
        print(f"Currently grading: {key}")
        if not val:
            print("There are multiple submissions for this student. Process manually\n")
        elif val[-4:].lower() == "html":
            print(f"Opening {val} in browser...")
            subprocess.run([BROWSER, f"{os.getcwd()}{SEP}submissions{SEP}{val}"])
        elif val[-3:].lower() == "zip":
            if os.path.isdir("current"):
                shutil.rmtree("current")
            os.mkdir("current")
            unzip_file(f"submissions{SEP}{val}", "current")

            html = find_html_file()
            if html is None:
                print("html file not found. Investigate manually")
            else:
                print(f"Opening {html} in browser...")
                subprocess.run([BROWSER, f"{os.getcwd()}{SEP}{html}"])
        else:
            print("file type not recognized. Investigate manually")

        input("Press enter to process next student...")
        count += 1
        print("\n")

    print(f"{count} submissions graded")

def unzip_file(file, dest):
    if os.name == "nt":
        subprocess.run([
            "powershell",
            "-Command",
            f"Expand-Archive -Path '{file}' -DestinationPath '{dest}'"
        ])
    else:
        subprocess.run(["unzip", file, "-d", f"{dest}"])

def main():
    num_submissions = {}
    if os.path.isdir("submissions"):
        shutil.rmtree("submissions")

    for file in os.listdir():
        if file[-3:].lower() == "zip":
            unzip_file(file, "submissions")

    for file in os.listdir("submissions"):
        if file[-3:] == "txt":
            data = get_data_from_txt_file(f"submissions{SEP}{file}")
            if data[0] in num_submissions:
                num_submissions[data[0]] = False
            else:
                num_submissions[data[0]] = data[1]

    process_submissions(num_submissions)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
