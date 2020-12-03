import subprocess

for x in range(0,30):
<<<<<<< HEAD
    print(count, "iteration")
    count += 1
    bashCmd = "pytest -v  -s /home/pi/cm/cloudmesh-openapi/tests/test_030_generator_eigenfaces_svm.py"
    output = Shell.run(bashCmd)
    outF = open("finalOutFile.txt", "a")
    outF.write(str(output))
    outF.flush()
    outF.close()
=======
	bashCmd = ["pytest -v  -s /home/pi/cm/cloudmesh-openapi/tests/test_30_generator_eigenfaces_svm.py"]
	process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
	output, error = process.communicate()
	outF = open("myOutFile.txt", "a")
	for line in output:
  		outF.write(line)
  		outF.write("\n")
outF.close()
>>>>>>> 4509dd11e92953250129d5f561c0c211e49873d2
