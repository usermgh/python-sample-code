from datetime import datetime
from tabulate import tabulate  # To format the table

# Sample patient data with specific medical data types
patient_data = {
    'patient_id': 123,
    'name': 'John Doe',
    'age': 30,
    'medical_data': {
        'heart_rate': '75 bpm',
        'blood_pressure': '120/80 mmHg',
        'temperature': '98.6 F',
        'blood_glucose': '90 mg/dL',
        'SpO2': '98%'
    },
    'access_policies': {}
}

# Sample users (user_id: role)
users = {
    'user1': {'role': 'doctor'},
    'user2': {'role': 'nurse'},
    'user3': {'role': 'patient'},
}

# Function to set patient-specific access policies
def set_patient_policy(id_owner, id_user, te, ds, de, data_types, read_permission, write_permission, valid):
    if id_owner == patient_data['patient_id']:
        patient_data['access_policies'][id_user] = {
            'expiration_date': te,
            'data_start': ds,
            'data_end': de,
            'data_types': data_types,  # List of specific data types (e.g., heart rate, blood pressure)
            'read': read_permission,
            'write': write_permission,
            'valid': valid
        }
        return f"Access policies updated for user {id_user}."
    return "Patient not found."

# Function to check if the current date is within the data availability period
def is_within_data_availability(ds, de):
    current_date = datetime.now().date()
    return ds <= current_date <= de

# Function to check if a policy is still valid (not expired or invalidated)
def is_policy_valid(te, valid):
    current_date = datetime.now().date()
    return valid == 1 and current_date <= te

# Function to check access permissions considering all parameters
def can_access(id_owner, id_user, action, data_type):
    if id_owner == patient_data['patient_id']:
        policy = patient_data['access_policies'].get(id_user)
        
        if policy:
            te = policy['expiration_date']
            ds = policy['data_start']
            de = policy['data_end']
            valid = policy['valid']
            allowed_data_types = policy['data_types']
            
            # Check if the policy is valid, within the availability period, and data type is allowed
            if is_policy_valid(te, valid) and is_within_data_availability(ds, de):
                if policy[action] and data_type in allowed_data_types:  # Check read/write permission and data type
                    return True
    return False

# Function to access patient data with all conditions
def access_patient_data(user_id, action, data_type):
    user = users.get(user_id)
    if user:
        id_owner = patient_data['patient_id']
        if can_access(id_owner, user_id, action, data_type):
            return f"Access granted: {action} {data_type} for {user_id}. Data: {patient_data['medical_data'].get(data_type)}"
        else:
            return "Access denied: You do not have permission, wrong data type, or the policy is expired/invalid."
    return "Access denied: User not found."

# Function to get and validate input dates
def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_obj
        except ValueError:
            print("Invalid date format! Please enter the date in YYYY-MM-DD format.")

# Function to configure access policies
def configure_access_policies():
    print("Configuring access policies for each user:")
    
    for user_id in users.keys():
        print(f"\nUser ID: {user_id}")
        te = get_date_input("Enter expiration date of the policy (YYYY-MM-DD): ")
        ds = get_date_input("Enter data availability start date (YYYY-MM-DD): ")
        de = get_date_input("Enter data availability end date (YYYY-MM-DD): ")

        # Get the types of data that user is allowed to access
        data_types = input(f"Enter the types of data {user_id} can access (e.g., heart_rate, blood_pressure, temperature, blood_glucose, SpO2), separate by commas: ").strip().lower().split(',')

        read_permission = input(f"Should {user_id} have read access? (yes/no): ").strip().lower() == 'yes'
        write_permission = input(f"Should {user_id} have write access? (yes/no): ").strip().lower() == 'yes'
        
        # Ensure valid input (1 or 0) for policy validity
        while True:
            valid_input = input(f"Is the policy valid? (1 for valid, 0 for invalid): ")
            if valid_input in ['1', '0']:
                valid = int(valid_input)
                break
            else:
                print("Invalid input! Please enter 1 for valid or 0 for invalid.")
        
        # Set patient-specific policy
        set_patient_policy(patient_data['patient_id'], user_id, te, ds, de, data_types, read_permission, write_permission, valid)

# Function to print access policy table
def print_access_policy_table():
    print("\nAccess Policies:")
    policy_data = []
    
    for user_id, policy in patient_data['access_policies'].items():
        policy_data.append([
            user_id,
            policy['expiration_date'],
            policy['data_start'],
            policy['data_end'],
            ', '.join(policy['data_types']),
            'Yes' if policy['read'] else 'No',
            'Yes' if policy['write'] else 'No',
            'Valid' if policy['valid'] == 1 else 'Invalid'
        ])
    
    # Print the table using tabulate for better readability
    headers = ["User ID", "Expiration Date", "Data Start", "Data End", "Allowed Data Types", "Read Access", "Write Access", "Validity"]
    print(tabulate(policy_data, headers, tablefmt="pretty"))

# Running the program
if __name__ == "__main__":
    # Configure access policies by taking input from the user
    configure_access_policies()
    
    # Print the access policy table
    print_access_policy_table()

    # Test access based on the new policies
    print(access_patient_data('user1', 'read', 'heart_rate'))      # Access test for user1 (doctor) - heart_rate
    print(access_patient_data('user1', 'write', 'blood_pressure'))  # Access test for user1 (doctor) - blood_pressure
    print(access_patient_data('user2', 'write', 'blood_glucose'))  # Access test for user2 (nurse) - blood_glucose
    print(access_patient_data('user3', 'read', 'SpO2'))            # Access test for user3 (patient) - SpO2
