# -*- coding: utf-8 -*-
"""
Created on 2020
@author: TAING
"""

import time
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions  
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import requests # to sent GET requests
import urllib.request
import urllib.parse


def generate_number_delay(mean = 4, sigma = 0.8):
    """
    Retourne un chiffre aléatoire suivant une distribution normal de moyenne 4 secondes et d'écart type de 0.8
    Ce chiffre aléatoire est le délai après chaque clic. Le but est de simuler le comportement d'un humain:
    un délai fixe peut attirer l'attention des contrôleurs, tout comme un délai aléatoire d'une distribution uniforme
    """
    delay = np.random.normal(mean,sigma,1)[0]
    if delay < 0.2: # relancer si inférieur à 0.2
        delay = np.random.normal(mean,sigma,1)[0]
        return delay
    else:
        return delay
    

# dictionnaire: en clé, le nom de la colonne de la dataframe, en valeurn leur xpath, class ou selecteur css sur le site internet

d_xpath = {'Job Title':'.//h1[contains(@class,"JobInfoHeader")]',  
       'Name Company':'.//div[contains(@class,"icl-u-lg-mr--sm icl-u-xs-mr--xs")]', 
       'Location':'//div[contains(@class,"jobsearch-InlineCompanyRating")]/div[4]', 
       'Descriptions': '//*[@id="jobDescriptionText"]', 

}

skills = ['Python', 'R', 'SQL', 'NoSQL', 'GIT', 'Spark', 'Flask', 'Streamlit', 
          'Docker', 'docker', 'Kubernetes', 'ReactJS', 'Machine Learning', 'Deep Learning',
          'NLP', 'VueJS', 'AngularJS', 'Scala', 'PySpark', 
          'PowerBI', 'SQLServer', 'Dataiku', 'Keras', 'TensorFlow', 'NLU', 'Pytorch', 'PyTorch', 
          'ScikitLearn', 'Scikit-Learn', 'SAS', 'Java', 'java', 'Scikit learn', 'Hadoop', 'hive',
          'Hive', 'ML DL', 'Azure', 'AWS']

def update_dic(dic, column, d):
    """
    Met à jour le dictionnaire d à chaque fiche (cf boucle while plus bas)
    dic: dictionnaire, soit d_id, d_class_name
    column: nom de la colonne de la dataframe et de la clé du dictionnaire
    """
    if dic == d_xpath:
        try:
            d[column] = browser.find_element_by_xpath(dic[column]).text
        
        except NoSuchElementException:
            try: 
                if column == 'Location':
                    d[column] = browser.find_element_by_xpath('//div[contains(@class,"jobsearch-InlineCompanyRating")]/div[3]').text
                
            except NoSuchElementException:
                d[column] = 'Non reference'
    return d


def returninfojob(d):
    """
    Retourne un dictionnaire contenant toute les informations nécessaires pour les offres d'emploi
    """
    d = update_dic(d_xpath,'Job Title', d)
    d = update_dic(d_xpath,'Name Company', d)
    d = update_dic(d_xpath,'Location', d)
    d = update_dic(d_xpath,'Descriptions', d)
    return d


def get_liste_link():
    """
    Retourne la liste de tout les objets selenium correspondant aux liens pour accéder aux annonces
    """
    elems = browser.find_elements_by_css_selector("[data-tn-element='jobTitle']")
    tab_url = [elem.get_attribute(name="href") for elem in elems]
    return tab_url




delays = [7, 4, 6, 2, 10, 19]
delay = np.random.choice(delays)
time.sleep(delay)

browser = webdriver.Chrome()
browser.get('https://www.indeed.fr')
browser.maximize_window()
time.sleep(generate_number_delay())


name_csv = 'indeed_df.csv'

try:
    df_indeed = pd.read_json(name_csv)
