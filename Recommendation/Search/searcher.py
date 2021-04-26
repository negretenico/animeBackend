from Search.imageScrapper import GoogleImageScraper
import os
class Search():
    def __init__(self):
        self.webdriver_path = os.getcwd() + "\\Search\\webdriver\\chromedriver.exe"
        print(self.webdriver_path)
        self.image_path = os.getcwd() + "\\Images"
        self.min_resolution = (0, 0)
        self.max_resolution = (1920, 1080)
        self.headless = False

    def do_search(self,keywords : str, limits : int, download : bool):
        keywords = keywords.replace("\n","")
        image_scrapper = GoogleImageScraper(self.webdriver_path, self.image_path+"\\"+keywords, keywords, limits, self.headless,
                                            self.min_resolution, self.max_resolution)
        image_urls = image_scrapper.find_image_urls()
        if download:
            image_scrapper.save_images(image_urls)
        return image_urls

search =  Search()
dir = os.getcwd()
i = 0
# with open(dir + "\\rooms.txt", encoding="utf8") as file:
#     for song in file:
#         if i>= 0:
#         i+=1
#             
