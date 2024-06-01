import subprocess

# 执行第一个脚本
subprocess.run(['python', 'CreateDatabase.py'])

# 执行第二个脚本
subprocess.run(['python', 'ImportCourse.py'])

# 执行第三个脚本
subprocess.run(['python', 'ImportStudentScores.py'])

subprocess.run(['python', 'ImportEmploymentInfo.py'])

subprocess.run(['python', 'DataReduction.py'])

subprocess.run(['python', 'DataPreparation.py'])
print("data preparation")

subprocess.run(['python', 'DataAnalyse.py'])
print("data analyse")

subprocess.run(['python', 'Prediction_Test.py'])
print("prediciotn test")
