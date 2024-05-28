import subprocess

# 执行第一个脚本
subprocess.run(['python', 'CreateDatabase.py'])

subprocess.run(['python', 'RealtimeDataPreparation.py'])

subprocess.run(['python', 'RealtimePrediction_Test.py'])