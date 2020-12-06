from cloudmesh.common.Shell import Shell
count = 1
for x in range(0,30):
    print(count, "iteration")
    count += 1
    bashCmd = "pytest -v  -s /home/pi/cm/cloudmesh-openapi/tests/test_030_generator_eigenfaces_svm.py"
    output = Shell.run(bashCmd)
    outF = open("myOutFile4.txt", "a")
    outF.write(str(output))
    outF.flush()
    outF.close()
