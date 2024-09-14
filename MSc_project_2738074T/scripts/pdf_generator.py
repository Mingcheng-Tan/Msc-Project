import os
import sys
import statistics
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def generate_data(file_path_default):

    test_info_path = os.path.join(file_path_default, "test_info.txt")
    stim_info_path = os.path.join(file_path_default, "stimulus_results.txt")
    eye_info_path = os.path.join(file_path_default, "EyeTrackingData.txt")
    false_positive_path = os.path.join(file_path_default, "false_positives.txt")

    test_info = []
    with open(test_info_path, 'r') as file:
        for line in file:
            test_info = line.split(',')


    false_positives = []
    with open(false_positive_path, 'r') as file:
        for line in file:
            false_positives.append(line.strip())

    with open(stim_info_path, 'r') as file:
        test_runtime = float(file.readline().strip())


    with open(eye_info_path, 'r') as file:
        fixation_point = file.readline().strip()

    eye_data = []
    with open(eye_info_path, 'r') as file:
        for i,line in enumerate(file):
            if i==0:
                continue
            eye_data.append(line.strip().split(','))
    
    stimulus_response_data = []
    with open(stim_info_path, 'r') as file:
        for i,line in enumerate(file):
            if i==0:
                continue
            fields = line.strip().split(',')
            fields[1], fields[3] = fields[1].strip('('), fields[3].strip(' )')
            del fields[2]
            stimulus_response_data.append(fields)

    centre_true_count = sum([1 for item in eye_data if item[3] == 'True'])
    percentage_centre_true = (centre_true_count / len(eye_data)) * 100 if len(eye_data) > 0 else 0


    false_positive_rate = len(false_positives) / len(stimulus_response_data) * 100

    point_tracker = {}
    for data in stimulus_response_data:
        _, x, y, seen, time_since_start, reaction_time, was_looking_at_center = data
        key = (x, y)

        if key not in point_tracker:
            point_tracker[key] = {'seen': 0, 'unseen': 0, 'valid': was_looking_at_center == 'True'}

        if seen == 'True':
            point_tracker[key]['seen'] += 1
        else:
            point_tracker[key]['unseen'] += 1


    total_points = len(stimulus_response_data)
    points_hit = sum(1 for data in stimulus_response_data if data[3] == 'True')

    valid_points_hit = sum(1 for point, stats in point_tracker.items() if stats['valid'] and stats['seen'] > 0)       

    false_negatives = sum(1 for point, stats in point_tracker.items() if stats['valid'] and stats['seen'] > 0 and stats['unseen'] > 0)
    total_valid_points = sum(1 for stats in point_tracker.values() if stats['valid'])
    false_negative_rate = (false_negatives / total_valid_points) * 100 if total_valid_points > 0 else 0

    
    reaction_times = [float(data[5]) for data in stimulus_response_data if data[3] == 'True']
    avg_reaction_time = 0
    if reaction_times:
        avg_reaction_time = statistics.mean(reaction_times) * 1000

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    results = {
        'Current Date': current_date,
        'Current Time': current_time,
        'Test Duration': f"{test_runtime:.2f}",
        'Fixation Point': fixation_point,
        'False Positive Error Rate': f"{false_positive_rate:.2f}%",
        'False Negative Error Rate': f"{false_negative_rate:.2f}%",
        'Points Hit / Total Points': f"{points_hit}/{total_points}",
        'Valid Points Hit / Total Points': f"{valid_points_hit}/{total_points}",
        'Average Reaction Time': f"{avg_reaction_time:.2f} ms" if avg_reaction_time else "N/A",
        'Centre True Perc' : f"{percentage_centre_true:.2f}%",
    }
    return results,test_info
    

def create_pdf(file_path_default, data, test_info):
    output_dir_path = os.path.abspath(os.path.join(os.path.dirname(file_path_default), 'reports'))
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    output_file_path = os.path.join(output_dir_path, "test_results.pdf")
    print("Report will be generated in: "+output_file_path)
    
    c = canvas.Canvas(output_file_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 40, "Visual Test")
    

    c.setFont("Helvetica", 12)
    c.drawString(40, height - 60, f"Test Duration: {data['Test Duration']}s")


    c.setFont("Helvetica", 12)
    c.drawRightString(width - 40, height - 40, f"{data['Current Date']} {data['Current Time']}")


    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 100, "Stim Info")
    c.setFont("Helvetica", 12)
    stim_info = ["Type: " + test_info[0], "Canvas: " + test_info[1], "Display Time: " + f"{float(test_info[2])*100}ms"]
    for i, info in enumerate(stim_info):
        c.drawString(40, height - 120 - (20 * i), info)


    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, height - 100, "Fixation Info")
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 120, "Fixation Monitor: Gaze")
    c.drawString(300, height - 140, f"Fixation Target: {data['Fixation Point']}")



    metrics_start_height = height - 225
    c.setFont("Helvetica-Bold", 14)
    c.drawString(375, metrics_start_height, "Metrics")
    metrics = [
        f"False Positive Error Rate: {data['False Positive Error Rate']}",
        f"False Negative Error Rate: {data['False Negative Error Rate']}",
        f"Average Reaction Time: {data['Average Reaction Time']}",
        f"Stimulus Entry / Total Stimulus: {data['Points Hit / Total Points']}",
        f"Valid Stimulus Entry / Total Stimulus: {data['Valid Points Hit / Total Points']}",
        f"Time looked at Centre: {data['Centre True Perc']}",
    ]
    c.setFont("Helvetica", 12)
    for i, metric in enumerate(metrics):
        c.drawString(375, metrics_start_height - 20 - (20 * i), metric)

    graph_dir_path = os.path.abspath(os.path.join(os.path.dirname(file_path_default), 'processed'))
    grayscale_path = os.path.join(graph_dir_path, "grayscale.png")
    if os.path.exists(grayscale_path):
        grayscale_img = ImageReader(grayscale_path)
        c.drawImage(grayscale_img, 0, height - 480, width=375, height=300, mask=None)

    heatmap_path = os.path.join(graph_dir_path, "heatmap.png")
    if os.path.exists(heatmap_path):
        heatmap_img = ImageReader(heatmap_path)
        c.drawImage(heatmap_img, 0, height - 750, width=330, height=264, mask=None)
        
    invalid_path = os.path.join(graph_dir_path, "invalid.png")
    if os.path.exists(invalid_path):
        invalid_img = ImageReader(invalid_path)
        c.drawImage(invalid_img, 285, height - 750, width=330, height=264, mask=None)

    c.showPage()
    c.save()



file_path_default = sys.argv[1]
data,test_info = generate_data(file_path_default)
create_pdf(file_path_default,data,test_info)
