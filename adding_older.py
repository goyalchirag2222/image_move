import os
from datetime import datetime
import re
from github import Github
import pytz

def process_issue_body(body):
    markdown_pattern = r'!\[(?:.*?)\]\((https?://[^\s)]+\.(?:png|jpg|jpeg|gif))\)'
    html_pattern = r'<img [^>]*src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|gif))["\'][^>]*>'
    
    def replace_path(image_url):
        if 'raw.githubusercontent.com' in image_url:
            url_parts = image_url.split('/')
            try:
                branch_index = url_parts.index('main') if 'main' in url_parts else url_parts.index('master')
                if 'older' not in url_parts:
                    url_parts.insert(branch_index + 1, 'older')
                return '/'.join(url_parts)
            except ValueError:
                return image_url
        return image_url
    
    def replace_markdown(match):
        return f'![ScreenShot of Issue]({replace_path(match.group(1))})'
    
    def replace_html(match):
        return match.group(0).replace(match.group(1), replace_path(match.group(1)))
    
    body = re.sub(markdown_pattern, replace_markdown, body)
    body = re.sub(html_pattern, replace_html, body)
    
    return body

def main():
    github_token = os.getenv('MY_GITHUB_TOKEN')
    if not github_token:
        raise ValueError("MY_GITHUB_TOKEN environment variable is not set")
    
    g = Github(github_token)
    repo = g.get_repo("goyalchirag2222/image_move")
    
    cutoff_date = datetime(2024, 12, 1, tzinfo=pytz.UTC)
    issues = repo.get_issues(state='all')
    
    updated_count = 0
    for issue in issues:
        if issue.body and ('![' in issue.body or '<img' in issue.body):
            try:
                new_body = process_issue_body(issue.body)
                if new_body != issue.body:
                    issue.edit(body=new_body)
                    print(f"Updated issue #{issue.number}: {issue.title}")
                    updated_count += 1
            except Exception as e:
                print(f"Error processing issue #{issue.number}: {str(e)}")
    
    print(f"\nProcess completed. Updated {updated_count} issues.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Script failed: {str(e)}")
        exit(1)
