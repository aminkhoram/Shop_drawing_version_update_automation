import os
import ezdxf
import re
import datetime
import subprocess

def convert_dwg_to_dxf(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.dwg'):
            # Load DWG file
            TEIGHA_PATH = "C:\Program Files\ODA\ODAFileConverter 25.2.0\ODAFileConverter.exe"
            INPUT_FOLDER = folder_path  # Use the provided folder_path
            OUTPUT_FOLDER = output_folder  # Use the provided output_folder
            OUTVER = "ACAD2018"
            OUTFORMAT = "DXF"
            RECURSIVE = "0"
            AUDIT = "1"
            INPUTFILTER = "*.DWG"

            # Command to run
            cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]

            # Run
            subprocess.run(cmd, shell=True)

# Function to detect DXF files in a specific path
def find_dxf_files(folder_path):
    dxf_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.dxf'):
            dxf_files.append(os.path.join(folder_path, filename))
    return dxf_files


# Function to find and print text entities (both single-line text and MTEXT) outside of blocks
def print_text_entities_outside_blocks(doc):
    outside_block_entities = []
    for entity in doc.entities:
        if entity.dxftype() in ['TEXT', 'MTEXT']:
            outside_block_entities.append(entity)
    print("Text entities outside of blocks:")
    for entity in outside_block_entities:
        if entity.dxftype() == 'TEXT':
            text = entity.dxf.text
        elif entity.dxftype() == 'MTEXT':
            text = entity.plain_text()
        print("Found text entity:", text)
#
#
# # Function to print all found text entities (both single-line text and MTEXT)
def print_text_entities(entities):
    for entity in entities:
        if entity.dxftype() == 'TEXT':
            text = entity.dxf.text
        elif entity.dxftype() == 'MTEXT':
            text = entity.plain_text()
        print("Found text entity:", text)


# Function to modify text entities in DXF files
def modify_text_entities(entities):
    today_date = datetime.datetime.today().strftime('%b-%d-%Y')  # Get today's date
    for entity in entities:
        if entity.dxftype() == 'TEXT':
            text = entity.dxf.text
            # Increment revision number if 'Rev' is found
            if entity.dxf.text.isdigit():
                current_number = int(entity.dxf.text)
                if current_number < 10:
                    entity.dxf.text = re.sub(r'\b(\d+)\b', lambda x: str(int(x.group(1)) + 1), entity.dxf.text)
            match_rev = re.search(r'Rev\s*(\d+)', text)
            if match_rev:
                current_rev = int(match_rev.group(1))
                new_rev = current_rev + 1
                revised_text = re.sub(r'(?P<rev>Rev\s*)\d+', r'\g<rev>' + str(new_rev)+' - '+"AFC", text)
                entity.dxf.text = revised_text
            # Convert dates to today's date in the same format
            if re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', text):
                entity.dxf.text = re.sub(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', today_date, text)
            # Update stamp text only if "FOR CUSTOMER" is present
            if "FOR CUSTOMER" in text:
                entity.dxf.text = text.replace("FOR CUSTOMER", "APPROVED FOR")
            if "APPROVAL" in text:
                entity.dxf.text = text.replace("APPROVAL", "CONSTRUCTION")
            elif "APPROVED FOR" in text and "CONSTRUCTION" in text:
                entity.dxf.text = "AS BUILT"
        elif entity.dxftype() == 'MTEXT':
            text = entity.plain_text()
            # Increment revision number if 'Rev' is found
            match_rev = re.search(r'Rev\s*(\d+)', text)
            if match_rev:
                current_rev = int(match_rev.group(1))
                new_rev = current_rev + 1
                revised_text = re.sub(r'(?P<rev>Rev\s*)\d+', r'\g<rev>' + str(new_rev)+' - '+"AFC", text)
                entity.text = revised_text
            # Convert dates to today's date in the same format
            if re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', text):
                entity.text = re.sub(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', today_date, text)
            # Update stamp text only if "FOR CUSTOMER" is present
            if "FOR CUSTOMER" in text:
                text = text.replace("FOR CUSTOMER", "APPROVED FOR")
            if "APPROVAL" in text:
                text = text.replace("APPROVAL", "CONSTRUCTION")
            elif "APPROVED FOR" in text and "CONSTRUCTION" in text:
                text = "AS BUILT"
            entity.text = text

        print("Found text entity:", entity.dxf.text if entity.dxftype() == 'TEXT' else entity.text)  # Print the text content


# Function to read and modify DXF files
def modify_dxf_files(dxf_files, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file in dxf_files:
        doc = ezdxf.readfile(file)
        # Print text entities outside of blocks
        print_text_entities_outside_blocks(doc)

        # Print and modify text entities in model space
        model_space_layout = doc.modelspace()
        model_space_text_entities = [entity for entity in model_space_layout if entity.dxftype() in ['TEXT', 'MTEXT']]
        print_text_entities(model_space_text_entities)
        modify_text_entities(model_space_text_entities)

        # Print and modify text entities in paper space layouts
        for layout in doc.layouts:
            if layout.name.lower() != 'model':
                paper_space_text_entities = [entity for entity in layout if entity.dxftype() in ['TEXT', 'MTEXT']]
                print_text_entities(paper_space_text_entities)
                modify_text_entities(paper_space_text_entities)
                # Add comment to a specific part of the drawing in paperspace
                # Specify comment text and location
                comment_text = ("2          APPROVED FOR CONSTRUCTION                     "
                                "          Apr-02-2024")
                bottom_left_coordinate = (0, 0)
                offset_x = 6.66  # Offset from the left edge
                offset_y = 1.78  # Offset from the bottom edg
                coordinate = (bottom_left_coordinate[0] + offset_x, bottom_left_coordinate[1] + offset_y)
                # Create a new MTEXT entity
                mtext_entity = layout.add_mtext(comment_text, dxfattribs={'style': 'Arial'})

                # Set the insertion point of the MTEXT entity
                mtext_entity.dxf.insert = coordinate

                # Set the text height through the style of the MTEXT entity
                mtext_entity.dxf.char_height = 0.08

                # Set the color of the MTEXT entity to black
                mtext_entity.dxf.color = 0

                # Set the paperspace background to ANSI B (ANSIB)
            layout.dxf.paper_size = (11, 17)  # ANSI B size is 11x17 inches




        # Save the modified DXF file in the output folder
        filename = os.path.basename(file)
        output_file = os.path.join(output_folder, filename)
        doc.saveas(output_file)


folder_path = r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\23034 - Project Gold Bar\02 Shop Drawing Package\_Working\23034 Shop Drawing Package Rev3 AFC\DWG"
dxf_files = find_dxf_files(folder_path)
output_folder = r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\23034 - Project Gold Bar\02 Shop Drawing Package\_Working\23034 Shop Drawing Package Rev3 AFC\DWG2"
convert_dwg_to_dxf(folder_path, output_folder)
modify_dxf_files(dxf_files, output_folder)

