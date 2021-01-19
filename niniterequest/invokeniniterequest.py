import getopt, sys, os, ctypes, requests, subprocess
from urllib.request import urlopen
from bs4 import BeautifulSoup

if os.name != 'nt':
  print(f'This script is not supported on {os.name} OS')
 
def isAdmin():
  try:
      is_admin = (os.getuid() == 0)
  except AttributeError:
      is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
  return is_admin

if isAdmin() == False:
  print('Script is not running as Administrator')
  print('Please rerun this script as Administrator.')
  sys.exit()

short_options = "i:fs:"
long_options = ["installpath=", "fetchlatestappnames", "specifyapps"]
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

try:
  arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
  print (str(err))
  sys.exit(2)

fetch_apps = False
install_path = 'C:/Kits'
apps_to_install = []
for current_argument, current_value in arguments:
  if current_argument == '-f':
    fetch_apps = True
  elif current_argument == '-i':
    install_path = current_value
  elif current_argument == '-s':
    apps_to_install = current_value.split(',')

def get_latest_ninite_app_list():

  page = requests.get('https://ninite.com')
  soup = BeautifulSoup(page.content, 'html.parser')
  app_list_html = soup.find_all('input',class_='js-homepage-app-checkbox')
  app_list = ''

  for app in app_list_html:
    app_list += app['value'] + ','

  app_list = app_list[:-1]
  f=open('listofapps.txt', 'w')

  f.write(app_list)
  f.close()
  
if fetch_apps:
  get_latest_ninite_app_list()

selected_apps = []
if len(apps_to_install) == 0:

  if os.path.isfile('./listofapps.txt') != True:
    print("listofapps.txt missing in directory")
    print("You can regenerate it by using the -f arg")
    sys.exit()
  
  list_of_apps = open('listofapps.txt')
  list_of_apps = list_of_apps.read()
  list_of_apps = list_of_apps.split(',')
  list_of_apps.sort()

  user_input = None

  print(list_of_apps)
  while user_input != 'done':
    user_input = input("Enter the apps you'd like to install from the list above one at a time, enter done to finish: ")
    if user_input == 'done':
      break
    if(user_input not in list_of_apps):
      print(f'{user_input} was not listed in the apps above')
      continue
    selected_apps.append(user_input)

install_string = ""
if len(selected_apps) > 0:
  for app in selected_apps:
    install_string += app + "-"
else:
  for app in apps_to_install:
    install_string += app + "-"

install_string = install_string[:-1]

if os.path.exists(install_path) != True:
  os.makedirs(install_path)

r = requests.get(f'https://ninite.com/{install_string}/ninite.exe')
with open(f'{install_path}/ninite.exe', 'wb') as f:
  f.write(r.content)

subprocess.call(f'{install_path}/ninite.exe')