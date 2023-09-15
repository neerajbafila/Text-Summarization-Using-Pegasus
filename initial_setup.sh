echo [$(DATE)]: "START"echo [$(DATE)]: "creating environment"
# conda create --prefix ./env python=3.10 -y
# echo [$(date)]: "activate environment"
# source activate ./env
# conda activate ./env
echo [$(date)]: "create folder and file structure"

project_name=textSummarizer
echo [$(date)]: "creating folder "$project_name
mkdir -p $project_name

for dir in components config constants entity exception_and_logger pipeline utils
do
    echo [$(date)]: "creating" $project_name/$dir
    mkdir -p $project_name/$dir
    echo [$(date)]: "Creating __init__.py inside "$project_name/$dir "folders"
    touch $project_name/__init__.py $project_name/$dir/__init__.py
done

# echo [$(date)]: "install requirements"
# pip install -r requirements.txt
echo [$(date)]: "END"
