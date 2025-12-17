SUBJECT_TOPICS = {
    "Programming Fundamentals": [
        "Variables & Data Types",
        "Conditional Statements",
        "Loops",
        "Functions",
        "Arrays",
        "Pointers",
        "Recursion"
    ],

    "Data Structures": [
        "Arrays",
        "Linked Lists",
        "Stacks",
        "Queues",
        "Trees",
        "Graphs",
        "Hashing",
        "Heaps"
    ],

    "Algorithms": [
        "Time & Space Complexity",
        "Sorting Algorithms",
        "Searching Algorithms",
        "Greedy Algorithms",
        "Divide and Conquer",
        "Dynamic Programming",
        "Backtracking"
    ],

    "Database Management Systems (DBMS)": [
        "ER Model",
        "Relational Model",
        "SQL Queries",
        "Normalization",
        "Transactions",
        "Indexing",
        "Concurrency Control"
    ],

    "Operating Systems": [
        "Process Management",
        "CPU Scheduling",
        "Deadlocks",
        "Memory Management",
        "Virtual Memory",
        "File Systems"
    ],

    "Computer Networks": [
        "OSI Model",
        "TCP/IP",
        "Routing Algorithms",
        "Congestion Control",
        "Network Security",
        "DNS & HTTP"
    ],

    "Software Engineering": [
        "SDLC Models",
        "Requirement Analysis",
        "Design Patterns",
        "Testing Techniques",
        "Agile & Scrum",
        "Maintenance"
    ],

    "Discrete Mathematics": [
        "Set Theory",
        "Relations & Functions",
        "POSETS and Matrices"
        "Graph Theory",
        "Combinatorics",
        "Logic",
        "Recurrence Relations"
    ],

    "Calculus for Engineers": [
    "Limits and Continuity",
    "Differentiation Techniques",
    "Applications of Derivatives",
    "Indefinite Integrals",
    "Definite Integrals",
    "Applications of Integrals",
    "Sequences and Series",
    "Taylor and Maclaurin Series",
    "Multivariable Functions"
    ],
    "Semiconductor Physics and Devices": [
    "Crystal Structure & Bonding",
    "Intrinsic and Extrinsic Semiconductors",
    "Carrier Concentration",
    "P-N Junction Diode",
    "Diode Characteristics",
    "Bipolar Junction Transistor (BJT)",
    "Field Effect Transistor (FET)",
    "MOSFET Basics",
    "Quantum Physics",
    "Optoelectronic Devices"
    ],
    "Chemistry for Engineers": [
    "Atomic Structure",
    "Chemical Bonding",
    "States of Matter",
    "Solutions and Colligative Properties",
    "Chemical Thermodynamics",
    "Chemical Kinetics",
    "Equilibrium",
    "Surface Chemistry",
    "Corrosion and Inhibition",
    "Electrochemistry"
    ],
    "Linear Algebra": [
        "Vectors",
        "Matrices",
        "Eigen Values",
        "Eigen Vectors",
        "Vector Spaces"
    ],

    "Probability & Statistics": [
        "Probability Basics",
        "Random Variables",
        "Distributions",
        "Bayes Theorem",
        "Mean, Variance",
        "Hypothesis Testing"
    ],

    "Machine Learning": [
        "Supervised Learning",
        "Unsupervised Learning",
        "Regression",
        "Classification",
        "Clustering",
        "Model Evaluation",
        "Overfitting & Underfitting"
    ],

    "Deep Learning": [
        "Neural Networks",
        "Backpropagation",
        "CNN",
        "RNN",
        "LSTM",
        "Activation Functions"
    ],

    "Artificial Intelligence": [
        "Search Algorithms",
        "Knowledge Representation",
        "Planning",
        "Expert Systems",
        "Reasoning",
        "Heuristics"
    ],

    "Data Science": [
        "Data Cleaning",
        "Data Visualization",
        "Feature Engineering",
        "Exploratory Data Analysis",
        "Model Building"
    ],
     "English": [
        "Grammar",
        "Vocabulary",
        "Reading Comprehension",
        "Writing Skills",
        "Literature",
        "Essay Writing"
    ]
}
def add_custom_subject(name, topics):
    if name and name not in SUBJECT_TOPICS:
        SUBJECT_TOPICS[name] = topics