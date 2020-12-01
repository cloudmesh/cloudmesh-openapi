
for x in range(0,30):
	bashCmd = ["pytest -v  -s /home/pi/cm/cloudmesh-openapi/tests/test_30_generator_eigenfaces_svm.py"]
	process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
	output, error = process.communicate()
	outF = open("myOutFile.txt", "a")
	for line in output:
  	outF.write(line)
  	outF.write("\n")
	outF.close()







