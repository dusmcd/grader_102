#! /usr/bin/env python3
import os
import shutil
import subprocess
from queue import Queue
from datetime import datetime

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
    
    for i in range(len(words)):
        if "Submitted" in words[i]:
            date_str = str.join(" ", words[i + 1:i + 7])
            break

    filename.reverse()

    return (f"{words[1]} {words[2]}", " ".join(filename), date_str)

def find_html_files(path="current", num_files=1):
    # perform breadth-first search
    queue = Queue()
    queue.enqueue(path)
    files = []

    while queue.count > 0:
        current = queue.dequeue()

        if "__MACOSX" in current:
            continue

        if os.path.isdir(current):
            for item in os.listdir(current):
                queue.enqueue(f"{current}{SEP}{item}")
        elif current[-4:].lower() == "html":
            files.append(current)
            if len(files) == num_files:
                return files

    return files

def get_latest_submission(subs):
    latest_entry =  max(subs, key=lambda sub : sub[1])
    return latest_entry[0]
    

def process_submissions(subs, num_files):
    count = 0
    for key, val in subs.items():
        print(f"Currently grading: {key}")
        if len(val) > 1:
            print("There are multiple submissions for this student. Choosing latest submission...\n")
            val = get_latest_submission(val)
        else:
            # just grab the filename of the first entry (a list of tuples)
            val = val[0][0]
        if val[-4:].lower() == "html":
            print(f"Opening {val} in browser...")
            subprocess.run([BROWSER, f"{os.getcwd()}{SEP}submissions{SEP}{val}"])
        elif val[-3:].lower() == "zip":
            if os.path.isdir("current"):
                shutil.rmtree("current")
            os.mkdir("current")
            unzip_file(f"submissions{SEP}{val}", "current")

            html_files = find_html_files(num_files=num_files)
            if len(html_files) == 0: 
                print("html file not found. Investigate manually")
            else:
                for html in html_files:
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
    num_files = int(input("How many html files do you need to grade per student? "))
    num_submissions = {}
    if os.path.isdir("submissions"):
        shutil.rmtree("submissions")

    for file in os.listdir():
        if file[-3:].lower() == "zip":
            unzip_file(file, "submissions")

    for file in os.listdir("submissions"):
        if file[-3:] == "txt":
            (name, filename, date_str) = get_data_from_txt_file(f"submissions{SEP}{file}")
            file_datetime = datetime.strptime(date_str, "%A, %B %d, %Y %I:%M:%S %p") 
            if name in num_submissions:
                num_submissions[name].append((filename, file_datetime))
            else:
                num_submissions[name] = [(filename, file_datetime)]

    process_submissions(num_submissions, num_files)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
