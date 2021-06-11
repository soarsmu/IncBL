#!/bin/bash
echo "ceate directory to store codebase"
# mkdi /Blinpy-app/evaluation_results/Bugzbook_codebases

cd /home/Blinpy-app/evaluation_results/splitted_reports/


# folder="jcr"
# while read -r line
# do
#     cd /home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder
#     ver=$(git rev-list --all -n 1 --before="$line|cut -d | -f 2")
#     git reset --hard $ver
#     cd /home/Blinpy-app/evaluation_results/splitted_reports/$folde
#     bug=$(echo $line|cut -d "L" -f 1)
#     python "/home/Blinpy-app/local.py" "/home/Blinpy-app" "/home/Blinpy-app/evaluation_results/splitted_reports/$folder/$bug""L" "/home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder"
# done < /home/Blinpy-app/evaluation_results/splitted_reports/$folder"/""id_time.txt"

# for folder in `ls $1`
# do {
#     while read -r line
#     do
#         echo $folder
#         cd /home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder
#         ver=$(git rev-list --all -n 1 --before="$line|cut -d | -f 2")
#         git reset --hard $ver
#         cd /home/Blinpy-app/evaluation_results/splitted_reports/$folde
#         bug=$(echo $line|cut -d "L" -f 1)
#         python "/home/Blinpy-app/local.py" "/home/Blinpy-app" "/home/Blinpy-app/evaluation_results/splitted_reports/$folder/$bug""L" "/home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder"
#         break
#     done < /home/Blinpy-app/evaluation_results/splitted_reports/$folder"/""id_time.txt"
# }  
# done


for folder in `ls $1`
do {
    while read -r line
    do
        cd /home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder
        ver=$(git rev-list --all -n 1 --before="$line|cut -d | -f 2")
        git reset --hard $ver
        cd /home/Blinpy-app/evaluation_results/splitted_reports/$folde
        bug=$(echo $line|cut -d "L" -f 1)
        python "/home/Blinpy-app/local.py" "/home/Blinpy-app" "/home/Blinpy-app/evaluation_results/splitted_reports/$folder/$bug""L" "/home/Blinpy-app/evaluation_results/Bugzbook_codebases/$folder"
    done < /home/Blinpy-app/evaluation_results/splitted_reports/$folder"/""id_time.txt"
}  > /home/Blinpy-app/evaluation_results/text_results/$folder".txt" &
done

# > /home/Blinpy-app/evaluation_results/text_results/$folder".txt" &