except:
    df_indeed = pd.DataFrame(columns=['Job Title', 'Name Company','Location','Descriptions'])
    """
    df_indeed = {'Job Title': [], 'Name Company': [], 'Location': [], 'Links': [], 'Review': [], 'Salary': [], 'Descriptions': [],
               'Python': [], 'R': [], 'SQL': [], 'NoSQL': [], 'GIT': [], 'Spark': [], 'Flask': [], 'Streamlit': [], 'Docker': [], 'Kubernetes': [],
               'React': [], 'VueJS': [], 'AngularJS': [],
               'Machine Learning': [], 'Deep Learning': [], 'NLP': [],  'Scala': [], 'PySpark': [],
               'PowerBI': [], 'SQLServer': [], 'Dataiku': [], 'Keras': [], 'TensorFlow': [], 'NLU': [],
               'PyTorch': [], 'ScikitLearn': [], 'Scikit-Learn': [], 'SAS': [],
               'Java': [], 'Scikit learn': [], 'Hadoop': [],  'Hive': [], 'ML DL': [], 'Azure': [], 'AWS': []
               }
    """
# Write your keyword's jobs
inputElement_what = browser.find_element_by_xpath('//*[@id="text-input-what"]')
inputElement_what.send_keys('Data Scientist')
time.sleep(generate_number_delay())

# Write your localisation
inputElement_where = browser.find_element_by_xpath('//*[@id="text-input-where"]')
inputElement_where.send_keys('Île-de-France')
time.sleep(generate_number_delay())

# click submit button
submit_button = browser.find_element_by_class_name('icl-Button')
submit_button.click()
time.sleep(generate_number_delay())

# click day filter
date = browser.find_element_by_id('filter-dateposted').click()

one_day = browser.find_element_by_partial_link_text('Dernières').click()
#three_days = browser.find_element_by_partial_link_text('3 derniers jours').click()
#seven_days = browser.find_element_by_partial_link_text('7 derniers jours').click()
#fourteen_days = browser.find_element_by_partial_link_text('14 derniers jours').click()

try:
    time.sleep(generate_number_delay())
    browser.find_element_by_class_name('popover-x-button-close').click()
except:
    pass

page = True

links =[]
#descriptions=[]

while page:
    i = 0 # i est le compteur de lien des annonces par page
    while i<len(get_liste_link()): # parcours tout les liens de la page, tant que i est plus petit que le nombre de liens
        liste_element = get_liste_link() # nécessaire de mettre à jour cette liste dans la boucle car ses éléments sont périmés à chaque rafraichissement ou back
        print(liste_element[i]) # affiche l'élement qui va être cliqué
        print(i) # affiche l'élement qui va être cliqué


        # Au cas où y a un pop up
        try:
            pop_up = browser.find_element_by_css_selector('#popover-x > a > svg > g > path')
            pop_up.click()
            time.sleep(generate_number_delay())
        except:
            pass


        browser.execute_script("window.open('');") # Switch to the new window and open URL B
        browser.switch_to.window(browser.window_handles[1])
        browser.get(liste_element[i]) # Each url of list
        time.sleep(generate_number_delay())
         


        # get info job
        try:
            d = {}
            d = returninfojob(d)

            links.append(liste_element[i])
            
            df_indeed = df_indeed.append(d, ignore_index=True)
            df_indeed['Link']= links

            print('ok')
            time.sleep(generate_number_delay())
            i+=1
            df_indeed.to_csv(name_csv, index=False, encoding='utf-8') # sauvegarde en cours
            browser.back()
            time.sleep(generate_number_delay())

        except ElementClickInterceptedException:
            pop_up = browser.find_element_by_css_selector('#popover-x > a > svg > g > path')
            pop_up.click()
            time.sleep(generate_number_delay())

        browser.close() # Switch back to the first tab with URL A
        browser.switch_to.window(browser.window_handles[0])
        
    # aller à la page suivante    
    try:
        next_page = browser.find_element_by_xpath("//a[@aria-label='Suivant'] | a[contains(text(),'Suivant')] ").get_attribute(name="href")
        browser.get(next_page)
        time.sleep(generate_number_delay())
    
    except NoSuchElementException:
        page = False
        print("End")

    except TimeoutException:
        page = False
        print("Toutes les pages ont été visité")
        #break