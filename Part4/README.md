# HbnB Project - Adrien Vieilledent

## Installation :
You will git clone the repository to get and test my API / front end project  part4 of the HbnB.

- You need to create an executable file **install.sh** :
```bash
touch install.sh &&
chmod u+x install.sh
```

- Then copy inside the **install.sh** this code:

<details>

```bash
#!/bin/bash

# Function to clone the 'part4' folder from the GitHub repository
clone_part4() {
echo "Cloning the 'part4' repository..."
git clone https://github.com/vlldnt/holbertonschool-hbnb.git

# Navigate into the 'part4' folder
cd holbertonschool-hbnb/part4
echo "The 'part4' folder has been cloned and you are now in that folder."

}

# Function to create a virtual environment and install dependencies
setup_venv_and_install_requirements() {
echo "Creating the virtual environment..."

# Create a virtual environment (venv)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
echo "Installing dependencies from 'requirements.txt'..."

# Check if the requirements.txt file exists
if [[ -f "requirements.txt" ]]; then
pip install -r requirements.txt
echo "Dependencies installed successfully."
else
echo "'requirements.txt' file not found."
exit 1
fi
}

# Function to run the API
run_api() {
echo "Starting the API..."

# Run the Python file to start the API
python3 run.py
}

# Run the functions
clone_part4
setup_venv_and_install_requirements
run_api
```
</details>

#### Step of the install.sh :

1. Clone the GitHub repository from vlldnt.
2. Navigate into the holbertonschool-hbnb/part4 folder.
3. Display a message confirming that the part4 folder has been cloned and the current directory is inside it.
4. Create a Python virtual environment using venv.
5. Activate the virtual environment.
6. Install the dependencies needed using `pip install -r requirements.txt`
7. Start the Python script `run.py` to launch the API.


## Usage 

Now you can "Go Live" the `index.html` in your VS Code and 