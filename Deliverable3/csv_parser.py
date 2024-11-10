import os

# Paths for CSV files and image directory
file_path_grade_9 = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
file_path_men = '37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv'
image_dir = 'images'

# Placeholder data for team scores and individual results for different files
team_scores_grade_9 = []
individual_results_grade_9 = []
team_scores_men = []
individual_results_men = []

# Function to read CSV data and store in lists
def read_csv(file_path, team_scores, individual_results):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    in_team_scores = False
    in_individual_results = False

    for line in lines:
        line = line.strip()
        if line.startswith("Place,Team,Score"):
            in_team_scores = True
            in_individual_results = False
            continue
        elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
            in_team_scores = False
            in_individual_results = True
            continue
        elif not line:
            continue

        data = line.split(',')
        
        if in_team_scores and len(team_scores) < 3:
            if len(data) >= 3 and all(data[:3]):
                team_scores.append(data[:3])
        elif in_individual_results:
            if len(data) >= 8 and all(data[:8]):
                individual_results.append(data[:8])

# Read data from both files
read_csv(file_path_grade_9, team_scores_grade_9, individual_results_grade_9)
read_csv(file_path_men, team_scores_men, individual_results_men)

# Filter Grade 9 and Grade 10 Results
grade_9_results = [result for result in individual_results_grade_9 if result[1].strip() == "9"]
grade_10_results = [result for result in individual_results_grade_9 if result[1].strip() == "10"]

# Select the top 10 athletes across all genders based on time
top_10_results = sorted(individual_results_grade_9 + individual_results_men, key=lambda x: float(x[4].replace(':', '')))[:10]

# This is my function that generates HTML content for the pages
def generate_html_content(title, file_name, team_data, individual_data, max_individual_results=None):
    nav_bar = """
    <nav>
        <a href="results.html">Women's Results</a> |
        <a href="mens_results.html">Men's Results</a> |
        <a href="top_athletes.html">Top 10 Athletes Across All Genders</a> |
        <a href="grade_9_results.html">Grade 9 Results</a> |
        <a href="grade_10_results.html">Grade 10 Results</a> |
        <a href="index.html">Welcome Page</a>
    </nav>
    """

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel="stylesheet" href="css/style.css">
   <title>{title}</title>
</head>
<body>
   <header id="main-header">
       <h1>{title}</h1>
   </header>

   {nav_bar}

   <main id="content">
       <section id="event-title">
           <h2>{title}</h2>
       </section>
    """

    # Added team scores table only for pages that have team data such as mens and womens
    if team_data:
        html_content += """
       <section id="team-scores">
           <h2>Team Scores</h2>
           <table>
               <thead>
                   <tr>
                       <th>Place</th>
                       <th>Team</th>
                       <th>Score</th>
                   </tr>
               </thead>
               <tbody>
        """
        for index, score in enumerate(team_data):
            css_class = ['first-place', 'second-place', 'third-place'][index] if index < 3 else ''
            if len(score) >= 3:
                html_content += f"""
                        <tr class="{css_class}">
                            <td>{score[0]}</td>
                            <td>{score[1]}</td>
                            <td>{score[2]}</td>
                        </tr>
                """

        html_content += """
               </tbody>
           </table>
       </section>
       """

    # Add individual results
    html_content += """
       <section id="individual-results">
           <h2>Top Results</h2>
    """

    # Limited the number of individual results displayed if max_individual_results is set. This was to not overload the user with data.
    for index, result in enumerate(individual_data[:max_individual_results] if max_individual_results else individual_data):
        if len(result) >= 7:
            athlete_name = result[2]
            athlete_link = result[3]
            athlete_id = result[7]
            image_path = os.path.join("images", f"{athlete_id}.jpg") if os.path.exists(f"images/{athlete_id}.jpg") else "images/default.jpg"
        
            html_content += f"""
            <div class="athlete">
                <h3>{athlete_name}</h3>
                <p>Place: {result[0]}</p>
                <p>Grade: {result[1]}</p>
                <p>Time: {result[4]}</p>
                <p>Team: {result[5]}</p>
                <a href="{athlete_link}" target="_blank">Athlete Profile</a>
                <img src="{image_path}" alt="Profile Picture of {athlete_name}" width="150">
            </div>
            <hr>
            """

    html_content += """
       </section>
   </main>
   <footer id="main-footer">
       <p>&copy; 2024 Client Project - All rights reserved.</p>
   </footer>
   
   <script src="js/script.js"></script>
</body>
</html>
    """
    with open(file_name, 'w') as file:
        file.write(html_content)
    print(f"{file_name} has been created successfully.")

# Generate HTML pages
generate_html_content("Women's Results", "results.html", team_scores_grade_9[:3], individual_results_grade_9, max_individual_results=20)
generate_html_content("Men's Results", "mens_results.html", team_scores_men[:3], individual_results_men) # No limit for men's page
generate_html_content("Top 10 Athletes Across All Genders", "top_athletes.html", [], top_10_results)
generate_html_content("Grade 9 Results", "grade_9_results.html", [], grade_9_results)
generate_html_content("Grade 10 Results", "grade_10_results.html", [], grade_10_results)
