# SeqGapStopRemover

 Description
`SeqGapStopRemover` is a Python script designed to clean FASTA sequences by removing gaps and stop codons. It can be run on a single file or on multiple files in a directory.

## Requirements
- Python 3.x

## Basic Usage

### Single File
To run the script on a single FASTA file and save the output to a new file:
 **python SeqGapStopRemover.py input.fasta > output.fasta**


### Multiple Files
To run the script on multiple FASTA files in a directory:
**python SeqGapStopRemover.py --loop input_directory/**


**Advanced Usage**
- See the comments in the `SeqGapStopRemover.py` script for advanced usage options.

## Making the Script Executable

### Step 1: Make the Script Executable
Add a 'shebang' line at the top of the script if it's not there:
#!/usr/bin/env python3

Then make the script executable:
chmod +x SeqGapStopRemover.py


### Step 2: Move to a Folder in PATH or Add Folder to PATH

#### Option A: Move to a Folder in PATH
Move the script to a directory that's already in your PATH (admin rights may be required):

sudo mv SeqGapStopRemover.py /usr/local/bin/SeqGapStopRemover


#### Option B: Add the Script's Folder to PATH
Add the folder where `SeqGapStopRemover.py` resides to your PATH variable. Add the following line to your `.bashrc`, `.zshrc`, or equivalent:

export PATH=$PATH:/path/to/your/script/directory


Then run:
source ~/.bashrc  # Or source ~/.zshrc


After following these steps, you can run the script using the command `SeqGapStopRemover` from any directory.

## Support
For further help, say "Hello to Aqib".

