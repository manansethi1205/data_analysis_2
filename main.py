import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

file_path = 'student_scores.xlsx'

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    exit()
except Exception as e:
    print(f"Error: Unable to load the Excel file. {e}")
    exit()
required_columns = {'Student ID', 'Name', 'Subject Score'}
if not required_columns.issubset(df.columns):
    print(f"Error: Ensure the Excel file contains {required_columns}.")
    exit()

if df.empty:
    print("Error: The Excel file is empty. Please provide a valid dataset.")
    exit()
# grouping data for each student and calculating total and avg scores
students = df.groupby('Student ID').agg(
    Name=('Name', 'first'),
    Total_Score=('Subject Score', 'sum'),
    Average_Score=('Subject Score', 'mean')
).reset_index()
# individual report cards for each student
for index, row in students.iterrows():
    student_id = row['Student ID']
    name = row['Name']
    total_score = row['Total_Score']
    average_score = row['Average_Score']
    
    # Handle missing or invalid data
    if pd.isna(name) or pd.isna(total_score) or pd.isna(average_score):
        print(f"Warning: Skipping report generation for Student ID {student_id} due to missing data.")
        continue
    
    # Filter subject-wise scores for this student
    student_scores = df[df['Student ID'] == student_id][['Name', 'Subject Score']]
    if student_scores.empty:
        print(f"Warning: No subject scores found for Student ID {student_id}. Skipping report generation.")
        continue
    
    student_scores.rename(columns={'Subject Score': 'Score'}, inplace=True)
    
    # Create PDF
    filename = f"report_card_{student_id}.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Add title
    elements.append(Paragraph(f"Report Card: {name}", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Add student details
    elements.append(Paragraph(f"Student ID: {student_id}", styles['Normal']))
    elements.append(Paragraph(f"Student Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Total Score: {total_score}", styles['Normal']))
    elements.append(Paragraph(f"Average Score: {average_score:.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Add subject-wise scores table
    table_data = [['Subject', 'Score']] + student_scores.values.tolist()
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    try:
        pdf.build(elements)
        print(f"Generated report card for {name}: {filename}")
    except Exception as e:
        print(f"Error: Failed to generate PDF for Student ID {student_id}. Details: {e}")
