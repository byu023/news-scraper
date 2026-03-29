from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import anthropic
import os
import time

load_dotenv()

def get_reviews(url):
    """ホットペッパーからレビューを取得する"""
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    reviews = driver.find_elements(By.CSS_SELECTOR, "p.mT10.wwbw")
    review_list = [r.text for r in reviews[:5]]
    driver.quit()
    return review_list


def generate_reply(review):
    """Claude APIで返信文を生成する"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"美容サロンのオーナーとして以下の口コミに丁寧な返信を100文字以内で書いてください：\n{review}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"APIエラー：{e}"


def main():
    url = "https://beauty.hotpepper.jp/slnH000376942/review/"
    reviews = get_reviews(url)

    print(f"取得したレビュー数：{len(reviews)}件\n")
    for i, review in enumerate(reviews):
        print(f"--- レビュー{i+1} ---")
        print(f"口コミ：{review[:50]}...")
        reply = generate_reply(review)
        print(f"返信案：{reply}")
        print()


if __name__ == "__main__":
    main()
