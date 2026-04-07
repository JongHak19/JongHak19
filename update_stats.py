import requests
import os

# 1. 환경 변수에서 깃허브 토큰 가져오기
TOKEN = os.environ.get('GH_TOKEN')
USERNAME = "JongHak19"
headers = {"Authorization": f"token {TOKEN}"}

def get_stats():
    # GitHub GraphQL API를 사용해 더 상세한 데이터를 가져올 수 있지만, 
    # 처음에는 간단하게 REST API로 내 정보를 가져옵니다.
    user_url = f"https://api.github.com/users/{USERNAME}"
    response = requests.get(user_url, headers=headers).json()
    
    # 예시 데이터: 팔로워 수, 공개 레포 수 등
    followers = response.get('followers', 0)
    repos = response.get('public_repos', 0)
    
    # SVG 이미지 생성 (문자열로 간단히 작성)
    svg_template = f"""
    <svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#282a36" rx="10"/>
      <text x="20" y="40" font-family="Arial" font-size="20" fill="#bd93f9" font-weight="bold">
        🚀 {USERNAME}'s Real-time Stats
      </text>
      <text x="20" y="70" font-family="Arial" font-size="15" fill="#f8f8f2">
        Followers: {followers} | Public Repos: {repos}
      </text>
    </svg>
    """
    
    with open("my_stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    get_stats()
