# LPF Project

An online platform to manage participants, handle assignment submissions, facilitate peer reviews, and provide analytics on the review process.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/RajThak-998/lpf_project.git
   cd lpf_project


2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   

3. **Setup Database**
   ```python
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'lpf_db',          # The name of your PostgreSQL database
         'USER': 'lpf_user',        # The PostgreSQL user you created
         'PASSWORD': 'your_pass',    # The password for the PostgreSQL user
         'HOST': 'localhost',
         'PORT': '5432',
      }
   }
   ```
      **run the migration**
      ```bash 
      python manage.py migrate
      ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser

5. **Run the server**
   ```bash
   python manage.py runserver

***


## API Endpoints
   
### Participants

   * List Participants
   ```http
   GET /api/participants/
   ```
   * Retrieve a Participant
   ```http
   GET /api/participants/{id}/
   ```
   * Create a Participant
   ```http
   POST /api/participants/
   ```
   * Update a Participant
   ```http
   PUT /api/participants/{id}/
   ```
   * Delete a Participant
   ```http
   DELETE /api/participants/{id}/
   ```

### Assignments
   
   * List Assignments
   ```http
   GET /api/assignments/assignments/
   ```
   * Retrieve an Assignment
   ```http
   GET /api/assignments/assignments/{id}/
   ```
   * Create an Assignment
   ```http
   POST /api/assignments/assignments/
   ```
   * Update an Assignment
   ```http
   PUT /api/assignments/assignments/{id}/
   ```
   * Delete an Assignment
   ```http
   DELETE /api/assignments/assignments/{id}/
   ```

### Reviews

   * List Reviews
   ```http
   GET /api/assignments/reviews/
   ```
   * Retrieve a Review
   ```http
   GET /api/assignments/reviews/{id}/
   ```
   * Create a Review
   ```http
   POST /api/assignments/reviews/
   ```
   * Update a Review
   ```http
   PUT /api/assignments/reviews/{id}/
   ```
   * Delete a Review
   ```http
   DELETE /api/assignments/reviews/{id}/
   ```

### Analytics
   * Participant Progress
   ```http
   GET /api/analytics/participant-progress/
   ```
   * Assignment Status
   ```http
   GET /api/analytics/assignment-status/
   ```
   * Assignment Submission Status
   ```http
   GET /api/analytics/assignment-submission-status/
   ```

### Management commands 

#### Import participants
```bash
python manage.py import_participants --file=path/to/file.csv
```
##### Options
   * ```--dry-run```: Run the import without making any changes to the database.
   * ```--batch-size```: Number of records to process in each batch (default: 200).

#### Import Assignments
```bash
python manage.py import_assignments --file=path/to/file.csv
```
##### Options
   * ```--dry-run```: Run the import without making any changes to the database.
   * ```--batch-size```: Number of records to process in each batch (default: 200).

#### Assign Reviews
```bash
python manage.py assign_reviews --reviews_per_participant=3 --reviews_per_assignment=2
```
##### Options
   * ```--reviews_per_participant```: Number of reviews each participant should perform (default: 3).
   * ```---reviews_per_assignment```: Minimum number of reviews each assignment should receive (default: 2).



### Additional Information

* The project uses Django REST Framework for building the APIs.
* The project uses PostgreSQL as the database.
* The project includes management commands for importing participants and assignments from CSV files and assigning peer reviews.


*For more details, refer to the source code and the comments within the code.*


