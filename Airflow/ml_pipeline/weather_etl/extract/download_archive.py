from selenium.webdriver.common.by import By
from extract.wait_load_file import wait_load_file


def download_archive(driver, date_from_str, date_to_str, CONFIG):

    driver.get("https://rp5.ru/Weather_archive_in_Moscow")
    driver.find_element(By.ID, "tabSynopDLoad").click()
    
    weather_station = driver.find_element(By.ID, "wmo_id")
    weather_station.clear()
    weather_station.send_keys("27612")
    
    date_from       = driver.find_element(By.ID, "calender_dload")
    date_from.clear()
    date_from.send_keys(date_from_str)
    date_to         = driver.find_element(By.ID, "calender_dload2")
    date_to.clear()
    date_to.send_keys(date_to_str)
    
    driver.find_element(By.XPATH, "//*[text() = 'Select to file GZ (archive)']").click()
    
    driver.find_element(By.XPATH, "//*[text() = 'Download']").click()

    file_path = wait_load_file(folder_path=CONFIG['export_historical_data_path'])

    return file_path