import requests
import os

TOKEN = os.environ.get('GH_TOKEN')
USERNAME = "JongHak19"
headers = {"Authorization": f"bearer {TOKEN}"}

def get_graphql_data():
    query = """
    query {
      user(login: "%s") {
        repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: STARGAZERS, direction: DESC}) {
          nodes {
            stargazers {
              totalCount
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
        }
        pullRequests(first: 1) {
          totalCount
        }
        issues(first: 1) {
          totalCount
        }
      }
    }
    """ % USERNAME
    
    response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['user']
    else:
        print("Query failed:", response.status_code)
        return None

def generate_svg():
    data = get_graphql_data()
    if not data:
        print("Failed to fetch data")
        return
    
    # 데이터 파싱
    stars = sum(repo['stargazers']['totalCount'] for repo in data['repositories']['nodes'])
    commits = data['contributionsCollection']['totalCommitContributions']
    prs = data['pullRequests']['totalCount']
    issues = data['issues']['totalCount']
    
    # 좀 더 리얼하고 멋진 Dracula 테마 SVG
    svg_template = f"""
    <svg width="350" height="195" viewBox="0 0 350 195" fill="none" xmlns="http://www.w3.org/2000/svg">
      <style>
        .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ff79c6; }}
        .stat-label {{ font: 600 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; fill: #f8f8f2; }}
        .stat-value {{ font: 700 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; fill: #bd93f9; text-anchor: end; }}
      </style>
      <rect x="0.5" y="0.5" width="349" height="194" rx="8" fill="#282a36" stroke="#44475a"/>
      
      <text x="25" y="35" class="header">🚀 {USERNAME}'s GitHub Stats</text>
      
      <!-- Stars -->
      <text x="25" y="80" class="stat-label">⭐ Total Stars Earned:</text>
      <text x="315" y="80" class="stat-value">{stars}</text>
      
      <!-- Commits -->
      <text x="25" y="110" class="stat-label">🔥 Commits (This Year):</text>
      <text x="315" y="110" class="stat-value">{commits}</text>
      
      <!-- PRs -->
      <text x="25" y="140" class="stat-label">💻 Total PRs:</text>
      <text x="315" y="140" class="stat-value">{prs}</text>
      
      <!-- Issues -->
      <text x="25" y="170" class="stat-label">🐛 Total Issues:</text>
      <text x="315" y="170" class="stat-value">{issues}</text>
    </svg>
    """
    
    with open("my_stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    generate_svg()
