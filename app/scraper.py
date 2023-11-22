from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime


class FacebookScraper:

    def __init__(self, fb_link):
        self.fb_link = fb_link
        self.url = "https://fsave.io/"
        self.link = ''
        self.temp = 0
        self.target_text = 'Download'
        self.quality = ['720p', '360p']
        self.videos = {}

    def extract_fb_link(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("detach", False)
        # chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        video_link = self.fb_link

        driver.get(self.url)

        driver.find_element("xpath", '//*[@id="url"]').send_keys(video_link)
        driver.find_element("xpath", '//*[@id="send"]').click()
        now = datetime.now()
        print("Current Time =", now.strftime("%H:%M:%S"))
        driver.implicitly_wait(10)
        matching_links = driver.find_elements(By.XPATH, f'//a[text()="{self.target_text}"]')

        for link in matching_links:
            href = link.get_attribute('href')
            self.videos[f'{self.quality[self.temp]}'] = href
            self.temp += 1

        link = driver.find_element("xpath",
                                   '//*[@id="download-section"]/section/div/div[1]/div[2]/div/table/tbody/tr[1]/td['
                                   '3]/a').get_attribute('href')

        driver.quit()
        return self.videos
