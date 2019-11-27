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

        def parse_creators(profile):
            desc = []
            divs = profile.select(".creators")[0].find_all("div")
            displayed_roles = ["Režie", "Hrají"]
            for div in divs:
                try:
                    role, names = div.text.split(":")
                except:
                    pass

                striped_role = role.strip()

                if striped_role in displayed_roles:
                    displayed_roles.remove(striped_role)
                    striped_names = names.strip().split(",")
                    striped_names = striped_names[0:min(len(striped_names), 5)]
                    striped_names = ", ".join(striped_names)
                    desc.append(striped_role + ": " + striped_names)
            desc = "\n".join(desc)

            return desc

        try:
            self.url = self.get_movie_url()
            if self.url == None:
                return
            soup = download_page(self.url)
            profile = soup.select("#profile")[0]
            self.true_name = BeautifulSoup(profile.find_all("h1")[0].text, "lxml").text.strip()
            self.genre = profile.select(".genre")[0].contents[0]
            self.origin = BeautifulSoup(profile.select(".origin")[0].text, "lxml").text
            self.creators = parse_creators(profile)
            try:
                self.plot = BeautifulSoup(soup.select("#plots")[0].find_all("li")[0].text, "lxml").text
            except IndexError:
                self.plot = ""
            self.loaded = True
        except Exception as e:
            print("Movie not loaded due to exception: " + str(e))
            self.loaded = False
            raise e

    def get_desc(self):
        desc = []
        if self.loaded:
            desc.append(self.true_name + " - " + self.genre + "  " + self.origin + "\n" + self.creators)
            splited = self.plot.split()
            desc.append(" ".join(splited[0:len(splited) // 2]))
            desc.append(" ".join(splited[len(splited) // 2:]))
            print(desc)
            return desc
        else:
            return None

    def get_movie_url(self):
        name = "+".join(self.name.split())
        url = csfd + "/hledat/?q=" + name
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
        first_sub = subtitles[0]
        first_sub_start = first_sub.start.total_seconds()
        should_work_this = subtitles[0].start != 0
    else:
        first_sub_start = duration

    if should_work_this:
        duration = min(first_sub_start, duration)
        one_frame_duration = duration / len(desc)

        for i, d in enumerate(desc):
            start = timedelta(seconds=one_frame_duration * i)
            end = timedelta(seconds=one_frame_duration * (i + 1))
            subtitles.append(srt.Subtitle(1, start, end, d))

        subtitles = list(srt.sort_and_reindex(subtitles))

        with open(path, "w") as f:
            f.write(srt.compose(subtitles))


def work_movie(path):
    name = get_name(path)
    print("Movie: {}".format(name))
    movie = Movie(name)
    movie.load_data()
    desc = movie.get_desc()
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
        test_path = os.path.join(path, os.path.basename(file))
        os.system("mkdir {}".format(path))
        os.system("copy {} {}".format(file, test_path))
        return test_path


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
