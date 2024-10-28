# program_analysis Dynamic Analysis 
# Below is the project structure and what each script does

 src/
  __init__.py
   math_operations.py          # Functions like add, subtract, multiply, divide
  string_operations.py        # Functions for string manipulation (e.g., concatenate, uppercase)
  utils.py                    # Utility functions (e.g., check even/odd)
tests/
   __init__.py
  test_math_operations.py     # Unit tests for math_operations.py
  test_string_operations.py   # Unit tests for string_operations.py
  test_utils.py               # Unit tests for utils.py
analysis_tool.py                # Main script to analyze and trigger tests
dynamic_analysis.py             # Logic for dynamic analysis of code changes

# Clone the reppsitory
git clone https://github.com/MounikaNallamothu11/program_analysis.git
cd program_analysis
# Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install Dependicies
pip install -r requirements.txt
Note: Install manually as of now I didn't add any requirements.txt file
# How to run dynamic analysis:
1. Make changes in any function in src code files (try with single change for the first time)
2. Whichever change you did in src file , make sure you modify test file as well 
   For example, if you change **subtract** function from **math_operations.py** as 
       **"return a-b to return a-b+1"**
   Change the same funtion's unit test case in **test_math_operations.py** to make sure it gives the result as per the calculation **a-b+1**
   Eg:
   Original: self.assertEqual(subtract(5, 3), 2)
             self.assertEqual(subtract(0, 1), -1)
   Modified:self.assertEqual(subtract(5, 3), 3)
            self.assertEqual(subtract(0, 1), 0)


3. Run the specific test you modified before running the whole analysis using the command:
   python3 -m unittest tests/test_math_operations.py

4. Now run the analysis using the command:
   python3 analysis_tool.py
5. The output looks like below:
   Added Methods: []
   Removed Methods: []
   Modified Methods: ['subtract']

**Note: These are just simple functions, complexity to be added.**
   
