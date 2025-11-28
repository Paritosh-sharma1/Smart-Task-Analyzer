Smart Task Prioritizer 🚀

A full-stack task management application that uses a weighted scoring algorithm to prioritize work based on urgency, importance, effort, and dependencies. Built with Django (DRF) and Vanilla JavaScript.

📋 Table of Contents

Setup Instructions

Algorithm Explanation

Design Decisions & Trade-offs

Bonus Challenges

Future Improvements

🛠 Setup Instructions

Follow these steps to get the project running on your local machine.

Prerequisites

Python 3.8+ installed

Git installed

1. Clone the Repository

git clone https://github.com/Paritosh-sharma1/Smart-Task-Analyzer.git
cd task_manager

2. Install Dependencies

pip install -r requirements.txt

3. Database Setup

You must create the database tables before running the app. Run these two commands in order:

python manage.py makemigrations
python manage.py migrate

4. Create Admin User

To view the stored tasks in the Admin Panel, create a superuser account:

python manage.py createsuperuser

(Follow the prompts to set a username and password)

4. Run the Application

Start the Django backend server:

python manage.py runserver

How to Use:

Frontend: Open the index.html file (located in the root folder) directly in your web browser.

Backend Admin: Go to http://127.0.0.1:8000/admin/ to log in and view the Task table.

🧠 Algorithm Explanation

The core of this application is the "Smart Balance" algorithm (tasks/utils.py). It is designed to solve the common problem of "Analysis Paralysis" by converting qualitative task attributes into a quantitative Priority Score.

The algorithm does not simply sort by date. It implements a weighted heuristic model that balances four competing factors. The logic mimics the decision-making process of a productive human, weighing the "Eisenhower Matrix" of Urgency vs. Importance, while also factoring in psychological momentum (Effort).

1. Urgency (The Deadline Factor)
   Deadlines are the strongest natural motivator. The algorithm calculates the delta between the due_date and the current system date (date.today()).

Overdue Tasks (+50 points): If a task is past its due date (days_left < 0), it receives a massive penalty score. This ensures that forgotten items immediately jump to the top of the queue, demanding attention.

Imminent Danger (+30 points): Tasks due within the next 48 hours receive a significant boost.

The "Week Ahead" (+15 points): Tasks due within 7 days get a moderate boost.

Future Tasks (0 points): Tasks due more than a week out receive no urgency score, preventing them from cluttering the top of the list unless they are extremely important.

2. Importance (User Weight)
   Users assign a subjective importance rating from 1 to 10. The algorithm treats this as a multiplier to compete with urgency.

Weighting: Score += Importance \* 3

Rationale: A maximum importance task (10) gains 30 points. This is equal to the "Imminent Danger" bonus. This design decision means a highly important task due next week can rightfully outrank a trivial task due tomorrow. This prevents the "Tyranny of the Urgent."

3. Effort (The "Quick Win" Psychology)
   Productivity methodologies (like GTD) suggest doing quick tasks immediately to build momentum.

Quick Wins (+20 points): If a task takes less than 2 hours (estimated_hours < 2), it gets a bonus. This pushes small, easy tasks up the list so the user can clear them quickly and feel productive.

High Effort Penalty (-10 points): Tasks taking >10 hours get a slight deduction. This acknowledges that starting a massive task requires significant energy and block time. It shouldn't block the "Quick Wins" unless it is also urgent.

4. Dependencies (Blockers)

Unblocked Bonus (+10 points): If a task has an empty dependency list [], it gets a small boost because it is actionable right now.

We prioritize actionable work over blocked work.

🏗 Design Decisions & Trade-offs

1. Data Persistence on Analysis

Decision: I implemented the database save logic inside the AnalyzeTasksView (POST request) rather than creating a separate CRUD "Create" endpoint.

Trade-off: This violates the REST principle of "Separation of Concerns" slightly (Analysis vs. Creation).

Why: Given the time constraint, this allowed me to fulfill the requirement of "Accept a list of tasks and return them sorted" while simultaneously ensuring the data is stored for the Admin panel requirement. It streamlines the user flow: Input -> Click Analyze -> Data Saved & Sorted.

2. Backend: Django Rest Framework (DRF)

Decision: Used DRF Serializers instead of manual Python dictionaries.

Why: Although it requires more setup code, DRF handles JSON validation automatically. It ensures that if the frontend sends a string for estimated_hours, the API rejects it cleanly rather than crashing the scoring algorithm.

3. Frontend:

Decision: Choose not to use React.

Trade-off: The DOM manipulation code is more verbose.

Django project structure, Model definition, and Admin registration.

Designing the weights in utils.py and writing Unit Tests (tasks/tests.py) to verify them.

Building the HTML interface, CSS for priority colors, and JavaScript Fetch API integration.

🏆 Bonus Challenges Attempted

Critical Thinking (Sorting Strategies): I implemented the dropdown selector to allow users to switch strategies.

Fastest Wins: Re-sorts the list by estimated_hours ascending.

High Impact: Re-sorts by importance descending.

Deadline Driven: Re-sorts by due_date ascending.

Smart Balance: The default custom algorithm.

🚀 Future Improvements

Circular Dependency Graph: Currently, the dependency check is simple (Is the list empty?). With more time, I would build a Directed Acyclic Graph (DAG) to detect if Task A blocks Task B, and ensure Task B receives a lower priority score until Task A is complete.

User Authentication: Implement Django Auth to allow multiple users to have private task lists.

Interactive Frontend: Migrate to React to allow Drag-and-Drop reordering and inline editing of tasks.
