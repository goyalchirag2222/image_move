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
    # Updated pattern to handle GitHub URLs correctly
    pattern = r'!\[(?:.*?)\]\((https?://[^\s)]+\.(?:png|jpg|jpeg|gif))\)'
    
    def replace_path(match):
        image_url = match.group(1)
        # Check if it's a GitHub raw URL
        if 'raw.githubusercontent.com' in image_url:
            # Split the URL parts
            url_parts = image_url.split('/')
            # Find the position of 'main' or 'master'
            try:
                branch_index = url_parts.index('main')  # or 'master'
                # Insert 'older' after the branch name if it's not already there
                if 'older' not in url_parts:
                    url_parts.insert(branch_index + 1, 'older')
                # Rejoin the URL without spaces
                new_url = '/'.join(url_parts)
                return f'![ScreenShot of Issue]({new_url})'
            except ValueError:
                return match.group(0)  # Keep original if structure isn't as expected
        return match.group(0)
    
    # First, clean up any malformed URLs (remove spaces)
    body = body.replace(' / ', '/')
    # Then apply our replacement
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
