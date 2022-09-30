from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "/Users/devsalvi/Desktop/web scrapping//chromedriver"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q=transparent+background+palm+tree+leaves+png&tbm=isch&hl=en&chips=q:transparent+background+palm+tree+leaves+png,online_chips:green+palm:NHpFSay3YfE%3D&rlz=1C5CHFA_enIN1016IN1016&sa=X&ved=2ahUKEwidqIDw47v6AhU6BLcAHQcJDr0Q4lYoAnoECAEQJw&biw=699&bih=805"

	wd.get(url)

	image_urls = set()


	while len(image_urls) < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails :
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:

				if image.get_attribute('src') in image_urls:
					continue
				
				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)} ")

	return image_urls


def download_image(prefix, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_name = prefix + file_name

		with open(file_name, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 10)

for i, url in enumerate(urls):
	download_image("./mainSpiderPlant/palmTree/palmQAZ", url, str(i) + ".jpg")

wd.quit()