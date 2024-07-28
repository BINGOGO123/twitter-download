import os

if __name__ == "__main__":
    files = os.listdir("./resources")
    files = [x for x in files if x.endswith(".txt")]
    all_urls = open("all_url.txt", "w", encoding = "utf8")
    for one_name in files:
        f = open("./resources/" + one_name, "r", encoding="utf8")
        datas = f.readlines()
        url = datas[-1].split(" ")[-1].strip()
        if url.startswith("http"):
            all_urls.write("{}:{}\n".format(one_name.split(".")[0], url))
        f.close()
    all_urls.close()