#!/bin/bash
# Function to find PRs by author (same as before)


function find_prs_by_author() {
    local repo="$1"
    local author="$2"

    api_url="https://api.github.com/repos/$repo/pulls?state=all&per_page=100"
    prs=$(curl -s "$api_url" | jq -r '.[] | select(.user.login == "'"$author"'") | [.title, .html_url, .created_at] | @tsv')

    if [ -z "$prs" ]; then
        echo "No PRs found for author '$author' in repository '$repo'."
    else
        echo "### PRs by '$author' in '$repo':"
        echo "$prs" | while IFS=$'\t' read -r title pr_url created_at; do
            echo "- **[$title]($pr_url)** (Created at: $created_at)"
        done
    fi
}
# Hardcoded repository list
repos=("pytorch/xla" "tensorflow/tensorflow" "google/JetStream")

# Hardcoded author list
authors=("will-cromar" "JoeZijunZhou" "qihqi")

# Iterate through repositories and authors
for repo in "${repos[@]}"; do
    for author in "${authors[@]}"; do
        find_prs_by_author "$repo" "$author"
        echo "---------------------------"
    done
done
