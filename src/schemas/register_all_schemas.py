import os
import subprocess


try:
    # List all schema registration scripts
    schema_files = [f for f in os.listdir("schemas") if f.startswith('register_') and f.endswith('.py')]
    print(f'Files are : {schema_files}')

    # Run each script
    for file in schema_files:
        if file != "register_all_schemas.py":
            subprocess.run(['python', os.path.join("schemas", file)])
            print(f"Successfully registered schema from {file}")

    print("Schema registration completed.")

except FileNotFoundError:
        print("Error: 'schemas' directory not found.")
except subprocess.CalledProcessError as e:
    print(f"Error: Schema registration failed for {file}. Return code: {e.returncode}")
    print(f"Output: {e.output}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")