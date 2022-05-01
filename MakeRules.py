#Script for making firewall rules using any FreeBSD router/packet filter (pfctl)

ASCII = '''
ASCII HERE
'''

SERVICES = {
    22:"SSH",
    80:"HTTP"
}

#Creates the rules in a temporary file which will then be written to the final file later
def writeRule(team, pathToFile):
    print("\nWelcome to rule writer!")
    print("You will be prompted to enter the ip, hostname, scored services, and any additional ports to allow.")
    print("To quit, type quit.\n")

    IP = input("Enter IP of machine (or quit): ")

    topology = dict()

    while(IP != "quit"):
        #Ask for hostname
        hostname = input("Enter hostname: ") 

        #Ask for OS
        OS = input("Enter OS: ")

        #Ask for allowed ports and init portString (used in dict)
        allowedPorts = input("Enter allowed ports (seperated by ',' with no spaces): ").split(",")
        portString = ""

        #Write the rule for each port
        with open(pathToFile, "a") as file:
            file.write("\n")
            for port in allowedPorts:
                portString += port + ", "
                try:
                    recognizedPort = "[" + SERVICES[int(port)] + "]"
                except(KeyError):
                    recognizedPort = ""
                file.write("#" + hostname + "(" + OS + ") - " + IP + " on " + port + recognizedPort + "\n")
                file.write("pass in quick proto { tcp udp } from any to " + IP + " port { " + port.strip() + " }" + "\n")

        #Add to topology
        key = hostname + "(" + OS + ")"
        value = IP + "(" + portString.strip(", ") + ")"
        topology[key] = value
        for host in topology:
            print(host + ":" + topology[host])

        #Ask for another box
        IP = input("Enter IP of next machine (or quit): ")

    return topology

def subnetWriter(team, pathToFile):
    #USE IF IP OF BOXES ARE CONSECUTIVE
    return

def main():
    #Ask user for file to save to, default to "etc/pf.conf"
    finalPathToFile = input("Enter a path to save this file to (default: /etc/pf.conf): ") or "/etc/pf.conf"
    #Add all of these rules to a tmp file until we finish
    pathToFile = finalPathToFile.strip() + ".tmp"

    
    #Ask user for ip of router
    routerIp = input("Enter IP of router: ")

    #Ask user for team number
    team = input("Enter team number: ")

    #Create the rules and pull the topology created
    topology = writeRule(team, pathToFile)

    #Print the topology for verification
    for host in topology:
        print(host + ":" + topology[host])

    



if __name__ == "__main__":
    main()