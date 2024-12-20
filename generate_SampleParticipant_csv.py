import csv
from faker import Faker

# generates the fake csv data (size = 800)
# to generate use python filename.py

def generate_csv(filename, num_users):
    fake = Faker()
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(['uid', 'name', 'email'])
        
        # Generate user data
        for i in range(1, num_users + 1):
            uid = f'UID{i:03d}'  # UID001, UID002, ..., UID800
            name = fake.name()
            email = fake.unique.email()
            writer.writerow([uid, name, email])

if __name__ == "__main__":
    generate_csv('participants_sample.csv', 800)
    print("sample.csv has been generated with 800 users.")