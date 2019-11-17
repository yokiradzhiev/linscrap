import pandas
import requests
from bs4 import BeautifulSoup
import time
import os
import datetime

class LinkScraper:

    def __init__(self):
        self.first_url = input("Enter the url: ")
        self.tick = input(
            "Time between each pull of a web page.You can get banned for too many requests to a site in a short time. This timer helps prevent this.(seconds): ")
        self.max_depth = input("How deep to search(If you enter 3 each link in each link in each link will be listed): ")
        self.failed_calls = []
        self.total_calls = []
        self.failed_calls.append(0)
        self.total_calls.append(0)
        self.parent_list = []
        self.link_list = []


    def rec_get_all_pages_dict(self, dept, parent_string, url):
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            if dept <= float(self.max_depth):
                counter = 0
                try:
                    self.parent_list.append(parent_string)
                    counter += 1
                    l = link.get('href')
                    print("Before '/' removed:")
                    print(l)
                    if l[0] == "/":
                        if url[len(url) - 1] == '/':
                            while l[0] == "/":

                                nl = l[1:]
                                l = nl
                        l = url + l
                    ls = l.split(" ")
                    l = ""
                    for i in range(len(ls)):
                        l += ls[i]
                    print("After '/' removed:")
                    print(l)
                    self.link_list.append(l)
                    counter += 1
                    time.sleep(float(self.tick))
                    self.rec_get_all_pages_dict(dept + 1, parent_string + " -> " + url, l)
                except Exception as e:
                    self.failed_calls[0] += 1
                    print("Something went wrong. This actually:")
                    print(e)
                finally:
                    self.total_calls[0] += 1
                    if counter == 1:
                        self.link_list.append("Error.")


    def main(self):
        self.rec_get_all_pages_dict(1, "", self.first_url)
        for i in range(len(self.parent_list)):
            if i != 0:
                self.failed_calls.append("")
                self.total_calls.append("")
        if len(self.parent_list) == 0:
            self.parent_list.append("")
        if len(self.link_list) == 0:
            self.link_list.append("")
        print(len(self.parent_list))
        print(len(self.link_list))
        print(len(self.failed_calls))
        print(len(self.total_calls))
        frame = pandas.DataFrame({
            "Parent": self.parent_list,
            "Links": self.link_list,
            "Failed Calls": self.failed_calls,
            "Total Calls": self.total_calls
        })
        try:
            os.mkdir("files")
        except Exception as e:
            nothing = "folder already exists"
        finally:
            s = datetime.datetime.now()
            l = "%s-%s-%s_%s-%s-%s" % (s.year, s.month, s.day, s.hour, s.minute, s.second)
            frame.to_csv("files/Links:%s.csv" % l)
            if len(self.link_list) == 0:
                print('Sorry no links were found.')

ls = LinkScraper()
ls.main()
