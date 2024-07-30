import requests
from selenium.webdriver.common.by import By

from webreg.utils import get_driver

res = requests.post(
    "https://anc.ca.apm.activecommunities.com/burnaby/rest/activities/list",
    data="""{
  "activity_search_pattern": {
    "skills": [],
    "time_after_str": "",
    "days_of_week": null,
    "activity_select_param": 2,
    "center_ids": [
      "50"
    ],
    "time_before_str": "",
    "open_spots": "",
    "activity_id": null,
    "activity_category_ids": [],
    "date_before": "",
    "min_age": null,
    "date_after": "",
    "activity_type_ids": [],
    "site_ids": [],
    "for_map": false,
    "geographic_area_ids": [],
    "season_ids": [],
    "activity_department_ids": [],
    "activity_other_category_ids": [
      "3"
    ],
    "child_season_ids": [],
    "activity_keyword": "volleyball",
    "instructor_ids": [],
    "max_age": null,
    "custom_price_from": "",
    "custom_price_to": ""
  },
  "activity_transfer_pattern": {}
}""",
    headers={
        "Content-Type": "application/json",
    },
)

body = res.json()["body"]
res = filter(lambda x: int(x["openings"]) > 0, body["activity_items"])
print(list(res))


# driver = get_driver(headless=False)
# driver.get("https://anc.ca.apm.activecommunities.com/burnaby/signin")

# # email
# driver.find_element(
#     By.CSS_SELECTOR,
#     "input[aria-errormessage='signin_login_errorMsg']",
# ).send_keys("dimasoltusyuk@gmail.com")

# # password
# driver.find_element(
#     By.CSS_SELECTOR,
#     "input[aria-errormessage='signin_password_errorMsg']",
# ).send_keys("123Asd_123")

# # submit
# driver.find_element(
#     By.CSS_SELECTOR,
#     "button[type='submit']",
# ).click()
