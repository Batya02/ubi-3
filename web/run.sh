ids=$(pgrep -f "python3 app.py")
sudo kill -9 $ids;
echo "Process successfull deleted!";

python3 app.py 