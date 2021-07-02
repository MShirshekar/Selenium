# directed by: Mohammad Shirshekar

import unittest
from array import array

import switch as switch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestCase(unittest.TestCase):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    rule = 1

    def setUp(self):
        self.check = True
        print("Rule " + str(self.rule) + ": \n")

    def test_links_not_images(self):
        driver = self.driver
        image_links = list()
        links = driver.find_elements_by_tag_name("a")
        for link in links:
            if link.get_attribute("href"):
                item = link.get_attribute("href")
                check_image = ".png" in item
                if not check_image:
                    self.check = False
                    print("LINK : " + item)
        self.assertEqual(self.check, True, "Links should not directly target images.")

    def test_attributes_deprecated(self):
        elements = self.driver.find_elements_by_xpath('//*')
        deprecated = ['accept', 'align', 'alink', 'allowtransparency', 'archive', 'axis', 'background',
                      'bgcolor', 'border', 'bordercolor', 'cellpadding', 'cellspacing', 'char', 'charoff',
                      'charset', 'classid', 'clear', 'code', 'codebase', 'codetype', 'color', 'compact',
                      'coords', 'datafld', 'dataformatas', 'datapagesize', 'datasrc', 'declare', 'event',
                      'for', 'frame', 'frameborder', 'height', 'hspace', 'ismap', 'language', 'link',
                      'lowsrc', 'marginbottom', 'marginheight', 'marginleft', 'marginright', 'margintop',
                      'marginwidth', 'methods', 'name', 'nohref', 'noshade', 'nowrap', 'profile',
                      'rules', 'scheme', 'scope', 'scrolling', 'shape', 'size', 'standby', 'summary',
                      'target', 'text', 'type', 'urn', 'usemap', 'valign', 'valuetype', 'version',
                      'vlink', 'vspace', 'width']
        for element in elements:
            attributes = self.driver.execute_script(
                'var items = {};'
                ' for (index = 0; index < arguments[0].attributes.length; ++index) {'
                ' items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value'
                ' };'
                ' return items;', element)
            for attribute in attributes:
                if attribute in deprecated:
                    self.check = False
                    print("ID : " + element.id + " || Attribute : " + attribute)
        self.assertEqual(self.check, True, "Attributes deprecated in HTML5 should not be used.")

    def test_meta_tag(self):
        elements = self.driver.find_elements_by_tag_name('meta')
        for element in elements:
            item = element.get_attribute('http-equiv')
            if item == "refresh" or item == "redirect":
                self.check = False
                print("ID : " + element.id + " || Attribute : " + item)
        self.assertEqual(self.check, True, "Meta tags should not be used to refresh or redirect.")

    def test_style_attribute(self):
        elements = self.driver.find_elements_by_xpath('//*')
        for element in elements:
            item = element.get_attribute("style")
            if item:
                self.check = False
                print("ID : " + element.id + " || Attribute : " + item)
        self.assertEqual(self.check, True, "The ""style"" attribute should not be used.")

    def test_identical_links(self):
        problem_links = list
        links = self.driver.find_elements_by_tag_name('a')
        for link1 in links:
            link1_href = link1.get_attribute('href')
            link1_text = link1.text
            for link2 in links:
                link2_href = link2.get_attribute('href')
                link2_text = link2.text
                if link1.text and link2_text and link1_text == link2_text and link1_href != link2_href:
                    self.check = False
                    print(" same text : " + link1_text + "\n different targets:")
                    print("target one: " + link1_href + "\ntarget two: " + link2_href + "\n")
        self.assertEqual(self.check, True, "Links with identical texts should have identical targets.")

    def tearDown(self):
        if self.check:
            print("Test Pass.")
        else:
            print("\nTest Failed:)")
        TestCase.rule += 1
        if TestCase.rule == 6:
            TestCase.driver.close()


if __name__ == "__main__":
    unittest.main()
