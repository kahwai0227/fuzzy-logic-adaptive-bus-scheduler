import matlab.engine

# Start MATLAB Engine
eng = matlab.engine.start_matlab()
pc = 100
# Define input values as a list
input_values = [pc]

# Convert input values to a MATLAB-compatible format (matrix of double values)
input_matrix = matlab.double(input_values)

# Call MATLAB function
print(eng.comp_disp_int(input_matrix))

# Stop MATLAB Engine
eng.quit()