'''
Created on 5. 10. 2019

@author: miros
'''
import urllib
import gzip
import os
from http.client import IncompleteRead

import srt
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.request
from datetime import timedelta

csfd = "https://www.csfd.cz"

def download_page(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
    except IncompleteRead as e:
        data = e.partial
    try:
        text = gzip.decompress(data)
    except:
        text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    return BeautifulSoup(text, 'html.parser')


class Movie:
    def __init__(self, name):
        self.name = name

    def load_data(self):
        try:
            url = self.get_movie_url()
            soup = download_page(url)
            profile = soup.select("#profile")[0]
            self.true_name = BeautifulSoup(profile.find_all("h1")[0].text, "lxml").text.strip()
            self.genre = profile.select(".genre")[0].contents[0]
            self.origin = BeautifulSoup(profile.select(".origin")[0].text, "lxml").text
            self.creators = BeautifulSoup(profile.select(".creators")[0].text, "lxml").text
            try:
                self.plot = BeautifulSoup(soup.select("#plots")[0].find_all("li")[0].text, "lxml").text
            except IndexError:
                self.plot=""
            self.loaded = True

        except Exception as e:
            print("Movie not loaded due to exception: " + str(e))
            self.loaded = False
            raise  e


    def get_desc(self):
        if self.loaded:
            desc = self.true_name + "\n" + self.genre + "\n"
            desc += self.origin
            return desc, self.plot
        else:
            return None

    def get_movie_url(self):
        name = "+".join(self.name.split())
        url = csfd + "/hledat/?q=" + name
        print(url)
        soup = download_page(url)
        search_result = soup.select("#search-films")[0].select(".ui-image-list")
        if len(search_result) == 0:
            print("Movie {} not found.".format(self.name))
            return None
        first_result = search_result[0].find_all("li")[0].find_all("a")[0].get("href")
        return csfd + first_result


def get_all_files_with_ext(dir, ext):
    found_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(ext):
                found_files.append(os.path.join(root, file))
    return found_files


def get_movie_files(dir):
    files = []
    for ext in ["avi", "mp4", "mkv"]:
        files = files + get_all_files_with_ext(dir, ext)
    return files

def create_srt(file):
    srt_file = os.path.splitext(file)[0] + ".srt"
    if not os.path.exists(srt_file):
        with open(srt_file, "w"):
            pass


def get_name(path):
    return Path(path).stem


def write_desc(path, desc, duration=30):
    with open(path, "r") as f:
        content = f.read()
    srt_generator = srt.parse(content)
    subtitles = list(srt_generator)

    should_work_this = True
    if len(subtitles) > 0:
        first_sub_delta = subtitles[0].start
        should_work_this = subtitles[0].start != 0
    else:
        first_sub_delta = timedelta(seconds=999999)

    if should_work_this:
        start = timedelta(seconds=0)
        end = timedelta(seconds=duration)

        halftime = min(end, first_sub_delta)/2
        info = srt.Subtitle(1, start, halftime, desc[0])
        subtitles.append(info)
        info = srt.Subtitle(2, halftime, end, desc[1])
        subtitles.append(info)
        subtitles = list(srt.sort_and_reindex(subtitles))

        with open(path, "w") as f:
            f.write(srt.compose(subtitles))


def work_movie(path):
    name = get_name(path)
    print("Movie: {}".format(name))
    movie = Movie(name)
    movie.load_data()
    desc = movie.get_desc()
    print(desc)
    if desc is not None:
        write_desc(path, desc)
        pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default="C:\\Users\\mkrabec\\Videos", type=str, help="Path of the directory")
    args = parser.parse_args()

    def prepare_test(file):
        path = os.path.join(args.d, "test")
        testpath = os.path.join(path, os.path.basename(file))
        os.system("mkdir {}".format(path))
        os.system("copy {} {}".format(file, testpath))
        return testpath


    movie_files = get_movie_files(args.d)
    print(movie_files)
    for file in movie_files:
        create_srt(file)
    srt_files = get_all_files_with_ext(args.d, ".srt")
    for file in srt_files:
        work_movie(file)
    # file = srt_files[0]
    # file = prepare_test(file)
    # work_movie(file)
