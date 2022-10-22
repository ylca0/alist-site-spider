from selenium import webdriver
from selenium.webdriver.common.by import By
import os

browser = webdriver.Firefox(
    firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe"
)

download_file_type = ["mp4", "txt"]
root_url = ""
root_dir = os.getcwd()
time_out = 10


def get_url_list(url):
    browser.get(url)
    browser.implicitly_wait(time_out)

    labels = [i.text for i in browser.find_elements(By.CLASS_NAME, "chakra-text")]
    links = [
        i.get_attribute("href")
        for i in browser.find_elements(By.CLASS_NAME, "chakra-linkbox__overlay")
    ]
    return (labels, links)


def spider_url(url, dir):

    labels, links = get_url_list(url)

    while str(labels).find("''") != -1 or str(links).find("''") != -1:
        labels, links = get_url_list(url)

    i = 3
    j = 0
    while i < len(labels) and j < len(links):
        current_file_path = dir + "\\" + labels[i]

        if labels[i].split(".")[-1] in download_file_type:
            print("download file:" + current_file_path)
            f = open(current_file_path, "w")
            f.write(links[j])
            f.close()
        else:
            try:
                os.makedirs(current_file_path)
                print("makedir:" + current_file_path)
            except Exception as e:
                print("makedir:", e)
            spider_url(links[j], current_file_path)

        i += 3
        j += 1


def main():
    spider_url(root_url, root_dir)
    browser.close()


if __name__ == "__main__":
    main()
