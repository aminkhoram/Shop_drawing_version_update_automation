#code generated by Ian (Amin Khorram)

import os
import ezdxf
import re
import datetime
import shutil
import subprocess
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

def get_user_input():
    x1 = float(input("Enter x1 for the first comment: "))
    y1 = float(input("Enter y1 for the first comment: "))
    x2 = float(input("Enter x2 for the second comment (default is x1): ")) or x1
    x3 = float(input("Enter x3 for the third comment (default is x1): ")) or x1
    y2 = y3 = y1
    rev_no = int(input("Enter revision number: "))
    rev_date = datetime.datetime.today().strftime('%b-%d-%Y')
    version_control = int(input("Choose version change: 1 (fca_to_afc), 2 (afc_to_asbuilt), 3 (fca_to_asbuilt): "))
    
    rev_map = {1: "APPROVED FOR CONSTRUCTION", 2: "AS BUILT", 3: "AS BUILT"}
    rev = rev_map.get(version_control, "UNKNOWN")
    
    return x1, y1, x2, y2, x3, y3, rev_no, rev, rev_date, version_control

def convert_dwg_to_dxf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.dxf'):
            shutil.copy(os.path.join(input_folder, filename), os.path.join(output_folder, filename))
        
        elif filename.endswith('.dwg'):
            # Load DWG file
            TEIGHA_PATH = "C:\Program Files\ODA\ODAFileConverter 25.2.0\ODAFileConverter.exe"
            INPUT_FOLDER = input_folder  # Use the provided input_folder
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

