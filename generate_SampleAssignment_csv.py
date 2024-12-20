import csv
from faker import Faker

def generate_assignments_csv(filename, num_entries):
    fake = Faker()
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(['participant_uid', 'title', 'content'])
        
        for i in range(1, num_entries + 1):
            participant_uid = f'UID{i:03d}'  # UID001, UID002, ..., UID800
            title = f'Assignment {i}'
            # Generate a realistic paragraph for content using faker
            content = fake.paragraph(nb_sentences=1)  # Adjust number of sentences as needed
            writer.writerow([participant_uid, title, content])

if __name__ == "__main__":
    generate_assignments_csv('assignments_sample.csv', 800)
    print("assignments.csv has been generated with 800 entries.")