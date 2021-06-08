bug_reports_path="/home/jack/bug_reports"
results_path="/home/jack/results"
codebase_path="/home/jack/codebase"
incbl_root="/home/jack/Blinpy-app"
cd $bug_reports_path
rm -rf $results_path"/runtime.txt"
for folder in `ls $1`
do  
    cd $bug_reports_path"/"$folder
    for bug_pair in `ls $1`
    do  
        firstline=$(echo `sed -n '1p' $bug_reports_path"/"$folder"/"$bug_pair"/""id_time.txt"`)
        lastline=$(echo `sed -n '$p' $bug_reports_path"/"$folder"/"$bug_pair"/""id_time.txt"`)
        echo $firstline
        echo $lastline
        cd $codebase_path"/"$folder
        ver=$(git rev-list --all -n 1 --before="$firstline|cut -d "L" -f 2")
        git reset --hard $ver
        bug=$(echo $firstline|cut -d "L" -f 1)
        python "$incbl_root"/local.py"" "$incbl_root" "$bug_reports_path"/"$folder/$bug_pair/$bug"L"" "/home/jack/codebase/$folder"
        mkdir -p $results_path"/"$folder"/"$bug_pair
        cp -r $incbl_root"/.incbl-data/"$folder"/"* $results_path"/"$folder"/"$bug_pair

        ver=$(git rev-list --all -n 1 --before="$lastline|cut -d "L" -f 2")
        git reset --hard $ver
        bug=$(echo $lastline|cut -d "L" -f 1)
        starttime=$(echo `date +%s.%N`)
        python "$incbl_root"/local.py"" "$incbl_root" "$bug_reports_path"/"$folder/$bug_pair/$bug"L"" "$codebase_path"/"$folder"
        endtime=$(echo `date +%s.%N`)
        runtime=$(echo  "scale=6; $endtime-$starttime" | bc)
        echo "$folder with incremental computing: $runtime" >> $results_path"/runtime.txt"
        rm -rf $incbl_root"/.incbl-data/"$folder
        
        starttime=$(echo `date +%s.%N`)
        python "$incbl_root"/local.py"" "$incbl_root" "$bug_reports_path"/"$folder/$bug_pair/$bug"L"" "$codebase_path"/"$folder"
        endtime=$(echo `date +%s.%N`)
        runtime=$(echo "scale=6; $endtime-$starttime" | bc)
        echo "$folder without incremental computing: $runtime" >> $results_path"/runtime.txt"
        rm -rf $incbl_root"/.incbl-data/"$folder
    done
done
