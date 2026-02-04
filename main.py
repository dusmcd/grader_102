#! /usr/bin/env python3
import os
import shutil
import subprocess

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

def process_submissions(subs):
    for key, val in subs.items():
        print(f"Currently grading: {key}")
        if not val:
            print("There are multiple submissions for this student. Process manually\n")
        else:
            print("Opening html file in Firefox...")

        input("Press enter to process next student...")
        print("\n")

def main():
    num_submissions = {}
    if os.path.isdir("submissions"):
        shutil.rmtree("submissions")

    for file in os.listdir():
        if file[-3:] == "zip":
            subprocess.run(["unzip", file, "-d", "submissions"])

    for file in os.listdir("submissions"):
        if file[-3:] == "txt":
            data = get_data_from_txt_file(f"submissions/{file}")
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
