# Script to download .stl models from Thingiverse,
# filter valid models and generate rotation images

python thingiverse_downloader.py --search="$1" --pages $2
python filter.py $1
python stl_to_jpg_auto.py $1