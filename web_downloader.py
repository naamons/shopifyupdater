import requests
import configparser

def login_to_website(session, login_url, credentials):
    response = session.post(login_url, data=credentials)
    if response.ok:
        print("Logged in successfully.")
    else:
        print("Login failed.")
        response.raise_for_status()

def download_excel_file(session, download_link, save_path):
    response = session.get(download_link)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded: {save_path}")
    else:
        print("Failed to download the file.")
        response.raise_for_status()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    login_url = config['WebDownloader']['login_url']
    download_link = config['WebDownloader']['download_url']
    credentials = {
        'email': config['WebDownloader']['username'],
        'password': config['WebDownloader']['password']
    }
    save_path = config['Filepaths']['excel_file_path']

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    # Perform login
    login_to_website(session, login_url, credentials)

    # Download file after login
    download_excel_file(session, download_link, save_path)
