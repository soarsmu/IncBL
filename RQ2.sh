
bug_reports_path="/home/incbl_experiment_data/clean_bugzbook/remove_truth"
results_path="/home/incbl_experiment_data/results"
codebase_path="/home/incbl_experiment_data/codebases"
incbl_root="/home/Blinpy-app"

cd $bug_reports_path
pwd

for folder in `ls $1`
do {
    while read -r line
    do
        cd $codebase_path"/"$folder
        ver=$(git rev-list --all -n 1 --before="$line|cut -d "l" -f 2")
        git reset --hard $ver
        cd $bug_reports_path"/"$folder
        bug=$(echo $line|cut -d "l" -f 1)
        python "$incbl_root"/"local.py" "$incbl_root" "$bug_reports_path"/"$folder/$bug""l" "$codebase_path"/"$folder"
    done < $bug_reports_path"/"$folder"/""ver_time.txt"
}  
done
