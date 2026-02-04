#! /usr/bin/env python3
import os
import shutil
import subprocess

def parse_txt_file(file):
    with open(file) as report:
        words = report.read().split(" ")

    print(words)

def main():
    if os.path.isdir("submissions"):
        shutil.rmtree("submissions")

    for file in os.listdir():
        if file[-3:] == "zip":
            subprocess.run(["unzip", file, "-d", "submissions"])

    for file in os.listdir("submissions"):
        if file[-3:] == "txt":
            parse_txt_file(f"submissions/{file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