def find_dxf_files(output_folder):
    return [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.dxf') and "DM-01" not in f]

def modify_text_entities(entities, version_control):
    today_date = datetime.datetime.today().strftime('%b-%d-%Y')
    for file in dxf_files:
        file_name = os.path.basename(file)
        doc = ezdxf.readfile(file)
        model_space_layout = doc.modelspace()
        paper_space_layout = doc.paperspace()
    for entity in entities:
        if entity.dxftype() in ('TEXT', 'MTEXT') and hasattr(entity, 'dxf'):
            text = entity.dxf.text
            match_rev = re.search(r'Rev(\d+)', text)

            if match_rev:
                current_rev = int(match_rev.group(1))
                new_rev = current_rev + 1
                rev_text = f"Rev {new_rev} - {'AS BUILT' if version_control > 1 else 'AFC'}"
                entity.dxf.text = re.sub(r'Rev\s*\d+', rev_text, text)

            if text.isdigit():
                    current_number = int(text)
                    
                    # Only increment if the current number is less than 10
                    if 1 < current_number < 10:
                        # Check for number in paper space
                        if any(entity.dxf.text.strip() == text for entity in paper_space_layout if entity.dxftype() == 'TEXT') and "list" not in file_name.lower():
                            # Increment the number in paper space
                            entity.dxf.text = re.sub(r'\b(\d+)\b', lambda x: str(int(x.group(1)) + 1), text)
                    else:
                        pass 
                    
            
            

            if entity in model_space_layout:
                # Update dates in model space only
                if re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', text):
                    entity.dxf.text = re.sub(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}-\d{4}', today_date, text)

            if "FOR CUSTOMER" in text and "APPROVAL" in text and version_control==3:
                entity.dxf.text = text.replace("FOR CUSTOMER", "AS BUILT").replace("APPROVAL", "").strip()
            elif "FOR CUSTOMER" in text and "APPROVAL" in text and version_control==1:
                entity.dxf.text = text.replace("FOR CUSTOMER", "APPROVED FOR").replace("APPROVAL", "CONTRUCTION").strip()
            elif "APPROVED FOR" in text and "CONSTRUCTION" in text and version_control==2:
                entity.dxf.text = text.replace("APPROVED FOR", "AS BUILT").replace("CONSTRUCTION", "").strip()

def list_incrementer(output_folder):
    # Iterate over all files in the output folder
    for filename in os.listdir(output_folder):
        # Check if the filename contains "list" (case-insensitive) and is a DXF file
        if 'list' in filename.lower() and filename.endswith('.dxf'):
            # Open the DXF file
            filepath = os.path.join(output_folder, filename)
            doc = ezdxf.readfile(filepath)
            
            # Iterate over all entities in the document (model and paper spaces)
            for entity in doc.entities:
                if entity.dxftype() in ('TEXT', 'MTEXT') and hasattr(entity, 'dxf'):
                    text = entity.dxf.text
                    if text.isdigit():
                        current_number = int(text)
                        if current_number<10:
                            # Increment standalone numbers in the text
                            updated_text = re.sub(r'\b(\d+)\b', lambda x: str(int(x.group(1)) + 1), text)
                            entity.dxf.text = updated_text
            
            # Save the updated DXF file
            doc.saveas(filepath)




def print_drawings(dxf_files, pdf_output):
    if not os.path.exists(pdf_output):
        os.makedirs(pdf_output)

    for file in dxf_files:
        doc = ezdxf.readfile(file)

        # Calculate the extents of the drawing
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        # Iterate over model space
        for entity in doc.modelspace():
            if entity.dxftype() == 'LINE':
                min_x = min(min_x, entity.dxf.start.x, entity.dxf.end.x)
                min_y = min(min_y, entity.dxf.start.y, entity.dxf.end.y)
                max_x = max(max_x, entity.dxf.start.x, entity.dxf.end.x)
                max_y = max(max_y, entity.dxf.start.y, entity.dxf.end.y)
            elif entity.dxftype() == 'LWPOLYLINE':
                for vertex in entity.vertices():
                    min_x = min(min_x, vertex[0])
                    min_y = min(min_y, vertex[1])
                    max_x = max(max_x, vertex[0])
                    max_y = max(max_y, vertex[1])

        # Iterate over paper space layouts
        for layout in doc.layouts:
            for entity in layout:
                if entity.dxftype() == 'LINE':
                    min_x = min(min_x, entity.dxf.start.x, entity.dxf.end.x)
                    min_y = min(min_y, entity.dxf.start.y, entity.dxf.end.y)
                    max_x = max(max_x, entity.dxf.start.x, entity.dxf.end.x)
                    max_y = max(max_y, entity.dxf.start.y, entity.dxf.end.y)
                elif entity.dxftype() == 'LWPOLYLINE':
                    for vertex in entity.vertices():
                        min_x = min(min_x, vertex[0])
                        min_y = min(min_y, vertex[1])
                        max_x = max(max_x, vertex[0])
                        max_y = max(max_y, vertex[1])

        # Calculate the width and height of the drawing
        width = max_x - min_x
        height = max_y - min_y

        # Add a slight margin of 0.25 inches
        margin = 0.25
        min_x -= margin
        min_y -= margin
        max_x += margin
        max_y += margin

        # Ensure the calculated dimensions are positive and finite
        if width <= 0 or height <= 0:
            continue

        # ANSI-B paper size in inches (11x17 inches)
        ansi_b_width_inches = 17
        ansi_b_height_inches = 11

        # Calculate the scale factor to fit the drawing onto the ANSI-B page
        scale_factor = min(ansi_b_width_inches / width, ansi_b_height_inches / height)

        # Calculate the new width and height of the drawing
        new_width = width * scale_factor
        new_height = height * scale_factor

        # Create a PDF file
        out_file = os.path.join(pdf_output, os.path.splitext(os.path.basename(file))[0] + '.pdf')

        # Create a matplotlib figure with ANSI-B paper size
        fig, ax = plt.subplots(figsize=(ansi_b_width_inches, ansi_b_height_inches))
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Set tight layout
        ax.set_xlim(min_x, min_x + new_width)
        ax.set_ylim(min_y, min_y + new_height)
        backend = MatplotlibBackend(ax)

        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        frontend = Frontend(ctx, out)

        # Draw model space
        frontend.draw_layout(doc.modelspace(), finalize=True)

        # Draw paper space layouts
        for layout in doc.layouts:
            if layout.name.lower() != 'model':
                frontend.draw_layout(layout, finalize=True)

        # Save the plot as PDF
        fig.savefig(out_file, format='pdf', dpi=300)
        plt.close(fig)

def modify_dxf_files(dxf_files, x1, y1, x2, y2, x3, y3, rev_no, rev, rev_date, version_control, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file in dxf_files:
        doc = ezdxf.readfile(file)
        # Print text entities outside of blocks
        # print_text_entities_outside_blocks(doc)

        # Print and modify text entities in model space
        model_space_layout = doc.modelspace()
        model_space_text_entities = [entity for entity in model_space_layout if entity.dxftype() in ['TEXT', 'MTEXT']]
        # print_text_entities(model_space_text_entities)
        modify_text_entities(model_space_text_entities, version_control)
        # Print and modify text entities in paper space layouts
        # Print and modify text entities in paper space layouts
        for layout in doc.layouts:
            if layout.name.lower() != 'model':
                paper_space_text_entities = [entity for entity in layout if entity.dxftype() in ['TEXT', 'MTEXT']]
                # print_text_entities(paper_space_text_entities)
                modify_text_entities(paper_space_text_entities, version_control)

                # Add each piece of text to the layout using the provided coordinates
                l1 = layout.add_mtext(rev_no, dxfattribs={'style': 'Arial'})
                l1.dxf.insert = (x1, y1)
                l1.dxf.char_height = 0.08
                l1.dxf.color = 0
                
                l2 = layout.add_mtext(rev, dxfattribs={'style': 'Arial'})
                l2.dxf.insert = (x2, y2)
                l2.dxf.char_height = 0.08
                l2.dxf.color = 0
                
                l3 = layout.add_mtext(rev_date, dxfattribs={'style': 'Arial'})
                l3.dxf.insert = (x3, y3)
                l3.dxf.char_height = 0.08
                l3.dxf.color = 0

                # Set the paperspace background to ANSI B (ANSIB)
            layout.dxf.paper_size = (11, 17)  # ANSI B size is 11x17 inches

        # Save the modified DXF file in the output folder
        filename = os.path.basename(file)
        output_file = os.path.join(output_folder, filename)
        doc.saveas(output_file)





# Save the modified DXF file in the output folder
input_folder = r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\24257 - MSFT YQB06 colo 2\02 Shop Drawing Package\_Working\24257 Shop Drawing Package_Rev2-test\dwg"
output_folder = r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\24257 - MSFT YQB06 colo 2\02 Shop Drawing Package\_Working\24257 Shop Drawing Package_Rev2-test\dwg2"
pdf_output = r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\24257 - MSFT YQB06 colo 2\02 Shop Drawing Package\_Working\24257 Shop Drawing Package_Rev2-test\pdf2"
x1, y1, x2, y2, x3, y3, rev_no, rev, rev_date, version_control = get_user_input()
# Convert DWG to DXF
convert_dwg_to_dxf(input_folder, output_folder)

# Find DXF files in the output folder
dxf_files = find_dxf_files(output_folder)

# Modify DXF files
modify_dxf_files(dxf_files, x1, y1, x2, y2, x3, y3, rev_no, rev, rev_date, version_control, output_folder)
print_drawings(dxf_files, pdf_output)
list_incrementer(output_folder)
