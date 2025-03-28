# RANsomCheck-Backend
## environment
1. conda create --name python=3.12
2. conda activate name
3. conda install numpy pytorch torchvision -c pytorch
4. pip install flask requests python-dotenv
## service
1. conda activate backend
2. cd /home/ubuntu/project/RANsomCheck-Backend
3. flask run
## background program
1. tmux at -t backend
   flask run
2. tmux at -t cuckoo
   cuckoo -d
3. tmux at -t cuckooProcess
   cuckoo process p1d
4. tmux at -t cuckooAPI
   cuckoo api -H 140.124.181.155 --port 1337 
