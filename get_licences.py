import pandas as pd
from bs4 import BeautifulSoup
import requests

def _get_licence(soup):
    """
    Finds the licence for the package from pypi

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        soup of pypi site for given package

    Returns
    -------
    licence: string
        licence of package
    """

    sidebars = soup.find_all("h3","sidebar-section__title")
    for sidebar in sidebars:
        if sidebar.text == "Meta":
            licence = sidebar.find_next("p").text.split("License: ")[-1]
            break
        else:
            licence = "Can't find"
    return licence

def _get_github(soup):
    """
    Finds the github repo link for a package from pypi if it exists

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        soup of pypi site for given package

    Returns
    -------
    github: string
        github repo link

    """

    sidebars = soup.find_all("h3","sidebar-section__title")
    for sidebar in sidebars:
        if sidebar.text == "Statistics":
            github_api = sidebar.find_next("div").get("data-url")
            if github_api is None:
                github = ""
            else:

                github_split = github_api.split("/")[-2:]
                github = "https://www.github.com/{}/{}".format(github_split[0],github_split[1])
            break
    return github

def get_csv(requirement_dir,dest_dir):
    """
    Gets a csv of licences and github repos for each package in requirements txt

    Parameters
    ----------
    requirements_dir: string
        directory of the requirements.txt file
    dest_dirL string
        directory of the destination csv file

    Returns
    -------
    df: pandas.DataFrame
        dataframe which is the same as the csv file
    """
    root_url = "https://pypi.org/project/"
    rows = []
    with open(requirement_dir, 'r') as file:
        lines = [f.split("\n")[0] for f in file]
    packages = [line for line in lines if len(line.split("#")) == 1 and line != ""]
    
    for package in packages:
        package_list = package.split('==')

        if len(package_list) == 2:
            package_name = package_list[0]
            package_version = package_list[1]
            
        elif len(package_list) == 1:
            package_list = package.split('>=')
            if len(package_list) == 2:
                package_name = package_list[0]
                package_version = package_list[1]
            elif len(package_list) == 1:
                package_name = package_list[0]
                package_version = "Unkown"
        else:
            print("package error")
        
        url = root_url + package_name
        
        page = requests.get(url)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        if soup.title.text.find("404") != -1:
            print("{} not found on pypi".format(package_name))
            licence = "Unknown"
            github = "Unknown"
        else:    
            licence = _get_licence(soup)
            github = _get_github(soup)
        
        row = [package_name,package_version,licence,url,github]
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.columns = ["Package","Version","Licence","URL","Gitbub"]
    df.to_csv(dest_dir)
    
    return df
