import requests,sys, os

roll_no= input("Roll no. ")
assign_id = input("Assignment ID: ")
ext = input("Extension: ")

url = f"https://cu.edu.pk/uploads/StudentsAssignments/2024%20Spring/Morning/{roll_no}-CSC-205(L)-SA-{assign_id}.{ext}"

response = requests.get(url)
folder_name = r"C:\Users\ha243\Downloads\assignments"
file_name = f"{roll_no}.{ext}"
os.makedirs(folder_name,exist_ok=True)

full_path = os.path.join(folder_name,file_name)

if response.status_code == 200:
    with open(full_path,"wb") as file:
        file.write(response.content)
        sys.exit("Downloaded 👍🏻")
else:
    sys.exit(f"{response.status_code}:{response.reason} 👎🏻")