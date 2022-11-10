from classes.high_level_csv_page import high_level_csv_page
from classes.DataFilterer import NumericSliderFilterer
from classes.DataFilterer import MultipleTextOptionsFilterer

# Upper level pages need these 2 variables.
name = "toxic_release_inventory"
link = "./?category=chw&dataset=toxic_release_inventory"



def run(params, page_configurations):
    filename = "Toxic Release Inventory.zip"
    page = high_level_csv_page()
    page.setName("Toxic Release Inventory")
    page.setYear("1987-2018")
    page.setDataType(".csv")
    page.setFileName(filename)
    page.setMetadataAvailability(True)
    page.setAdditionalInformation("Information about chemicals and their toxicity from chemicals")
    page.setSource("https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present")
    page.setCloudConfigurations("cedar-datasets", "CEDaR Repository/" + filename, filename, 'application/zip')
    page.setCSVDownloadLink('https://storage.googleapis.com/cedar-datasets/CEDaR%20Repository/tri_UT_all.csv')
    page.setCSVFilename('tri_UT_all.csv')
    filterYear = NumericSliderFilterer("Years:", 1987, 2018, "1. YEAR")
    filterYear = NumericSliderFilterer(":", 1987, 2018, "1. YEAR")
    page.addDataFilterer(filterYear)
    allCounties = ["SALT LAKE", "UTAH", "CACHE" , "WEBER", "BOX ELDER", "DAVIS", "JUAB", 
            "TOOELE", "DUCHESNE", "BEAVER", "CARBON", "SEVIER", "IRON", "WASHINGTON", 
            "SUMMIT", "MORGAN", "SANPETE", "UINTAH", "MILLARD", "EMERY", "SAN JUAN", "GRAND", "WAYNE" ]
    someCounties = ["SALT LAKE", "UTAH", "CACHE" , "WEBER", "BOX ELDER", "DAVIS", "JUAB", 
            "TOOELE", "DUCHESNE", "BEAVER", "CARBON", "SEVIER", "IRON", "WASHINGTON", 
            "SUMMIT", "MORGAN", "SANPETE", "UINTAH", "MILLARD", "EMERY", "SAN JUAN", "GRAND", "WAYNE" ]
    filterCounties = MultipleTextOptionsFilterer("Select Counties:", allCounties, someCounties, "7. COUNTY")
    page.addDataFilterer(filterCounties)
    page.loadPage()