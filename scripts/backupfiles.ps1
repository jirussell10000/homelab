# Powershell version of the bash bk script.

# Description: Stages updated files to be commited via git. Commits the files and uploads them to the specified remote repo.

echo "Staging updated files..."
git add .

echo "Committing files to local repo..."
git commit -m "backup notes"

echo "Pushing updated local repo to remote repo..."
git push

echo "Notes successfully uploaded to remote repo."