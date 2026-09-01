"""Optional browser-assisted doctor-page search.

This module intentionally stops before any appointment confirmation.
"""

import time
from datetime import datetime, timedelta


def find_doctor_page(department, selected_date, search_url):
    if not department:
        raise ValueError("A department is required")
    if not search_url:
        raise ValueError("BOOKING_SEARCH_URL is not configured")

    start_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=17)
    today = datetime.today().date()
    first_offset = max(0, (start_date - today).days)
    last_offset = first_offset + (end_date - start_date).days

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Edge()
    try:
        driver.get(search_url)
        time.sleep(5)
        hospitals = driver.find_elements(
            By.CSS_SELECTOR,
            ".hospital-list.c-gap-inner-left-boundary.c-gap-inner-right-boundary > div",
        )
        for hospital in hospitals:
            try:
                hospital.click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, ".gh-search").click()
                search_box = driver.find_element(By.CSS_SELECTOR, ".gh-search > div > input")
                search_box.send_keys(department)
                search_box.send_keys("\ue007")

                for offset in range(first_offset, last_offset + 1):
                    try:
                        driver.find_element(By.CSS_SELECTOR, "#date-%d" % offset).click()
                        experts = driver.find_elements(
                            By.CSS_SELECTOR,
                            ".expert-list.static-padding.consult.experiment",
                        )
                        if experts:
                            experts[0].click()
                            time.sleep(1)
                            return driver.current_url
                    except Exception:
                        continue
                driver.back()
            except Exception:
                continue
        return ""
    finally:
        driver.quit()
