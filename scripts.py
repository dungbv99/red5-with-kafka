import subprocess
import random







def getListContainersRed5Running():
    listContainers = subprocess.check_output(["docker","ps","--format", "'{{.Names}}'"]).replace("'","").split("\n")
    print listContainers
    for container in listContainers:
        if "red5" not in container and container != "haproxy":
            listContainers.remove(container)
    return listContainers



def runGstreamer(listContainers):
    if "haproxy" in listContainers:
        ip =  subprocess.check_output(["docker","inspect","-f","'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","haproxy"]).rstrip("\n").replace("'","")
        location = "location='rtmp://" + ip + "/oflaDemo/red5StreamDemo live=1'"
        subprocess.call(["gst-launch-1.0","autovideosrc","!","videoconvert","!","avenc_flashsv","!","flvmux","!","rtmpsink",location])
    else:
        randomContainer = random.choice(listContainers)
        ip =  subprocess.check_output(["docker","inspect","-f","'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'",randomContainer]).rstrip("\n").replace("'","")
        location = "location='rtmp://" + ip + "/oflaDemo/red5StreamDemo live=1'"        
        subprocess.call(["gst-launch-1.0","autovideosrc","!","videoconvert","!","avenc_flashsv","!","flvmux","!","rtmpsink",location])









listContainersRed5Running = getListContainersRed5Running()
while len(listContainersRed5Running) > 0:
    print listContainersRed5Running
    runGstreamer(listContainersRed5Running)
    listContainersRed5Running = getListContainersRed5Running()

