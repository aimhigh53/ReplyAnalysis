from selenium import webdriver
from selenium.common import exceptions
import atexit

def _enable_download_in_headless_chrome(driver: webdriver, download_dir: str):
    """
    :param driver: 크롬 드라이버 인스턴스
    :param download_dir: 파일 다운로드 경로
    """
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_dir
        }
    }
    driver.execute("send_command", params)

def _close_chrome(chrome: webdriver):
    """
    크롬 종료

    :param chrome: 크롬 드라이버 인스턴스
    """

    def close():
        chrome.close()

    return close


def generate_chrome(
    driver_path:str,
    download_path:str,
    headless: bool=False
    ) -> webdriver:
    """
       크롭 웹드라이버 인스턴스 생성

       :param driver_path: 드라이버 경로
       :param download_path: 파일 다운로드 경로
       :param headless: headless 옵션 설정 플래그
       """

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
    options.add_experimental_option('prefs', {
        'download.default_directory': download_path,
        'download.prompt_for_download': False,
    })
    chrome = webdriver.Chrome(executable_path=driver_path, options=options)

    if headless:
        _enable_download_in_headless_chrome(chrome, download_path)

    atexit.register(_close_chrome(chrome))  # 스크립트 종료전 무조건 크롬 종료

    return chrome
