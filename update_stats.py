import os
import requests


# GitHub Actions에서 자동으로 제공되는 GITHUB_TOKEN 사용
TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "JongHak19"

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def get_graphql_data():
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN 환경변수가 설정되지 않았습니다.")

    query = """
    query($username: String!) {
      user(login: $username) {
        repositories(
          first: 100
          ownerAffiliations: OWNER
          orderBy: {
            field: STARGAZERS
            direction: DESC
          }
        ) {
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
    """

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-stats-action",
    }

    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json={
            "query": query,
            "variables": {
                "username": USERNAME,
            },
        },
        headers=headers,
        timeout=30,
    )

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            "GitHub API가 JSON 형식이 아닌 응답을 반환했습니다. "
            f"HTTP {response.status_code}: {response.text}"
        ) from error

    if response.status_code != 200:
        raise RuntimeError(
            f"GitHub API 요청에 실패했습니다. "
            f"HTTP {response.status_code}: {result}"
        )

    # GraphQL은 일부 데이터에 문제가 있어도 HTTP 200을 반환할 수 있습니다.
    if result.get("errors"):
        print("GitHub GraphQL warnings:", result["errors"])

    data = result.get("data") or {}
    user = data.get("user")

    if user is None:
        raise RuntimeError(
            f"GitHub 사용자 데이터를 가져오지 못했습니다: {result}"
        )

    return user


def generate_svg():
    data = get_graphql_data()

    # GitHub GraphQL 응답의 nodes에 null이 들어오는 경우를 제외합니다.
    repositories_data = data.get("repositories") or {}
    repositories = repositories_data.get("nodes") or []

    stars = sum(
        (repo.get("stargazers") or {}).get("totalCount", 0)
        for repo in repositories
        if repo is not None
    )

    contributions = data.get("contributionsCollection") or {}
    pull_requests = data.get("pullRequests") or {}
    issues_data = data.get("issues") or {}

    commits = contributions.get("totalCommitContributions", 0)
    prs = pull_requests.get("totalCount", 0)
    issues = issues_data.get("totalCount", 0)

    svg_template = f"""\
<svg width="350" height="195" viewBox="0 0 350 195"
     fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #ff79c6;
    }}

    .stat-label {{
      font: 600 14px 'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif;
      fill: #f8f8f2;
    }}

    .stat-value {{
      font: 700 14px 'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif;
      fill: #bd93f9;
      text-anchor: end;
    }}
  </style>

  <rect
    x="0.5"
    y="0.5"
    width="349"
    height="194"
    rx="8"
    fill="#282a36"
    stroke="#44475a"
  />

  <text x="25" y="35" class="header">
    🚀 {USERNAME}'s GitHub Stats
  </text>

  <!-- Stars -->
  <text x="25" y="80" class="stat-label">
    ⭐ Total Stars Earned:
  </text>
  <text x="315" y="80" class="stat-value">
    {stars}
  </text>

  <!-- Commits -->
  <text x="25" y="110" class="stat-label">
    🔥 Commits (This Year):
  </text>
  <text x="315" y="110" class="stat-value">
    {commits}
  </text>

  <!-- Pull requests -->
  <text x="25" y="140" class="stat-label">
    💻 Total PRs:
  </text>
  <text x="315" y="140" class="stat-value">
    {prs}
  </text>

  <!-- Issues -->
  <text x="25" y="170" class="stat-label">
    🐛 Total Issues:
  </text>
  <text x="315" y="170" class="stat-value">
    {issues}
  </text>
</svg>
"""

    with open("my_stats.svg", "w", encoding="utf-8") as file:
        file.write(svg_template)

    print("GitHub stats SVG generated successfully.")
    print(
        f"Stars: {stars}, Commits: {commits}, "
        f"PRs: {prs}, Issues: {issues}"
    )


if __name__ == "__main__":
    generate_svg()
