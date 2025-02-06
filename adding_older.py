import os
from datetime import datetime
import re
from github import Github
import pytz

def process_issue_body(body):
    """
    Process the issue body to update image paths.
    Adds '/older' before image.png in markdown image links.
    """
    pattern = r'!\[.*?\]\((.*?\.(?:png|jpg|jpeg|gif))\)'
    
    def replace_path(match):
        image_path = match.group(1)
        path_parts = image_path.split('/')
        if 'older' not in path_parts:
            if len(path_parts) == 1:
                return f'![](older/{image_path})'
            else:
                path_parts.insert(-1, 'older')
                return f'![]{"/".join(path_parts)}'
        return match.group(0)
    
    return re.sub(pattern, replace_path, body)

def main():
    # Get GitHub token from environment variable
    github_token = os.getenv('MY_GITHUB_TOKEN')
    if not github_token:
        raise ValueError("MY_GITHUB_TOKEN environment variable is not set")
    
    # Initialize GitHub client and specify the repository
    g = Github(github_token)
    repo = g.get_repo("goyalchirag2222/image_move")  # Direct repository reference
    
    # Set cutoff date (December 2024)
    cutoff_date = datetime(2024, 12, 1, tzinfo=pytz.UTC)
    
    # Get all issues
    issues = repo.get_issues(state='all')
    
    updated_count = 0
    for issue in issues:
        # Skip issues created after December 2024
        # if issue.created_at >= cutoff_date:
        #     continue
            
        # Check if the issue body contains image links
        if '![' in issue.body and '.png' in issue.body.lower():
            try:
                # Process the issue body
                new_body = process_issue_body(issue.body)
                
                # Update the issue only if changes were made
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
