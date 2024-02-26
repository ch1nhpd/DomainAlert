echo 'start'
git add .
current_time=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "auto $current_time"
git push
