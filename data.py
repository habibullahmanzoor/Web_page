# data.py
DATA = {
    "name": "Dr. Habib Ullah Manzoor",
    "title": "AI Research Scientist",
    "location": "Glasgow, United Kingdom",
    "email_primary": "habibullahmanzoor@gmail.com",
    "phone": "+44 7780 465653",
    "links": {
        "LinkedIn": "https://www.linkedin.com/in/habib-ullah-manzoor-phd-19198994/",
        "Google Scholar": "https://scholar.google.com/citations?user=tKDhmdAAAAAJ&hl=en",
        "ORCID": "https://orcid.org/0000-0003-0192-7353",
    },
   "summary": (
    "Ph.D.-level Research Scientist with over 10 years of experience in teaching and research, specializing in machine learning, "
    "electrical engineering, and cyber-secure systems. Skilled in image, audio, and video processing, environmental monitoring, "
    "medical imaging, federated learning, large language models (LLMs), retrieval-augmented generation (RAG), and dashboard design."),


    "skills": {
        "Machine Learning & AI": ["Supervised/Unsupervised", "Deep Learning (CNN, LSTM, Transformers)", "Federated Learning", "Anomaly Detection"],
        "Cloud & MLOps": ["AWS Bedrock", "SageMaker", "Lambda", "CI/CD", "Linux", "Git/GitHub"],
        "Security": ["SIEM", "IDS/IPS", "Secure-by-design workflows"],
        "Programming": [
    "Python",
    "NumPy",
    "Pandas",
    "scikit-learn",
    "PyTorch",
    "TensorFlow",
    "Keras",
    "LangChain",
    "HuggingFace",
    "Dash",
    "Flask",
    "R",
    "MATLAB",
    "C++"
],
        "Visualisation": ["Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau"],
        "Hardware/IoT": ["Digital Logic", "PCB Design", "AutoCAD Electrical", "Proteus", "IoT (Arduino/Raspberry Pi)"]
    },

"education": [
    {
        "years": "2021–2025",
        "degree": "Ph.D. in Applied Artificial Intelligence",
        "school": "James Watt School of Engineering, University of Glasgow, UK",
        "details": (
            "Thesis: Securing Intelligent Networks: Federated Learning for Privacy-Preserving Anomaly Detection."
            "<br>Fully funded PhD Scholarship."
        )
    },
    {
        "years": "2014–2016",
        "degree": "M.S. Electronic Engineering",
        "school": "Ghulam Ishaq Khan Institute, Pakistan",
        "details": (
            "Institute Fellowship (top 2% of cohort)."
            "<br>Fully funded MS Scholarship."
        )
    },
    {
        "years": "2009–2013",
        "degree": "B.Sc. Electrical Engineering",
        "school": "HITEC University, Pakistan",
        "details": "Merit-based partial scholarship."
    }
],



"experience": {
    "teaching": [
        {
            "org": "University of Glasgow, UK",
            "role": "Tutor & Lab Demonstrator",
            "dates": "Jan 2023 – Jul 2024",
            "bullets": [
                "Delivered lectures in Programming Fundamentals (Python), Electronic Systems, Digital Logic Design, and Power Systems.",
                "Supervised labs for Digital Electronics and Aerospace Engineering; created manuals and evaluations.",
                "Marked exams/scripts and supervised Master’s theses in AI-based anomaly detection and fibre-optical optimisation."
            ]
        },
        {
            "org": "UET Lahore, Pakistan",
            "role": "Lecturer",
            "dates": "Sep 2016 – Oct 2021",
            "bullets": [
                "Taught DLD, Circuit Analysis, Instrumentation, Control Systems, EM Theory, and Analog Electronics.",
                "Designed OBE-aligned curricula and managed laboratories in Digital Electronics and Electric Machines.",
                "Supervised 20+ final-year projects; chaired curriculum and quality enhancement committees."
            ]
        },
        {
            "org": "GIK Institute, Pakistan",
            "role": "Lab Instructor",
            "dates": "Jan 2014 – Dec 2015",
            "bullets": [
                "Assisted teaching in Electromagnetic Theory and Circuit Design labs; authored lab manuals and exams.",
                "Served as hostel warden overseeing accommodation and welfare operations."
            ]
        }
    ],
    "research": [
        {
            "org": "University of Glasgow, UK",
            "role": "Research Assistant",
            "dates": "Jul 2025 – Present",
            "bullets": [
                "Designing and implementing ML models for deepfake detection in video and audio.",
                "Developing a mobile app for real-time deepfake detection with optimised architectures for accuracy and latency.",
                "Training and validating models across diverse datasets; presenting findings at conferences."
            ]
        },
        {
            "org": "University of Glasgow, UK",
            "role": "Research Assistant",
            "dates": "Aug 2024 – Apr 2025",
            "bullets": [
                "Developed an IoT + AI framework for forest conservation using acoustic analytics for illegal activity detection.",
                "Built real-time tree-health monitoring dashboards for environmental stakeholders.",
                "Implemented scalable cloud pipelines (AWS Lambda + S3) for data ingestion and anomaly alerts."
            ]
        },
        {
            "org": "University of Glasgow, UK",
            "role": "Research Assistant",
            "dates": "Apr 2022 – Nov 2022",
            "bullets": [
                "Contributed to the SODOR Project: autonomous weather stations and ML-driven anomaly detection for ScotRail.",
                "Developed sensor-fusion algorithms and environmental monitoring pipelines.",
                "Produced research documentation and delivered findings to industrial partners."
            ]
        }
    ]
},



    "research_roles": [
        {"title": "Research Assistant", "org": "University of Glasgow", "dates": "Jul 2025 – Present",
         "desc": "Deepfake detection in video/audio; mobile app for real-time detection; model training across diverse datasets."},
        {"title": "Research Assistant", "org": "University of Glasgow", "dates": "Aug 2024 – Apr 2025",
         "desc": "IoT + AI for deforestation monitoring; sound detection for illegal activity; tree-health monitoring dashboard."},
        {"title": "Research Assistant", "org": "University of Glasgow", "dates": "Apr 2022 – Nov 2022",
         "desc": "SODOR project: autonomous weather stations + ML anomaly detection for ScotRail network."}
    ],

    "funding": [{
        "project": "Stealth Attack Detection in Federated Learning Environments",
        "body": "University of Ajman, Deanship Interdisciplinary Research Grant (IDG)",
        "amount": "£10,000",
        "role": "Co-Lead Investigator",
        "outcome": "90% attack detection accuracy in distributed ML settings"
    }],

    # ✅ NEW: Projects now live inside DATA
    "projects": [
        {
            "title": "Deep Fake Mitigation",
            "summary": "Scaled distributed ML pipelines using CNNs with pruning for efficient deepfake detection.",
            "impact": "",
            "tags": ["CNN", "Model Pruning", "Distributed ML"]
        },
        {
            "title": "IoT-Driven Environmental Monitoring",
            "summary": "Real-time illegal tree-cutting detection via audio classification; edge compute for low-latency forest surveillance.",
            "impact": "",
            "tags": ["Audio ML", "Edge", "IoT"]
        },
        {
            "title": "Smart Safety Solutions",
            "summary": "AI-powered automated fire detection for high-risk areas; reduced emergency response times using IoT sensor networks.",
            "impact": "",
            "tags": ["Computer Vision", "IoT", "Alerts"]
        },
        {
            "title": "Data Visualization Platform",
            "summary": "Cross-platform dashboard for multi-sensor IoT analytics; real-time resource monitoring for stakeholders.",
            "impact": "",
            "tags": ["Dashboards", "Analytics", "IoT"]
        },
        {
            "title": "Medical Imaging at Scale",
            "summary": "Communication-efficient distributed ML for brain-tumor detection with quantization-aware training.",
            "impact": "≈95% accuracy (private healthcare datasets).",
            "tags": ["Medical Imaging", "QAT", "Distributed ML"]
        },
        {
            "title": "Cybersecurity Research",
            "summary": "Pioneered stealth communication attacks to expose network resource vulnerabilities.",
            "impact": "",
            "tags": ["Security", "Adversarial", "Networks"]
        },
        {
            "title": "Game Theory for IoT Security",
            "summary": "Incentive-based framework to detect adversarial IoT clients.",
            "impact": "Reduced false positives by ~30%.",
            "tags": ["Game Theory", "Security", "IoT"]
        },
        {
            "title": "Grid Optimization Framework",
            "summary": "LSTM-based load forecasting for smart grids.",
            "impact": "Improved residential energy cost savings by ~18%.",
            "tags": ["LSTM", "Energy", "Forecasting"]
        },
        {
            "title": "Explainable AI Systems",
            "summary": "Adversarial image attack model with interpretable gradients to improve transparency in diagnostics.",
            "impact": "",
            "tags": ["XAI", "Adversarial", "Healthcare"]
        },
        {
            "title": "Infrastructure Predictive Analytics",
            "summary": "Autoencoder-based predictive maintenance for power-line components to increase grid reliability.",
            "impact": "",
            "tags": ["Autoencoders", "Predictive Maintenance", "Power"]
        }
    ],

    "awards": [
        "Best Paper Presentation Award, IEEE GPECOM 2022",
        "PhD Fellowship, University of Glasgow (2021–2025)",
        "MS Fellowship, GIKI (2014–2016, top 2% cohort)"
    ],

    "training": [
        "LLM Fine-Tuning & Customization (PEFT/LoRA, RLHF), Coursera, Jul 2025",
        "AWS Generative AI Applications (Bedrock, Titan, Claude-3), Coursera, Feb 2025",
        "Google Cybersecurity Professional Certificate, Apr 2024",
        "Emergency First Aid at Work, Jul 2024",
        "QEC/OBE Training, Sep 2017"
    ],

    "metrics": {"h_index": 0, "i10_index": 0, "citations": 0, "journals": 43, "conferences": 16, "book_chapters": 1},

    "publications": [
        {"title": "Novel Stealth Communication Round Attack and Robust Incentivized Federated Averaging for Load Forecasting",
         "venue": "IEEE Transactions on Sustainable Computing", "year": 2025},
        {"title": "Semantic-Aware Federated Blockage Prediction (SFBP) in Vision-Aided Next-Gen Wireless Network",
         "venue": "IEEE Transactions on Network and Service Management", "year": 2025},
        {"title": "Enhancing Consumer Privacy in Federated Load Forecasting through Single Layer Aggregation",
         "venue": "IEEE Consumer Electronics Magazine", "year": 2024},
        {"title": "Smart grid security through fusion-enhanced federated learning against adversarial attacks",
         "venue": "Engineering Applications of Artificial Intelligence", "year": 2025},
        {"title": "Adaptive Single-Layer Aggregation Framework for Energy-Efficient and Privacy-Preserving Load Forecasting",
         "venue": "Elsevier Internet of Things", "year": 2024},
        {"title": "Centralised vs. Decentralised Federated Load Forecasting in Smart Buildings",
         "venue": "Elsevier Energy & Buildings", "year": 2024}
    ],

    "references": [
        "Prof. Dr. Muhammad Ali Imran — Professor of Communication Systems, Head of School, University of Glasgow",
        "Dr. Ahmed Zoha — Senior Lecturer (Autonomous Systems & Connectivity), University of Glasgow"
    ]
}
