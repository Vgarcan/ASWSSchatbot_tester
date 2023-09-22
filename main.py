### Modulo REQUESTS ###
#######################

import requests

response = requests.get('https://aswss.com/chatbots/v4/script2.js')

if response.status_code == 200:
    print ('Connection made:\n#-----#-----#-----#-----#-----#')
    
    # Encuentra la posición del primer ';'
    first_semicolon_index = response.text.find(';')
    # Copia el contenido hasta el primer ';'
    copied_content = response.text[:first_semicolon_index]


    import json
    json_content = copied_content.replace("const userMessage =", "q =").strip()
    json_content = json_content.replace("keywords:", '"keywords":')
    json_content = json_content.replace("responses:", '"responses":')
    

    with open('questions.py', 'w') as file:
        file.write(json_content)

elif response.status_code != 200:
    print ('Couldn\'t make connection made:\n#-----#-----#-----#-----#-----#')
    print (response.status_code)


### Modulo SELENIUM ###
#######################

## importamos WEBDRIVER 
from selenium import webdriver 
## Importamos el uso del BY para ser usado mas adelante 
from selenium.webdriver.common.by import By 


## Establecemos opcipones para que el WEBDRIVER mantenga la ventana abierta
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default")


## La siguiente variable guardara el WEBDRIVER con el browser the nuestra eleccion al cual le adjuntaremos nuestras preferencias
driver = webdriver.Chrome(options=chrome_options)


## Usamos el driver para obtener la URL deseada
driver.get('https://aswss.com/chatbots/v4/')


## USERS ACTIONS
USER_TEXT_BOX = driver.find_element(By.ID, "input")
SEND_MESSAGE = driver.find_element(By.TAG_NAME, "button")


import time
from questions import q
with open('info.json', 'a') as info:

    info.write('{')
    for question_set in q:

        info.write("\n    'keywords' : [")

        list_counter = 0
        for user_keywords in question_set['keywords']:
            USER_TEXT_BOX.send_keys(question_set['keywords'][list_counter])
            SEND_MESSAGE.click()
            time.sleep(2)
            ## BOT'S ANSWERS
            Bot_Answers = driver.find_elements(By.ID, "bot-response")  


            if Bot_Answers[-1].text in question_set['responses']:
                info.write('ok')
            else:
                info.write('WRONG')


            if list_counter + 1 !=len(question_set['keywords']):
                info.write(',')
            else:
                info.write('],')

            list_counter +=1

    info.write('}')


driver.quit()