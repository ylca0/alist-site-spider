import os
import requests
from tqdm import tqdm


root_dir = os.getcwd() + "\\" + ""


def deal_file(dir):
    file_list = os.walk(dir)
    for root, dirs, files in file_list:
        # 遍历所有文件，深度优先
        for file in files:
            try:
                # 当前下载的文件绝对路径
                file_name = root + "\\" + file

                # 避免下载已经下载过的文件
                if os.path.getsize(file_name) > 1024:
                    print('[' + file_name + "] is downloaded!")
                    continue

                # 读取没有下载的文件并合成链接
                with open(file_name, "r") as f:
                    link = f.read().split("/")
                    link.insert(3, "d")
                    link = "/".join(link)

                r = requests.get(link, stream=True)

                with open(file_name, "wb") as f:

                    total_size = int(r.headers.get("Content-Length"))
                    # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
                    # iterable：可迭代的进度条 total：总的迭代次数 desc：进度条的前缀
                    for chunk in tqdm(
                        iterable=r.iter_content(1048576),
                        total=total_size // 1048576,
                        unit="m",
                        desc=file_name,
                    ):
                        f.write(chunk)

            except Exception as e:
                print(str(e)[:150], end="")


def main():
    deal_file(root_dir)


if __name__ == "__main__":
    main()
