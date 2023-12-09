import sys
# We import sys so we later use it for taking the input file name as a spacial variable

### The general idea behind this script is to create  helper functions for different tasks (such as reading fasta file, hydrapathy calculation, cvs file generation and plot) and finaly we write a main function that takes all the helper functions  and arrange them so that we get the results as we want. Therefore, we first will have a read_fasta function that takes sequence as input and read the sequence, then calculate_hydrapathy that takes the output of the read_fasta and return the values for each AA individually, and finally a funtion to save the output of the hydrapathy for each protein in a csv file and a function to plot it.



# Here is two ways to create a function to read Fasta file, the first one is commented, however the first one is based on the fact that the given fasta file contains only one sequence, therefore, the first line is header.
#------------------------------------------------------------------------------------ Read Fasta File --------------------------------------------------
#def read_fasta(input_file):
#    with open(input_file, 'r') as f:
#       lines = f.readlines()
#   # We assuming there is only one sequence in the file

#   sequence = ''.join(line.strip() for line in lines[1:])
 #   return sequence

# The following is the second function to read fasta file named "input_file" here, and the idea here is that as the fasta file contains only one sequence, the line starting with ">" is header. 

def read_fasta(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # we initialize an empty sequence so we fill it with the fasta data
    sequence = ""

    # We iterate through lines and extract sequence
    for line in lines:
        # Here we check if the line starts with '>'
        if line.startswith('>'):
            # This line is a header, skip it
            continue
        # We concatenate all the sequence into a sequence named "sequence" here
        sequence += line.strip()
	# We return the sequence as output of this helper function 
    return sequence



#---------------------------------------------------------------- Hydrapathy calculation -------------------------------------------------------
# Here is the function to calculate hydropathy for an amino acid: We have a hashmap and the function returns the value for a given amino acid  named "aa" using this hashmap
def calculate_hydropathy(aa):
    hydropathy_values = {
        'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5,
        'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4,
        'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
        'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8,
        'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
    }
    return hydropathy_values.get(aa, 0)



#------------------------------------------  CSV file with three columns, amino acid, position and value-----------------
# Function to write CSV file: it takes the "hydrapathy_data" as input and generates a csv file named "output_file"  
def write_csv(output_file, hydropathy_data):
    with open(output_file, 'w') as csv_file:
        # Here we create the header then we have a for loop to write the resluts line by line 
        csv_file.write("AA,Position,Hydropathy\n")
        for row in hydropathy_data:
            csv_file.write(','.join(map(str, row)) + '\n')



#---------------------------------------------------------------------------- Our function to plot the values --------------------------------------------
# Here we have the function to plot data using matplotlib, note that here we need to import matplotlib as the standard way to be able to plot something in python, pleas make sure you have this library installed beforehand. Variables include position of each AA named "positions", and the "hydrapathy_values" for the AA plus a "plot_file" as the name of the .png file to be saved  
def plot_data(positions, hydropathy_values, plot_file):
    import matplotlib.pyplot as plt

    plt.plot(positions, hydropathy_values, marker='o', linestyle='-')
    plt.xlabel('Position')    # The label for x axis
    plt.ylabel('Hydropathy')    # # The label for y axis
    plt.title('AA Hydropathy by Position')   # Title of our plot
    plt.savefig(plot_file)   # saving our plot 
    plt.show()    # Showing our plot in a popped up window 


#--------------------------------------------------------------- Our main function to take the helper functions ------------------------------------------
# Here is our main function that arrages all the helper functions; in essence it takes the input file name, and gives us the csv and plot files.
def main(input_file, output_file, plot_file):
    sequence = read_fasta(input_file)    # Reading the input file here
    hydropathy_data = [(aa, i + 1, calculate_hydropathy(aa)) for i, aa in enumerate(sequence)]  # This is a compact form of for loop in python, which simultaneously goes over index and the data
    write_csv(output_file, hydropathy_data)

    positions, hydropathy_values = zip(*[(i + 1, hydropathy) for _, i, hydropathy in hydropathy_data])   # Here we read the second and third columns of the "hydrapathy_data" for and put them into two variables
    plot_data(positions, hydropathy_values, plot_file)



#--------------------------------------------------- Calling the main function -------------------------------------------------------------------
# Here we have the Command-line argument check to make sure the user is giving the name of the fasta file, and after that we call the main function and give the input file to it so it returns the resulst 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You should provide the input file name: python script.py input.fasta")
        sys.exit(1)
        
        # Here we read input file name as a special variable argv, then we specify the name of the outputs 
    input_file = sys.argv[1]
    output_file = "output_table.csv"
    plot_file = "hydropathy_plot.png"

    main(input_file, output_file, plot_file)

